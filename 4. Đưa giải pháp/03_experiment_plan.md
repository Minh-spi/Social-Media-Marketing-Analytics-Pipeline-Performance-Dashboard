# Experiment / Validation Plan

## Preconditions và thiết kế chung

1. Hoàn tất R1: định nghĩa ER được owner xác nhận, unique publication ID, timezone và cửa sổ đo cố định. Source ER lịch sử chỉ là tham chiếu; không đổi tên một công thức tự tính thành source ER. Nếu không xác nhận được, chưa dùng ER làm primary KPI để quyết định scale.
2. Hoàn tất R2: mục tiêu, một platform/format đủ khả năng test, KPI và baseline tương ứng. Chọn nơi có hoạt động Entertainment và capability randomization; không chọn LinkedIn vì gap lịch sử nhỏ nhất hoặc một kênh vì ER cao nhất.
3. Tạo control và treatment, randomize trước khi publish; log assignment, version, block và mọi deviation. Giữ platform, region/audience, Content_Type, offer, hashtag và các yếu tố khác cố định/cân bằng theo test. Sponsored cần cùng thiết lập phân phối và ghi spend; không mở rộng Sponsored chỉ để chạy test.
4. Ưu tiên native A/B có audience chia ngẫu nhiên và tránh overlap nếu capability cho phép. Randomization unit là audience/user; phân tích theo assignment, đúng cấp randomization. Nếu chỉ có post-level aggregate, dùng post/slot pairs: phân block theo platform × format × tuần/ngày, randomize variant vào slot, ghi nhận contamination từ audience lặp. Thiết kế này yếu hơn native split; không gọi hai post đăng nối tiếp là A/B causal sạch.
5. Hạn chế một thay đổi mỗi test. Không chạy test chồng trên cùng audience/slot. Không post cùng một creative nhiều lần chỉ để tạo đủ n; cần nhiều ý tưởng/đợt tương đương, tránh fatigue. Cửa sổ đo **7 ngày sau đăng là đề xuất vận hành**, owner xác nhận trước test và áp dụng hai arm như nhau; không suy ra từ Excel.

## Experiment cards

ER trong bảng là **ER đã xác nhận cho platform pilot**, đo cùng tuổi bài. Control là nội dung/quy trình hiện tại, không phải non-Entertainment.

| Test / recommendation | Hypothesis cần kiểm chứng | Treatment | Control | Primary KPI | Secondary KPI | Guardrails |
| --- | --- | --- | --- | --- | --- | --- |
| E1 / R3 — Caption | Một câu hỏi mời phản hồi có thể cải thiện ER Entertainment | Thêm đúng một câu hỏi liên quan ở cuối caption | Caption hiện tại, không thêm câu hỏi | ER | Engagement và comment trên publication; Views/Impressions | Exposure không giảm vượt dung sai; hide/report/unfollow nếu có; chất lượng comment/spam |
| E2 / R4 — Format | Gói trình bày khác có thể thay đổi ER | Image từ cùng ý tưởng/story | Video cùng ý tưởng/story | ER | Engagement, Views/Impressions trên publication | Exposure; cost/effort sản xuất; không đổi thông điệp/offer |
| E3 / R5 — Product Promotion | Caption theo tình huống sử dụng có thể tăng ER | Thay một đoạn bằng tình huống sử dụng cụ thể | Caption hiện tại | ER | Engagement, Views/Impressions; Clicks/CTR nếu coverage tương đương | Exposure, thông tin sản phẩm; action KPI không giảm vượt dung sai nếu được chọn |
| E4 / R6 — Timing, deferred | Hai slot có kết quả khác nhau trong điều kiện cố định | Slot B, owner chọn và ghi timezone | Slot A hiện tại | ER | Engagement, Views/Impressions | Exposure; weekday cân bằng, không tăng tần suất; audience overlap |
| E5 / R7 — Hashtag, deferred | Một tag liên quan có thể thay đổi ER | Bộ tag hiện tại + một tag đã chọn trước | Bộ tag hiện tại | ER | Engagement, Views/Impressions; Clicks/CTR nếu đo đủ | Exposure; không đổi topic/category; không thêm tag không liên quan |

Với E2, effect được ước lượng cho **gói chuyển định dạng**, không tách được format khỏi cách creative được chuyển thể. E4/E5 chỉ kích hoạt sau high-priority work và một hypothesis vận hành cụ thể; dữ liệu lịch sử chưa đủ để ưu tiên chúng.

