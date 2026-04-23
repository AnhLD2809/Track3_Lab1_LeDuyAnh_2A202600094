from __future__ import annotations
import json, os, time
from dotenv import load_dotenv
from openai import OpenAI
from .prompts import ACTOR_SYSTEM, EVALUATOR_SYSTEM, REFLECTOR_SYSTEM
from .schemas import JudgeResult, QAExample, ReflectionEntry
from .utils import normalize_answer

load_dotenv()
_client: OpenAI | None = None

def _get_client() -> OpenAI:
    global _client
    if _client is None:
        # Sử dụng Ollama OpenAI compatible API
        _client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
    return _client

_MODEL = "qwen2.5:1.5b"

def generate_plan(example: QAExample) -> str:
    """Bonus: plan_then_execute – sinh kế hoạch trước attempt đầu tiên."""
    ctx = "\n".join(f"[{i+1}] {c.title}: {c.text}" for i, c in enumerate(example.context))
    resp = _get_client().chat.completions.create(
        model=_MODEL,
        messages=[
            {"role": "system", "content": "You are a planning assistant for multi-hop QA."},
            {"role": "user", "content": f"Question: {example.question}\n\nContext:\n{ctx}\n\nGive a 2-step plan to answer. Format: Step 1: ... Step 2: ..."},
        ],
        max_tokens=120, temperature=0,
    )
    return resp.choices[0].message.content.strip()

def actor_answer(example: QAExample, attempt_id: int, agent_type: str,
                 reflection_memory: list[str], plan: str = "") -> tuple[str, int, int]:
    """Gọi LLM sinh câu trả lời. Returns (answer, tokens, latency_ms)."""
    ctx = "\n".join(f"[{i+1}] {c.title}: {c.text}" for i, c in enumerate(example.context))
    parts = [f"Question: {example.question}", "", f"Context:\n{ctx}"]
    if plan:
        parts += ["", f"Plan:\n{plan}"]
    if reflection_memory:
        lessons = "\n".join(f"- {m}" for m in reflection_memory)
        parts += ["", f"Past lessons (apply these):\n{lessons}"]
    parts += ["", "Short final answer:"]

    t0 = time.time()
    resp = _get_client().chat.completions.create(
        model=_MODEL,
        messages=[{"role": "system", "content": ACTOR_SYSTEM},
                  {"role": "user", "content": "\n".join(parts)}],
        max_tokens=60, temperature=0,
    )
    return (resp.choices[0].message.content.strip(),
            resp.usage.total_tokens,
            int((time.time() - t0) * 1000))

def evaluator(example: QAExample, answer: str) -> tuple[JudgeResult, int, int]:
    """Bonus: structured_evaluator – trả về missing_evidence + spurious_claims."""
    t0 = time.time()
    resp = _get_client().chat.completions.create(
        model=_MODEL,
        messages=[{"role": "system", "content": EVALUATOR_SYSTEM},
                  {"role": "user", "content": (
                      f"Question: {example.question}\n"
                      f"Gold: {example.gold_answer}\n"
                      f"Predicted: {answer}\n\nReturn ONLY valid JSON.")}],
        max_tokens=300, temperature=0,
        response_format={"type": "json_object"},
    )
    latency_ms = int((time.time() - t0) * 1000)
    try:
        d = json.loads(resp.choices[0].message.content)
        judge = JudgeResult(score=int(d.get("score", 0)), reason=d.get("reason", ""),
                            missing_evidence=d.get("missing_evidence", []),
                            spurious_claims=d.get("spurious_claims", []))
    except Exception:
        correct = normalize_answer(example.gold_answer) == normalize_answer(answer)
        judge = JudgeResult(score=1 if correct else 0, reason="Fallback match")
    return judge, resp.usage.total_tokens, latency_ms

def reflector(example: QAExample, attempt_id: int, judge: JudgeResult) -> tuple[ReflectionEntry, int, int]:
    """Gọi LLM sinh reflection entry."""
    t0 = time.time()
    resp = _get_client().chat.completions.create(
        model=_MODEL,
        messages=[{"role": "system", "content": REFLECTOR_SYSTEM},
                  {"role": "user", "content": (
                      f"Question: {example.question}\n"
                      f"Evaluator reason: {judge.reason}\n"
                      f"Missing: {judge.missing_evidence}\n"
                      f"Spurious: {judge.spurious_claims}\nReturn ONLY valid JSON.")}],
        max_tokens=300, temperature=0,
        response_format={"type": "json_object"},
    )
    latency_ms = int((time.time() - t0) * 1000)
    try:
        d = json.loads(resp.choices[0].message.content)
        entry = ReflectionEntry(attempt_id=attempt_id,
                                failure_reason=d.get("failure_reason", judge.reason),
                                lesson=d.get("lesson", "Re-read context carefully."),
                                next_strategy=d.get("next_strategy", "Trace all hops explicitly."))
    except Exception:
        entry = ReflectionEntry(attempt_id=attempt_id, failure_reason=judge.reason,
                                lesson="Re-examine all context passages.",
                                next_strategy="Trace every hop explicitly before answering.")
    return entry, resp.usage.total_tokens, latency_ms

def adaptive_max_attempts(example: QAExample, base: int = 3) -> int:
    """Bonus: adaptive_max_attempts – điều chỉnh theo độ khó."""
    return {"easy": 2, "medium": 3, "hard": 4}.get(example.difficulty, base)
