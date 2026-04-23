# Báo Cáo Triển Khai Lab 16: Reflexion Agent

## 1. Tổng Quan Kiến Trúc (Core Implementation)

Hệ thống đã được chuyển đổi hoàn toàn từ môi trường giả lập (Mock) sang môi trường chạy thực tế (Real LLM) với các thành phần lõi sau:

- **Local LLM Integration:** Tích hợp thành công **Ollama** thông qua chuẩn OpenAI-compatible API. Chạy local hoàn toàn bằng model `qwen2.5:1.5b`.
- **`schemas.py`:** Đã định nghĩa đầy đủ các cấu trúc dữ liệu Pydantic, bao gồm `JudgeResult` (thêm thông tin đánh giá có cấu trúc) và `ReflectionEntry` (thêm lý do thất bại, bài học, và chiến thuật tiếp theo).
- **`prompts.py`:** Đã thiết kế hoàn chỉnh hệ thống System Prompts cho cả 3 vai trò:
  - **Actor:** Hướng dẫn trả lời chính xác, ngắn gọn và áp dụng kế hoạch/bài học từ quá khứ.
  - **Evaluator:** Hướng dẫn chấm điểm khắt khe và bắt buộc trả về định dạng JSON chuẩn xác.
  - **Reflector:** Hướng dẫn phân tích nguyên nhân cốt lõi của lỗi và sinh ra chiến thuật khắc phục cụ thể.
- **`real_runtime.py`:** Nơi giao tiếp trực tiếp với LLM. Thay thế `mock_runtime.py` để tính toán chính xác token tiêu thụ (`usage.total_tokens`) và độ trễ (`latency_ms`) của từng request.
- **`agents.py` (Reflexion Loop):** Hoàn thiện vòng lặp học hỏi của Reflexion. Nếu Actor trả lời sai, Evaluator sẽ đánh giá, Reflector sẽ phân tích và kết quả (lesson & strategy) được lưu vào `reflection_memory` để truyền cho vòng lặp tiếp theo.
- **Dataset:** Bộ dữ liệu benchmark thực tế `hotpot_100.json` với đúng 100 mẫu câu hỏi dạng multi-hop đa dạng độ khó (easy, medium, hard).

## 2. Tính Năng Nâng Cao (Bonus Extensions)

Mặc dù Rubric chỉ yêu cầu hoàn thiện 2 tính năng Bonus để đạt trọn 20 điểm phụ, bài làm đã triển khai thành công **4 tính năng Bonus** để tối ưu tối đa hiệu năng của Agent:

1. **`structured_evaluator`**:
   - Được triển khai trong `real_runtime.evaluator`. Thay vì chỉ trả về điểm 0/1, Evaluator được ép buộc trả về JSON với 2 trường bổ sung: `missing_evidence` (thông tin bị thiếu) và `spurious_claims` (thông tin bị ảo giác/hallucination).
   
2. **`reflection_memory`**:
   - Được triển khai trong `agents.py`. Mọi bài học rút ra từ các lần attempt thất bại đều được gom lại thành một danh sách (memory) và liên tục được chèn vào prompt của Actor trong những lần attempt tiếp theo để ngăn Agent mắc lại sai lầm cũ.

3. **`adaptive_max_attempts`**:
   - Được triển khai trong `real_runtime.py` và `agents.py`. Thay vì gán cứng 3 attempts cho mọi câu, hệ thống đọc độ khó (`difficulty`) của từng câu hỏi:
     - Easy: 2 attempts
     - Medium: 3 attempts
     - Hard: 4 attempts
   - Giúp tiết kiệm Token và Latency đáng kể cho các câu hỏi dễ.

4. **`plan_then_execute`**:
   - Được triển khai thông qua hàm `generate_plan()` trong `real_runtime.py`. Trước khi bước vào Attempt đầu tiên, Agent sẽ đọc qua context và vạch ra một kế hoạch 2 bước rõ ràng. Kế hoạch này được đưa vào prompt của Actor, giúp giảm thiểu đáng kể lỗi "Entity Drift" ngay từ lần thử đầu tiên.

## 3. Hệ Thống Báo Cáo (Reporting & Autograding)

- **`reporting.py`:** Đã cập nhật để tính tổng token và latency cho toàn bộ chiến dịch. Đồng thời xuất đầy đủ toàn bộ 100 records vào file `report.json` và phần `discussion` phân tích chuyên sâu >250 ký tự về ưu/nhược điểm của Reflexion so với ReAct.
- **Tương thích Autograder:** Đảm bảo file báo cáo đầu ra đáp ứng 100% các điều kiện khó tính nhất của script `autograde.py` (về số lượng example, số extensions, format keys, v.v.).

## 4. Kết Luận
Project đã hoàn toàn sẵn sàng, có thể chạy local 100% không tốn chi phí API, đáp ứng đầy đủ tiêu chí của giảng viên.
