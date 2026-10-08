# Measurement & Action Plan

## Measurement framework

| Tầng | KPI / check | Cách dùng |
| --- | --- | --- |
| Leading — thực thi | Số unit đã assign/publish/mature, balance giữa arm/block, completeness tracking | Đánh giá test có triển khai đúng và đủ mẫu; không phải thành công marketing |
| Leading — chất lượng đo | KPI contract, unique publication key, cùng cửa sổ đo/timezone; coverage Click/CTR | Điều kiện hợp lệ; dữ liệu thiếu không được gán 0 |
| Outcome chính — Engagement | ER xác nhận: mean giữa arm; median sensitivity | Difference pp và relative uplift `(ER_T−ER_C)/ER_C`; nếu control=0 thì chỉ báo pp. Không tổng hợp rate bằng công thức chưa xác nhận |
| Outcome hỗ trợ | Engagement, Views, Impressions trên unit/publication | Đọc cùng số unit, total và mean/median; không cộng Views với Video_Views hoặc coi Views là unique reach |
| Outcome Action — nếu đủ dữ liệu | Clicks/CTR | Chỉ đối chiếu hai arm khi định nghĩa/cửa sổ/coverage tương đương; không suy ra lead/sales |
| Guardrails | Exposure trên unit, negative feedback/comment quality, cost/effort nếu thu thập được | Tránh tăng ER bằng cách giảm Views mạnh hoặc tạo phản hồi chất lượng thấp; dung sai phải đăng ký |

Trong dữ liệu lịch sử, Exposure là tầng đứng trước Engagement trong flow. Trong test, Views/Impressions cũng là outcome/guardrail sau triển khai; không coi chúng là leading indicator dự báo ER.

### Success criteria

- R1 thành công khi owner ký xác nhận metric contract, Analyst kiểm tra export mới và unit/window giữa arm đối chiếu được; không yêu cầu uplift.
- R2 thành công khi mục tiêu category và primary KPI được xác nhận, baseline cùng segment/window được lập; không tự gán business target.
- R3–R7 thành công để mở rộng khi đạt rule scale của [experiment plan](03_experiment_plan.md). Gap lịch sử, mean ER category khác hoặc point uplift đơn lẻ không phải tiêu chuẩn scale.
- Nếu measurement contract mới khác source ER lịch sử, thiết lập baseline mới và ghi break về định nghĩa; không nối chuỗi hoặc sửa dataset bước 1/2/3.

## Action roadmap

Các mốc sau là **đề xuất lịch vận hành** tính từ kickoff, không phải lịch đã phê duyệt hoặc thời gian suy ra từ dataset.

| Giai đoạn | Việc triển khai | Vai trò accountable / supporting | Review và exit gate |
| --- | --- | --- | --- |
| Kickoff, tuần 1–2 | R1 metric contract; R2 mục tiêu category; kiểm tra capability A/B, export và timezone | Marketing Owner / Analyst + Channel Owner | Review hai lần/tuần; contract + objective + tracking thống nhất |
| Readiness pilot, khoảng 2 tuần tiếp | Chuẩn bị E1 control/treatment; thử logging; chốt variance, n, δ_min, τ và window | Analyst / Content Lead + Experiment/Channel Owner | Review hàng tuần; protocol hoàn chỉnh, randomization vận hành được |
| E1, khung tuyển mẫu dự kiến 4 tuần | Randomize và ghi assignment; giữ yếu tố khác cố định/cân bằng | Experiment/Channel Owner / Content Lead + Analyst | Quality/guardrail hàng tuần; không đổi test để chạy theo interim uplift |
| Readout sau maturity | Estimate uplift/CI, volume và guardrail; scale/stop/iterate | Marketing Owner / Analyst | Một readout sau bài cuối hết cửa sổ; lưu kết quả cả khi không thắng |
| Đợt tiếp theo, chưa chốt ngày | E2 nếu nguồn lực và câu hỏi format còn quan trọng; E3 riêng cho Product Promotion | Content Lead / Analyst + Channel Owner | Protocol riêng; không chồng test lên cùng audience |
| Deferred | E4/E5 chỉ sau các gate và hypothesis mới | Marketing Owner / Analyst | Không đổi lịch/tag hàng loạt từ ranking lịch sử |

## Sau test và khi mở rộng

Scale từng đợt trong phạm vi đã test, giữ nhóm holdout nếu capability cho phép. Review weekly với cùng window, theo dõi ER cùng Engagement và exposure; monthly review vai trò category và bằng chứng tích lũy. Mức mở rộng và cadence theo volume thực, chưa có cơ sở chọn tỷ lệ ngân sách hay tỷ lệ traffic cụ thể.

Dừng mở rộng khi guardrail vi phạm mức đã chốt, tracking mất khả năng đối chiếu hoặc effect không duy trì theo tiêu chuẩn đăng ký. Owner quyết định stop/iterate theo readout; Analyst lưu version, cohort, coverage và uncertainty. Không giải thích mọi thay đổi sau rollout là causal nếu không có control phù hợp.

## Dữ liệu mới cần ghi

Lưu trong **khu vực experiment mới**, chưa ghi vào raw/analysis-ready cũ: experiment ID, arm, assignment unit, block, creative/caption version, category/objective, platform, post type, audience/region targeting, toàn bộ hashtag, timezone, publish/measure timestamp, window, spend/effort nếu có, metric definition version và guardrails. Không có dữ liệu thử nghiệm được giả lập trong bước 4.

**Nguồn và liên kết:** [Recommendations](01_opportunities_and_recommendations.md), [Priority](02_prioritization.md), [Validation rules](03_experiment_plan.md).
