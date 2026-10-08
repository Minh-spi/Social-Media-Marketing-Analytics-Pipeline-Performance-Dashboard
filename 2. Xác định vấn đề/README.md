# Bước 2 — Xác định vấn đề

Chạy `01_data_preparation.ipynb` trước, rồi `02_baseline_and_problem_detection.ipynb`. Dependencies: Python, pandas, openpyxl, numpy, matplotlib, tabulate. Có thể tái tạo toàn bộ output bằng `python "2. Xác định vấn đề/build_step2.py"` từ project root.

| Output | Nội dung |
| --- | --- |
| [Data preparation](01_data_preparation.ipynb) | Kiểu dữ liệu, null, duplicate, miền KPI; lưu dataset riêng |
| [Analysis-ready CSV](artifacts/analysis_ready.csv) | Giữ nguyên record/missing; thêm trường phân tích và cờ chất lượng |
| [Data quality summary](04_data_quality_summary.md) | Rule xử lý, số lượng và giới hạn còn lại |
| [Baseline & detection](02_baseline_and_problem_detection.ipynb) | Baseline, time trend, breakdown, evidence và độ nhạy |
| [Problem statement](03_problem_statement.md) | Candidates, chấm ưu tiên, problem chính và secondary |
| [Bảng dữ liệu](artifacts/tables) / [Biểu đồ](artifacts/figures) | Output tĩnh để đối chiếu số liệu |

**Problem chính:** Entertainment có mean source ER thấp hơn rõ rệt phần còn lại, trong khi đóng góp volume Views đáng kể; khoảng cách duy trì qua 16 tháng trọn. Product Promotion được giữ làm secondary. Không có KPI target; đây là tín hiệu cần điều tra, chưa phải kết luận không đạt mục tiêu.

Không thực hiện phân tích nguyên nhân, recommendation, predictive/prescriptive analysis hoặc dashboard cuối cùng.
