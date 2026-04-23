# Lab 16 Benchmark Report

## Metadata
- Dataset: sample_run
- Mode: real
- Records: 200
- Total tokens: 792335
- Total latency (ms): 987573
- Agents: react, reflexion

## Summary
| Metric | ReAct | Reflexion | Delta |
|---|---:|---:|---:|
| EM | 0.23 | 0.45 | 0.22 |
| Avg attempts | 1 | 2.85 | 1.85 |
| Avg token estimate | 1931.19 | 5992.16 | 4060.97 |
| Avg latency (ms) | 2617.48 | 7258.25 | 4640.77 |

## Failure modes
```json
{
  "wrong_final_answer": 77,
  "none": 68,
  "reflection_overfit": 55
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
Qua bài kiểm tra giới hạn (Stress Test) trên bộ dữ liệu này, chúng tôi nhận thấy mô hình Reflexion đạt độ chính xác 45.0%, vượt trội hơn gần gấp đôi so với mức 23.0% của ReAct (cải thiện 22.0%). Dữ liệu cho thấy ở bài test cực khó này, ReAct gần như thất bại thảm hại do không thể xử lý tốt các câu phức tạp đa bước. Ngược lại, Reflexion nhờ có khả năng tự sửa lỗi qua structured_evaluator và reflection_memory đã cứu vớt được một lượng lớn các câu trả lời sai ban đầu. Tuy nhiên, cái giá phải trả cho độ khó này là rất lớn: thời gian phản hồi trung bình của Reflexion lên tới 7258.25ms (gấp gần 3 lần so với mức 2617.48ms của ReAct), đồng thời tiêu tốn một lượng token khổng lồ do trung bình phải thử lại tới 2.85 lần mỗi câu (gọi liên tục Evaluator và Reflector). Dù đã có adaptive_max_attempts và plan_then_execute hỗ trợ, stress test này chứng minh rằng Reflexion là công cụ rất mạnh mẽ nhưng cần cân nhắc kỹ về chi phí vận hành trong môi trường thực tế.
