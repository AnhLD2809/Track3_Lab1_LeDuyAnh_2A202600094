# Lab 16 Benchmark Report

## Metadata
- Dataset: hotpot_hard
- Mode: real
- Records: 20
- Total tokens: 14844
- Total latency (ms): 62238
- Agents: react, reflexion

## Summary
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| EM | 0.8 | 0.8 | 0.0 |
| Avg attempts | 1 | 1.7 | 0.7 |
| Avg token estimate | 486.3 | 998.1 | 511.8 |
| Avg latency (ms) | 2691.5 | 3532.3 | 840.8 |

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
