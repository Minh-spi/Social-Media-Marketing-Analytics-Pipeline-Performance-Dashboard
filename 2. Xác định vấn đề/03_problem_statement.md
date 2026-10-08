# Problem statement — Bước 2

## Kết luận chính

**Trong giai đoạn 01/01/2024–01/05/2025, nhóm Entertainment có Engagement_Rate trung bình nguồn 7.51%, thấp hơn 9.21 điểm phần trăm so với 16.73% của phần dữ liệu còn lại, cho thấy mức tương tác tương đối ghi nhận thấp trên nhóm chiếm 22.81% Views nhưng chỉ 12.66% Engagement của tổng record.**

Đây là vấn đề tiềm năng về khoảng cách engagement, không phải kết luận nhóm này không đạt mục tiêu: brief không có target và category có thể có mục đích marketing khác nhau. “ER” trong tài liệu là mean/median của rate nguồn ở cấp record; công thức chưa xác nhận. Không phải ER tính từ tổng và không quy đổi gap thành engagement thất thoát.

## Baseline và time trend

| KPI | Baseline toàn bộ file |
| --- | ---: |
| Record / Post_ID duy nhất | 5,600 / 5,000 |
| Impressions — tổng record | 5,766,555,744 |
| Views — tổng record | 4,806,275,234 |
| Engagement — tổng record | 646,491,442 |
| Mean / median source ER | 15.28% / 15.44% |
| Clicks — tổng phần có dữ liệu | 35,407,176 |
| Click coverage | 1,860/5,600 (33.21%) |
| Mean / median source CTR — phần có dữ liệu | 1.84% / 1.81% |

Các tháng trọn 01/2024–04/2025 có mean source ER từ **14.66% đến 15.68%**, mean source CTR quan sát từ **1.76% đến 1.92%**. ER tháng cuối trọn cao hơn tháng đầu 0.44 pp; không có chuỗi giảm liên tục. Tháng 04/2024 là điểm ER thấp nhất nhưng không được chọn là vấn đề chính vì khoảng cách nhỏ và các tháng sau không duy trì mức này.

Volume tháng trọn: Views **262,617,738–326,490,166**, Engagement **34,641,091–44,548,650**, Clicks phần quan sát **1,660,046–2,653,727**. Số record tháng **297–393**, click coverage **28.49%–36.34%**; chưa thể coi biến động tổng là biến động efficiency tương ứng.

Tháng 05/2025 chỉ có 10 record, ngày 01/05; tổng tháng thấp không được coi là performance giảm. Tổng theo tháng là performance của cohort ngày đăng, chưa có cửa sổ đo đồng nhất. Đồ thị và bảng kèm volume/coverage trong notebook.

## Segment performance summary

| Chiều | Dấu hiệu quan sát | Giới hạn đối chiếu |
| --- | --- | --- |
| Platform | Mean source ER: Instagram 15.85%, LinkedIn 14.33%; gap 1.52 pp | Volume/cơ cấu khác nhau; Click coverage LinkedIn chỉ 304/525, Instagram không có Clicks |
| Category | Educational 19.89%, Entertainment 7.51%; Entertainment có 22.81% Views | Mục tiêu category chưa xác nhận; đối chiếu mô tả |
| Post type | Video có 75.76% Views, mean ER 14.42% so với Image 17.86% | PDF/Carousel n < 100; không chọn nhóm nhỏ thành “tốt nhất” |
| Content type | Organic 15.26%, Sponsored 15.40% | Không có chi phí; không suy ra hiệu quả quảng cáo |
| Region | Germany 14.63%; các region còn lại 15.07%–15.47% | Nhãn Region chưa xác nhận là vị trí người xem |
| Time | Mean ER theo giờ 14.72%–15.67% | Không có timezone; chưa kết luận giờ tối ưu |
| Main hashtag | #TrendingNow: n=535, mean ER 7.97%; #SuccessStory: n=1.523, ER 19.96% | Một số tag chỉ 1–4 record; không khẳng định tác động hashtag |

## Problem candidates

| ID | KPI / segment / thời gian | Evidence | Ảnh hưởng sơ bộ quan sát |
| --- | --- | --- | --- |
| P1 | Source ER / Entertainment / toàn kỳ | n=877; 7.51% so với phần còn lại 16.73%; gap 9.21 pp (55.09% tương đối) | 22.81% Views, 12.66% Engagement; nhóm quy mô lớn có rate thấp tương đối |
| P2 | Source ER / Product Promotion / toàn kỳ | n=1385; 11.59% so với phần còn lại 16.50%; gap 4.90 pp (29.73% tương đối) | 40.12% Views, 34.55% Engagement; phạm vi exposure rộng |
| P3 | Source ER / Video so với Image / toàn kỳ | n=2.948 so với 996; 14.42% so với 17.86%; gap 3.43 pp | Video chiếm 75.76% Views; candidate rộng, chưa tách khỏi P1/P2 |
| P4 | Source ER / LinkedIn so với Instagram / toàn kỳ | n=525 so với 998; 14.33% so với 15.85%; gap 1.52 pp | LinkedIn chiếm 7.09% Views; magnitude nhỏ hơn category gap |
| P5 | Source ER / 04/2024 so với 03/2024 | n=353 so với 393; 14.66% so với 15.30%; thấp hơn 0.64 pp | Một cohort tháng; chưa thấy suy giảm duy trì |

