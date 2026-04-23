# Lab 16 Benchmark Report

## Metadata
- Dataset: hotpot_medium
- Mode: real
- Records: 20
- Total tokens: 11554
- Total latency (ms): 47997
- Agents: react, reflexion

## Summary
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| EM | 0.9 | 0.9 | 0.0 |
| Avg attempts | 1 | 1.2 | 0.2 |
| Avg token estimate | 480.3 | 675.1 | 194.8 |
| Avg latency (ms) | 2593.5 | 2206.2 | -387.3 |

## Failure modes
```json
{
  "none": 18,
  "wrong_final_answer": 1,
  "reflection_overfit": 1
}
```

## Extensions implemented
- structured_evaluator
- reflection_memory
- adaptive_max_attempts
- plan_then_execute
- benchmark_report_json
- mock_mode_for_autograding

## Discussion
[ĐIỀN KẾT QUẢ THỰC TẾ VÀ ĐÁNH GIÁ CỦA BẠN VÀO ĐÂY]
