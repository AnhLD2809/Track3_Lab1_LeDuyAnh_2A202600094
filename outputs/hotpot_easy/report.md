# Lab 16 Benchmark Report

## Metadata
- Dataset: hotpot_easy
- Mode: real
- Records: 20
- Total tokens: 12117
- Total latency (ms): 51388
- Agents: react, reflexion

## Summary
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| EM | 0.8 | 0.8 | 0.0 |
| Avg attempts | 1 | 1.3 | 0.3 |
| Avg token estimate | 482.9 | 728.8 | 245.9 |
| Avg latency (ms) | 2571.4 | 2567.4 | -4.0 |

## Failure modes
```json
{
  "none": 16,
  "wrong_final_answer": 2,
  "reflection_overfit": 2
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
