# Individual Report: Lab 3 - Chatbot vs ReAct Agent

- **Student Name**: Trần Thái Huy
- **Student ID**: 2A202600309
- **Date**: 2026-04-06

---

## I. Technical Contribution (15 Points)

Phần đóng góp chính của tôi trong bài lab này là thiết kế và triển khai giao diện demo web để trình bày rõ sự khác nhau giữa Chatbot Baseline và ReAct Agent. Ngoài phần UI, tôi có chỉnh nhẹ phần technical để frontend có thể hiển thị đúng trace, tool calls và metrics của agent.

- **Modules Implemented**:
  - `frontend/index.html`
  - `frontend/styles.css`
  - `frontend/app.js`
  - `web_demo.py`
  - Cập nhật thêm ở `src/agent/chatbot.py`
  - Cập nhật thêm ở `src/agent/agent.py`

- **Code Highlights**:
  - Xây dựng giao diện tiếng Việt cho demo AI lab, gồm phần chọn mode Baseline / Agent, vùng chat chính, prompt mẫu, panel trace và metrics.
  - Tạo web server local đơn giản để nối frontend với backend, giúp demo có thể chạy thật trên máy local thay vì chỉ là mock UI.
  - Chỉnh phần trả dữ liệu từ backend để `BaselineChatbot` và `ReActAgent` có thể trả về cấu trúc gồm `answer`, `trace`, `tool_calls`, `metrics`.
  - Có chỉnh phần action parsing / trace extraction ở agent để frontend hiển thị được các bước `Thought`, `Action`, `Observation`, `Final Answer` theo panel riêng.
  - Có xử lý lại phần format đầu ra để câu trả lời hiển thị gọn hơn, tránh markdown thừa trong giao diện demo.

- **Documentation**:
  - UI đóng vai trò lớp trình bày giúp người xem hiểu nhanh hệ thống làm gì và vì sao Agent tốt hơn Baseline.
  - Backend được nối thêm API cục bộ để nhận câu hỏi từ giao diện, gọi vào `BaselineChatbot` hoặc `ReActAgent`, rồi trả về dữ liệu có cấu trúc.
  - Phần cập nhật ở `agent.py` giúp trace của vòng lặp ReAct không chỉ chạy nội bộ mà còn có thể quan sát được trên giao diện, điều này rất quan trọng cho mục tiêu demo trước lớp.

---

## II. Debugging Case Study (10 Points)

Phần này tôi không trực tiếp phụ trách trong quá trình làm bài, nên không ghi thành một case study riêng.

---

## III. Personal Insights: Chatbot vs ReAct (10 Points)

1. **Reasoning**: So với Chatbot Baseline, ReAct Agent thể hiện rõ quá trình suy luận theo từng bước. Chatbot thường trả lời trực tiếp dựa trên tri thức có sẵn trong model, còn ReAct Agent có thể chia nhỏ bài toán thành các bước như xác định địa điểm, kiểm tra thời tiết, rồi mới tổng hợp phương án đi cắm trại phù hợp. Việc có `Thought` block giúp Agent xử lý bài toán nhiều bước một cách có cấu trúc hơn.

2. **Reliability**: ReAct Agent có thể lấy được nhiều thông tin hơn chatbot khi hệ thống được cấu hình API đầy đủ. Cụ thể, agent có thể:
   - tìm địa điểm cắm trại thực tế bằng `search_camp_site`
   - lấy dự báo thời tiết bằng `get_weather_forecast`
   - tổng hợp khuyến nghị di chuyển và đồ dùng bằng `get_travel_and_gear_recommendations`

   Trong khi đó, Chatbot Baseline chủ yếu chỉ trả lời từ prompt và kiến thức mô hình, nên dễ đưa ra gợi ý chung chung hoặc tự suy đoán. Tuy vậy, Agent cũng có thể kém hơn nếu tool lỗi, thiếu API key, hoặc model sinh sai format `Action` / `Action Input`.

3. **Observation**: Điểm mạnh nhất của ReAct là có `Observation` từ môi trường. Sau mỗi lần gọi tool, Agent nhận được dữ liệu phản hồi thực tế rồi mới quyết định bước tiếp theo. Nhờ vậy, câu trả lời cuối cùng bám sát điều kiện thực hơn, ví dụ biết được khu vực nào có địa điểm phù hợp, ngày nào có khả năng mưa, hoặc cần chuẩn bị thêm áo mưa và bạt che. Đây là khác biệt rất rõ so với chatbot thông thường, vốn không có cơ chế nhận phản hồi từ môi trường để tự điều chỉnh.

---

## IV. Future Improvements (5 Points)

- **UI / UX**: Có thể bổ sung chế độ so sánh song song Baseline và Agent trên cùng một prompt để việc demo trực quan hơn.
- **Reliability**: Có thể chuẩn hoá output format của agent mạnh hơn để giao diện luôn hiển thị ổn định, kể cả khi model đổi cách diễn đạt.

---

> [!NOTE]
> File này được viết theo phạm vi đóng góp thực tế của cá nhân, tập trung chủ yếu vào phần giao diện và lớp kết nối để quan sát được quá trình hoạt động của ReAct Agent.
