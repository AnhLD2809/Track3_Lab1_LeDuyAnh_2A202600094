# Lab 16 Benchmark Report

## Metadata
- Dataset: sample_run_qwen2.5_0.5b
- Mode: real
- Records: 200
- Total tokens: 118457
- Total latency (ms): 492995
- Agents: react, reflexion

## Summary
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| EM | 0.9 | 0.92 | 0.02 |
| Avg attempts | 1 | 1.23 | 0.23 |
| Avg token estimate | 482.25 | 702.32 | 220.07 |
| Avg latency (ms) | 2433.81 | 2496.14 | 62.33 |

## Failure modes
```json
{
  "none": 182,
  "wrong_final_answer": 10,
  "reflection_overfit": 8
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
