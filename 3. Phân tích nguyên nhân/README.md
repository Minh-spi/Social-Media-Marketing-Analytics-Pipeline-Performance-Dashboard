# Bước 3 — Phân tích nguyên nhân

Đọc [root-cause summary](03_root_cause_summary.md) để xem kết luận, evidence và giới hạn. Các mix quan sát chưa giải thích phần lớn khoảng cách ER; category-associated residual là phát hiện chính, không phải nguyên nhân causal được xác nhận.

| Deliverable | Nội dung |
| --- | --- |
| [Hypothesis setup](00_hypothesis_setup.md) | Driver, logic, metric và cách kiểm tra |
| [Driver analysis](01_hypothesis_and_driver_analysis.ipynb) | Single-driver comparisons, record mix, common-support decomposition, hashtag overlap |
| [Interaction & robustness](02_interaction_and_robustness.ipynb) | Joint segments, heatmaps, coverage, sensitivity và secondary problem |
| [Summary](03_root_cause_summary.md) | Primary finding, secondary driver, unsupported hypotheses và giới hạn |
| [Tables](artifacts/tables) / [Figures](artifacts/figures) | Evidence đầy đủ; cell nhỏ vẫn giữ, gắn cờ |

**Tái tạo:** chạy từng notebook từ project root hoặc folder notebook. Hai notebook đọc dataset bước 2 độc lập. Hoặc chạy `python "3. Phân tích nguyên nhân/build_step3.py"` từ project root. Requires Python, pandas, numpy, matplotlib, tabulate; cần `2. Xác định vấn đề/artifacts/analysis_ready.csv` đã tạo ở bước 2.

Chỉ ghi output vào folder bước 3. Không sửa raw/bước 1/2, không recommendation, giải pháp, prescriptive/predictive model hoặc dashboard.
