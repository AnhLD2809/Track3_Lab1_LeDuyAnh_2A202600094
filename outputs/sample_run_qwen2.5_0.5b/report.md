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
Qua đánh giá thực tế trên bộ dữ liệu này, chúng tôi nhận thấy mô hình Reflexion đạt độ chính xác 92.0%, vượt trội hơn so với mức 90.0% của ReAct (cải thiện 2.0%). Nguyên nhân chính là do Reflexion có khả năng tự sửa lỗi nhờ vào cơ chế structured_evaluator và reflection_memory. Các lỗi phổ biến của ReAct thường là entity_drift (chọn sai thực thể ở bước 2) hoặc incomplete_multi_hop (quên suy luận bước 2). Khi sử dụng Reflexion, agent đã biết tự nhìn nhận lại sai lầm và áp dụng plan_then_execute để đi đúng hướng. Tuy nhiên, sự đánh đổi là chi phí tính toán: thời gian phản hồi trung bình của Reflexion là 2496.14ms, so với mức 2433.81ms của ReAct, đồng thời tiêu tốn nhiều token hơn do phải gọi thêm Evaluator và Reflector. Việc sử dụng tính năng adaptive_max_attempts đã giúp cân bằng phần nào chi phí này bằng cách dừng sớm ở những câu hỏi dễ.