Các guardrail hide/report/unfollow, chất lượng comment, chi phí và assignment **chưa có trong dataset**. Phải thu thập mới hoặc ghi rõ không đo được. Không biến missing thành 0. Click/CTR không là primary cho pilot chung: lịch sử thiếu 66,79%; chỉ dùng khi hai arm đo được cùng định nghĩa và coverage tương đương.

## Sample và thời gian

- Chọn trước mức cải thiện tối thiểu có ý nghĩa thực tiễn `δ_min` (pp ER) và các dung sai guardrail `τ`. Marketing Owner và Analyst chốt dựa trên mục tiêu, nguồn lực và trade-off; **không đặt target giả** hay dùng gap 9,21 pp làm δ.
- Cần variance ở đúng cấp randomization, baseline mới, throughput publication và mức phụ thuộc audience. File lịch sử chưa đủ để chốt n/duration cho test causal: công thức rate/grain chưa rõ và creative/audience ID thiếu.
- Với **hai arm độc lập ở cấp publication**, ước lượng sơ bộ mỗi arm: `n ≈ 2 × (z_(1−α/2) + z_(power))² × σ² / δ_min²`; σ và δ cùng đơn vị pp. Có thể dùng α=0,05 và power=80% như lựa chọn thiết kế, không phải KPI target. Nếu randomize audience/cluster/paired slots, tính mẫu theo thiết kế đó và design effect; không lấy Views làm số quan sát độc lập cho ER cấp post.
- Pilot vận hành **2 tuần** để kiểm tra tracking và ước lượng variance; **4 tuần tuyển mẫu** cho test đầu là khung lịch dự kiến, chưa suy ra từ dữ liệu. Chỉ chốt lịch khi tính đủ n. Đảm bảo ngày trong tuần cân bằng; đợi hết cửa sổ đo bài cuối mới đọc kết quả.
- Nếu throughput không đáp ứng n trong khung đã chốt, ghi “inconclusive”, hoặc điều chỉnh thiết kế **trước** đợt test mới. n≥30 ở bước 3 là ngưỡng screening, không phải n đủ power. Không dừng sớm khi p-value/ER tạm thời thuận lợi.

## Validation và decision rules

Đăng ký trước primary KPI, estimand, unit, n, δ_min, τ, alpha, test end và phương pháp CI. Với post/slot design: estimate mean ER difference theo block/assignment, kèm median sensitivity; CI/permutation/bootstrap ở cấp unit/cluster thực tế, không coi repeated exposure là independent sample. Native A/B dùng estimator đúng thiết kế nền tảng và lưu định nghĩa. Một primary test tại một thời điểm; thêm arm/so nhiều segment cần kiểm soát multiple comparisons hoặc ghi exploratory.

| Quyết định | Rule sau khi dữ liệu đã mature |
| --- | --- |
| Scale có giới hạn | Test hợp lệ, đủ n; lower bound CI của uplift ER vượt δ_min; guardrail không suy giảm vượt τ theo CI/phương pháp chốt trước. Chỉ mở rộng từng phần trong platform/audience/format đã test; không tự chuyển sang thị trường khác |
| Stop variant | Guardrail vi phạm mức dừng đã đăng ký hoặc upper bound CI của uplift ER dưới 0 sau test đủ mẫu; không tiếp tục rollout variant |
| Không scale | Upper bound CI dưới δ_min: chưa chứng minh lợi ích thực tiễn đủ lớn, kể cả uplift point estimate dương |
| Iterate / inconclusive | CI còn cắt δ_min, tracking/cell thiếu hoặc contamination cao: ghi uncertainty, không scale; sửa thiết kế cho đợt mới và đăng ký lại |

Review hàng tuần chỉ để kiểm tra quality và guardrail; kết luận efficacy tại thời điểm đã đăng ký. Các ngưỡng δ_min/τ chưa chốt nghĩa là kế hoạch **chưa đủ điều kiện quyết định scale**. Baseline lịch sử là context; **concurrent randomized control** là comparator chính để estimate uplift.

**Protocol artifact:** [Experiment registration template](artifacts/experiment_registration_template.csv). Các trường `TBD` là thiết kế cần owner chốt, không phải kết quả đã có.
