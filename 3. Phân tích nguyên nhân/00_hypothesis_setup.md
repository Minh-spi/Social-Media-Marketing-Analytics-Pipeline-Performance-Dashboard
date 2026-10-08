# Hypothesis Setup

Đối tượng chính: Entertainment so với non-Entertainment trong 16 cohort tháng trọn (01/2024–04/2025). Tháng 05/2025 partial chỉ dùng kiểm tra độ nhạy. Secondary: Product Promotion, kiểm tra riêng ở mức giới hạn.

| ID | Driver / giả thuyết | Logic | Metric | Cách kiểm tra |
| --- | --- | --- | --- | --- |
| H1 | Platform mix | Entertainment tập trung ở kênh có ER thấp | Source ER mean/median, record mix, Views | So cùng platform; chuẩn hóa mix và decomposition |
| H2 | Post Type | Cơ cấu định dạng liên quan đến một phần gap | ER, record mix, Views/Engagement | So cùng post type; chuẩn hóa mix; kiểm tra platform × post type |
| H3 | Organic/Sponsored | Cơ cấu phân phối khác nhau liên quan đến gap | ER, record mix | So cùng Content_Type; decomposition |
| H4 | Region | Entertainment tập trung ở region có ER thấp | ER, record mix | So cùng Region; decomposition, leave-one-region-out |
| H5 | Month/Day/Hour | Cơ cấu thời điểm đăng liên quan đến gap | ER, số record | So cùng Month/Weekday/Post_Hour; không quy đổi timezone |
| H6 | Main hashtag | Nhóm hashtag gắn với ER thấp | ER, số record và common support | Cross-tab category × hashtag; chỉ so tag có cả hai nhóm đủ mẫu |
| H7 | Interaction | Một tổ hợp platform/định dạng/phân phối tập trung phần lớn gap | ER, cell n, Views; gap chuẩn hóa | So cùng platform × post type, platform × Content_Type, region × post type; xác định coverage |
| H8 | Độ nhạy | Gap phụ thuộc mẫu nhỏ/outlier/mã lặp/cách đo | Mean/median, gap pp | Ngưỡng 10/30/50; winsor 1%; trọng số mã; loại lần lượt platform/region |

Không giả thuyết nào được coi là causal từ phép so sánh observational. “Driver” là yếu tố liên quan được kiểm tra; không mặc định mọi hypothesis phải được ủng hộ.
