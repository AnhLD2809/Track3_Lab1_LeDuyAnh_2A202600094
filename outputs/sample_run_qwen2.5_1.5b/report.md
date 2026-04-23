# Lab 16 Benchmark Report

## Metadata
- Dataset: sample_run_qwen2.5_1.5b
- Mode: real
- Records: 200
- Total tokens: 105249
- Total latency (ms): 369643
- Agents: react, reflexion

## Summary
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| EM | 0.95 | 0.98 | 0.03 |
| Avg attempts | 1 | 1.03 | 0.03 |
| Avg token estimate | 470.75 | 581.74 | 110.99 |
| Avg latency (ms) | 2008.38 | 1688.05 | -320.33 |

## Failure modes
```json
{
  "none": 193,
  "wrong_final_answer": 5,
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
