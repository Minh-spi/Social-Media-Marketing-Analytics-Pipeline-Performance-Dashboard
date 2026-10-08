# Root-cause summary — Bước 3

## Kết luận

**ER thấp của Entertainment liên quan mạnh nhất đến khoảng cách gắn với Content Category (category-associated residual), chưa được giải thích bởi các mix quan sát. Post Type mix chỉ giải thích một phần nhỏ trên common support. Khoảng cách vẫn còn khi so trong cùng platform, region và platform × post type; kết quả consistent with phần chênh lệch chưa được giải thích, chưa xác định nguyên nhân business hoặc creative cụ thể.**

Không có bằng chứng để viết “ER thấp chủ yếu vì platform/hashtag/thời điểm”. Primary finding là residual quan sát, không phải category gây ER thấp. Không có target nên đây không phải kết luận không đạt mục tiêu marketing.

## Primary / secondary / unsupported

| Phân loại | Yếu tố / hypothesis | Evidence |
| --- | --- | --- |
| Primary finding | Category-associated residual; driver thực tế chưa xác định | 16 tháng trọn: n=876 Entertainment / 4.714 non-Entertainment; mean source ER 7.51% vs 16.72%, gap 9.21 pp; median gap 9.14 pp |
| Primary finding | Residual trong segment tương đồng | Platform: gap 8.95–9.46 pp, 6/6 platform. Region: 8.90–9.44 pp, 8/8 region |
| Secondary, giải thích một phần nhỏ | Post Type mix | Composition 0.213 pp trên 4 định dạng đủ mẫu; subset gap 9.63 pp; coverage Entertainment 97.83%, Rest 79.40%. Đây không phải phần trăm gap toàn mẫu |
| Secondary, khác biệt mức gap | Platform × Post Type | LinkedIn Video gap 4,00 pp (n=66/33), TikTok Video 10,03 pp (n=193/803). Cả hai vẫn thấp hơn Rest; không phải interaction được xác nhận causal |
| Weak / unsupported | Platform, Content_Type, Region mix | Composition lần lượt -0.005, -0.012, 0.008 pp; không giải thích mức gap khoảng 9 pp |
| Weak / unsupported | Month, Weekday, Hour mix | Composition -0.006, -0.002, -0.000 pp trên common support tương ứng; không có tín hiệu timing mix giải thích gap lớn |
| Không tách được effect độc lập | Main hashtag | Chỉ 1 tag có ≥30 record ở cả hai nhóm; coverage Entertainment 5.25%. #TrendingNow có 515 Entertainment vs 20 Rest; n Rest nhỏ. Không quy kết hashtag là nguyên nhân |

Post Type là secondary yếu về mức giải thích, không phải driver mạnh. Các decomposition phân tích riêng từng chiều, không được cộng lại thành tỷ lệ giải thích chung. Composition âm nghĩa là khác biệt mix đang bù nhẹ gap trên subset, không tạo ra gap.

## Interaction

Platform × Post Type có **8 cell đủ mẫu**, bao phủ **90.75% Entertainment** và **66.06% Rest**. Không cell đủ mẫu nào có mean ER Entertainment bằng hoặc cao hơn Rest; gap cell **4.00–10.03 pp**. Nếu chuẩn hóa Rest theo mix Entertainment trên subset này, gap vẫn **8.65 pp**.

Composition của joint platform × post type là **0.323 pp**, within-segment **8.95 pp**, tổng gap subset **9.27 pp**. Không thấy tổ hợp này giải thích phần lớn gap. Các joint platform × Content_Type, region × post type, post type × Content_Type và platform × hour cũng có bảng coverage/gap riêng; các cell nhỏ được giữ nhưng không overclaim.

Trong 8 cell này, mean ER Entertainment chỉ dao động **7.22%–7.80%**, còn Rest **11.58%–17.64%**. Mức gap khác nhau đi cùng mức benchmark Rest khác nhau; không đủ chứng minh hiệu ứng interaction độc lập. Platform × hour chỉ có **15.18%** Entertainment đủ common support, nên kết luận tổ hợp thời gian bị hạn chế phạm vi.

Platform/Region/Content_Type × Category và Time × Category đều được xuất mean/median, n và volume. Đối chiếu từng category không dùng một benchmark business chung. Không có cell Entertainment “tốt hơn Rest” trong các so sánh chính đủ mẫu; điều này không chứng minh mọi tổ hợp hiếm đều như vậy.

## Robustness

| Kiểm tra | Evidence |
| --- | --- |
| Theo tháng | Gap dương trong 16/16 tháng trọn; khoảng 8.26–9.83 pp; tất cả n≥30 mỗi nhóm |
| Mean vs median | Gap 9.21 vs 9.14 pp; không đổi chiều |
| Thêm tháng partial | Gap 9.21 pp |
| Giảm trọng số mã lặp | Gap 9.22 pp; không deduplicate hoặc chọn category đại diện |
| Winsor ER pooled 1%/99% | Gap 9.20 pp; chỉ sensitivity, không sửa dataset |
| Loại top 1% Views | Gap 9.23 pp; không xem record lớn là lỗi |
| Leave-one-platform / region-out | Gap 9.14–9.30 pp; không phụ thuộc một platform/region duy nhất |

Bảng ngưỡng n=10/30/50 lưu số cell và coverage cho từng phép so. Các gap còn dương trên common support; ngưỡng lớn làm giảm phạm vi, không được diễn giải như kết quả toàn bộ dataset. Không thấy thay đổi mạnh về chiều khoảng cách giữa các sensitivity chính.

## Secondary problem

Product Promotion được kiểm tra riêng trong cùng platform, post type và region với n mỗi nhóm ≥30: gap còn dương trong **19 cell đủ mẫu**, từ **3.17 đến 6.97 pp**. Evidence lưu tại [bảng secondary](artifacts/tables/secondary_product_promotion.csv). Đây là kiểm tra mô tả giới hạn; không chọn thêm root cause hoặc chuyển trọng tâm khỏi Entertainment.

## Giới hạn

- Observational segment comparison không kiểm soát mọi confounder; không chứng minh category, mix hoặc hashtag gây gap. Không dùng mô hình predictive/prescriptive.
- Công thức source ER chưa xác nhận; chưa biết có quy tắc tạo dữ liệu/nhãn gắn với category hay không. Không thể phân biệt hiệu ứng nội dung thực với cơ chế đo lường từ file này.
- Post_ID lặp, có ID khác category; grain nghiệp vụ và cửa sổ đo chưa rõ. Mean/median là ở cấp record; tổng Views/Impressions/Engagement không được coi là lượng unique post/person.
- Không có creative/caption, audience, follower base, campaign objective, spend, timezone hoặc dữ liệu thử nghiệm; chưa xác định mechanism business/creative.
- Common support hạn chế với tag và một số interaction. Ngưỡng mẫu là rule sàng lọc, không phải kiểm định significance; không suy rộng ra ngoài mẫu.

**Kết thúc bước 3:** driver mix quan sát chưa giải thích phần lớn gap; bằng chứng mạnh nhất là category-associated residual ổn định. Không đưa recommendation, giải pháp hoặc sang bước 4.

**Nguồn:** [Hypotheses](00_hypothesis_setup.md), [Driver notebook](01_hypothesis_and_driver_analysis.ipynb), [Interaction & robustness notebook](02_interaction_and_robustness.ipynb), [Driver effects](artifacts/tables/driver_effect_summary.csv), [Interaction effects](artifacts/tables/interaction_effect_summary.csv), [Robustness](artifacts/tables/robustness_overall.csv).
