from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Literal
from .schemas import AttemptTrace, QAExample, ReflectionEntry, RunRecord

_USE_REAL = os.getenv("USE_REAL_LLM", "0") == "1"

if _USE_REAL:
    from .real_runtime import (actor_answer as _actor, evaluator as _evaluator,
                                reflector as _reflector, generate_plan, adaptive_max_attempts)
else:
    from .mock_runtime import (FAILURE_MODE_BY_QID as _FMAP,
                                actor_answer as _mock_actor,
                                evaluator as _mock_evaluator,
                                reflector as _mock_reflector)
    def _actor(ex, aid, at, mem, plan=""):
        ans = _mock_actor(ex, aid, at, mem)
        tok = 320 + aid * 65 + (120 if at == "reflexion" else 0)
        lat = 160 + aid * 40 + (90 if at == "reflexion" else 0)
        return ans, tok, lat
    def _evaluator(ex, ans):
        j = _mock_evaluator(ex, ans); return j, 80, 50
    def _reflector(ex, aid, j):
        e = _mock_reflector(ex, aid, j); return e, 60, 40
    def generate_plan(ex): return ""
    def adaptive_max_attempts(ex, base=3): return base
    _FMAP: dict = {}


@dataclass
class BaseAgent:
    agent_type: Literal["react", "reflexion"]
    max_attempts: int = 1

    def run(self, example: QAExample) -> RunRecord:
        reflection_memory: list[str] = []
        reflections: list[ReflectionEntry] = []
        traces: list[AttemptTrace] = []
        final_answer = ""
        final_score = 0

        # Bonus: plan_then_execute
        plan = ""
        if _USE_REAL and self.agent_type == "reflexion":
            try:
                plan = generate_plan(example)
            except Exception:
                plan = ""

        for attempt_id in range(1, self.max_attempts + 1):
            answer, tokens, latency_ms = _actor(example, attempt_id, self.agent_type, reflection_memory, plan)
            judge, eval_tok, eval_lat = _evaluator(example, answer)
            tokens += eval_tok
            latency_ms += eval_lat

            trace = AttemptTrace(attempt_id=attempt_id, answer=answer,
                                 score=judge.score, reason=judge.reason,
                                 token_estimate=tokens, latency_ms=latency_ms)
            final_answer = answer
            final_score = judge.score
            traces.append(trace)

            if judge.score == 1:
                break

            # Reflexion loop
            if self.agent_type == "reflexion" and attempt_id < self.max_attempts:
                entry, ref_tok, ref_lat = _reflector(example, attempt_id, judge)
                reflections.append(entry)
                trace.reflection = entry
                # Bonus: reflection_memory
                reflection_memory.append(
                    f"[Attempt {attempt_id}] {entry.lesson} Strategy: {entry.next_strategy}"
                )
                tokens += ref_tok
                latency_ms += ref_lat

        total_tokens = sum(t.token_estimate for t in traces)
        total_latency = sum(t.latency_ms for t in traces)

        if final_score == 1:
            failure_mode = "none"
        elif _USE_REAL:
            r = (traces[-1].reason or "").lower()
            if "hop" in r or "incomplete" in r:
                failure_mode = "incomplete_multi_hop"
            elif "hallucin" in r or "spurious" in r or "entity" in r:
                failure_mode = "entity_drift"
            elif len(traces) >= self.max_attempts and self.agent_type == "reflexion":
                failure_mode = "reflection_overfit"
            else:
                failure_mode = "wrong_final_answer"
        else:
            failure_mode = _FMAP.get(example.qid, "wrong_final_answer")

        return RunRecord(
            qid=example.qid, question=example.question, gold_answer=example.gold_answer,
            agent_type=self.agent_type, predicted_answer=final_answer,
            is_correct=bool(final_score), attempts=len(traces),
            token_estimate=total_tokens, latency_ms=total_latency,
            failure_mode=failure_mode, reflections=reflections, traces=traces,
        )


class ReActAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__(agent_type="react", max_attempts=1)


class ReflexionAgent(BaseAgent):
    def __init__(self, max_attempts: int = 3) -> None:
        super().__init__(agent_type="reflexion", max_attempts=max_attempts)

    def run(self, example: QAExample) -> RunRecord:
        # Bonus: adaptive_max_attempts
        if _USE_REAL:
            self.max_attempts = adaptive_max_attempts(example, base=self.max_attempts)
        return super().run(example)