Missing Click/CTR 66,79% là hạn chế đo lường, không được ghi thành vấn đề “click thấp”. Không có căn cứ định lượng thiệt hại doanh thu, chi phí hoặc phần engagement có thể tăng thêm.

## Problem prioritization

Điểm 1–4 là rule sàng lọc minh bạch, không phải KPI target hoặc kiểm định thống kê. Tổng điểm dùng trọng số bằng nhau:

- **Magnitude:** tỷ lệ thấp hơn comparator: ≥40% → 4; 25–<40% → 3; 10–<25% → 2; <10% → 1.
- **Scope:** share Views của segment: ≥30% → 4; 15–<30% → 3; 5–<15% → 2; <5% → 1. Với candidate tháng, share Views của cohort trong toàn kỳ.
- **Business relevance:** 4 nếu trực tiếp thuộc Content/Channel decision được brief nhấn mạnh; 3 cho lịch đăng/thị trường; 2 nếu chỉ liên quan gián tiếp; 1 nếu chưa gắn decision.
- **Data support:** 4 nếu KPI/grain/cửa sổ đo được xác nhận và có coverage đủ; 3 nếu n≥100, KPI đủ record nhưng còn giới hạn định nghĩa/grain; 2 nếu tín hiệu chỉ là một lần thay đổi giữa hai cohort liền kề hoặc coverage hạn chế; 1 nếu mẫu quá nhỏ/không đủ KPI.

| Candidate | Magnitude | Scope | Business relevance | Data support | Tổng | Ưu tiên |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| P1 — Entertainment | 4 | 3 | 4 | 3 | 14 | Chính |
| P2 — Product Promotion | 3 | 4 | 4 | 3 | 14 | Secondary |
| P3 — Video vs Image | 2 | 4 | 4 | 3 | 13 | Giữ trong candidate; chưa mở thêm problem |
| P4 — LinkedIn vs Instagram | 1 | 2 | 4 | 3 | 10 | Thấp hơn |
| P5 — 04/2024 | 1 | 2 | 3 | 2 | 8 | Thấp hơn |

P1/P2 cùng tổng điểm; chọn P1 theo tie-break **gap tương đối và gap pp lớn hơn**, cùng với độ bền mô tả qua các tháng. P2 có scope rộng hơn nên giữ đúng một secondary problem. P3 chưa mở thành problem riêng để giữ phạm vi điều tra gọn; chưa xác định quan hệ giữa các candidate.

## Evidence đủ để ưu tiên P1

- Mean source ER 7.51% so với 16.73%; median 7.51% so với 16.66%. Tín hiệu không chỉ xuất hiện ở mean.
- Chỉ tháng trọn: 7.51% so với 16.72%. Entertainment thấp hơn phần còn lại trong **16/16 cohort tháng trọn**; không dựa vào tháng partial.
- Giảm trọng số mã lặp: ER 7.51% so với 16.73%. Đây là kiểm tra độ nhạy, không giải quyết grain.
- n=877, không thiếu ER trong nhóm; mức 22.81% Views gắn trực tiếp với Content decision ở bước 1. Đủ metadata để tiếp tục điều tra mô tả, nhưng chưa đủ cho kết luận causal.

## Secondary problem statement

Trong giai đoạn 01/01/2024–01/05/2025, Product Promotion có Engagement_Rate trung bình nguồn 11.59%, thấp hơn 4.90 pp so với 16.50% của phần dữ liệu còn lại, cho thấy mức engagement tương đối ghi nhận thấp trên nhóm chiếm 40.12% Views và 34.55% Engagement của tổng record.

**Phạm vi bàn giao bước 3:** điều tra khoảng cách của P1, giữ P2 làm secondary. Bước 2 chỉ xác lập tín hiệu và mức ưu tiên; không giải thích nguyên nhân, đề xuất hành động, dựng dashboard hoặc model.

**Nguồn:** [Notebook phân tích](02_baseline_and_problem_detection.ipynb), [Data quality](04_data_quality_summary.md), [Evidence category](artifacts/tables/category_candidate_evidence.csv), [Evidence theo tháng](artifacts/tables/entertainment_monthly_evidence.csv).
