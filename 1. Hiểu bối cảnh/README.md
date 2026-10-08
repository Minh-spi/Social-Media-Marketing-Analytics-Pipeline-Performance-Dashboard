# Bước 1 — Hiểu bối cảnh

**Social Media Marketing Analytics Pipeline & Performance Dashboard**

Brief đặt tình huống social media cho một **công ty IT toàn cầu chưa nêu tên**; Onyx cung cấp dataset. Mục tiêu là hiểu hiệu suất để hỗ trợ quyết định chiến lược về nội dung và nền tảng. Chưa có KPI target hoặc benchmark business.

| Phần | Nội dung | Tài liệu |
| --- | --- | --- |
| Business Context | Doanh nghiệp, mục tiêu, phạm vi bước 1 | [Business context](Business%20Context/01_business_context.md) |
| Process Context | Content Decision → Publish → Exposure → Engagement → Action | [Process context](Process%20Context/02_process_context.md) |
| Measurement Context | KPI theo tầng; absolute/rate; định nghĩa chưa xác nhận | [Measurement context](Measurement%20Context/03_measurement_context.md) |
| Data Context | Grain, mapping, coverage, missing/duplicate, giới hạn kết luận | [Data context](Data%20Context/01_data_context.md) · [Notebook kiểm tra](Data%20Context/02_excel_context_checks.ipynb) |
| Decision Context | Channel, Content, Distribution, Market và câu hỏi cho bước sau | [Decision context](Decision%20Context/05_decision_context.md) |

Excel có **5.600 record, 24 cột, 5.000 Post_ID**, 6 platform và 8 region, bao phủ **01/01/2024–01/05/2025**. Phạm vi rộng hơn mô tả năm 2024 và 4 platform trong brief. Không có duplicate toàn dòng; mã bài và khóa ứng viên vẫn lặp. Click/CTR thiếu **66,79%**; công thức KPI và cửa sổ đo performance chưa rõ.

Flow là mô hình logic, không phải hành trình người dùng được theo dõi. Action hiện có chỉ là click; dữ liệu không có chi phí, doanh thu hoặc conversion sau click. Phân tích sau này có thể mô tả khác biệt quan sát, chưa đủ để khẳng định nhân quả hoặc ROI.

Bước 1 gồm tài liệu bối cảnh và kiểm tra cấu trúc dữ liệu. Không thực hiện xác định vấn đề, nguyên nhân, giải pháp, xếp hạng hiệu suất, dashboard hoặc predictive model.

**Nguồn:** [PDF business brief](../Social%20Media%20Marketing%20Performance%20Analytics.pdf) và [Excel dataset](../data/Social_Media_Content_Performance_Dataset.xlsx). Các tài liệu phân tích khác có sẵn không được dùng làm căn cứ kết luận trong bước này.
