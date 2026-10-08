# Recommendation Prioritization

Chấm 6 tiêu chí bằng trọng số bằng nhau, **1–3, cao hơn là thuận lợi hơn**. Đây là đánh giá lập kế hoạch, không phải estimated uplift, ngân sách được duyệt hoặc benchmark business.

| Tiêu chí | 1 | 2 | 3 |
| --- | --- | --- | --- |
| Expected impact | Lợi ích chưa rõ/hẹp | Test có thể giảm một uncertainty quan trọng | Điều kiện nền tảng cho đo lường/quyết định đúng |
| Evidence strength | Hypothesis chưa được hỗ trợ/thiếu overlap | Liên hệ mô tả, chưa causal | Giới hạn/finding ổn định trực tiếp đòi hỏi hành động tương ứng |
| Ease | Cần nhiều điều kiện/capability chưa rõ | Cần phối hợp hoặc biến thể creative | Công việc tài liệu/export trong quy trình hiện có |
| Cost / effort | Nhiều phiên bản/nguồn lực test | Công sức vừa phải, chưa có cost thực | Công sức tương đối thấp |
| Risk | Coverage/định nghĩa/implementation uncertainty cao | Pilot có giới hạn rủi ro | Thiết lập/đo lường, không đổi phân phối |
| Business relevance | Không trực tiếp giải quyết trọng tâm | Liên quan secondary hoặc driver yếu | Trực tiếp phục vụ Entertainment / điều kiện đánh giá |

High ≥15; Medium 11–14; Low ≤10. Ease/cost là giả định về nguồn lực, cần owner cập nhật khi lập lịch; không có dữ liệu tiền để tính ROI. Expected impact ở đây là **giá trị quyết định**, không dự báo mức tăng KPI.

| ID | Impact | Evidence | Ease | Cost/effort | Risk | Relevance | Tổng | Priority | Dependency |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| R1 Measurement contract | 3 | 3 | 3 | 2 | 3 | 3 | 17 | High | Có owner/source export |
| R2 Objective + baseline | 3 | 3 | 3 | 3 | 3 | 3 | 18 | High | Owner xác nhận mục tiêu; R1 cho baseline mới |
| R3 Caption question pilot | 2 | 2 | 3 | 3 | 2 | 3 | 15 | High | R1/R2; experimental capability |
| R4 Format pilot | 2 | 2 | 2 | 1 | 2 | 3 | 12 | Medium | R1/R2; không chạy chồng E1 |
| R5 Product Promotion pilot | 2 | 2 | 2 | 2 | 2 | 2 | 12 | Medium | Entertainment ưu tiên trước |
| R6 Timing pilot | 1 | 1 | 2 | 2 | 1 | 2 | 9 | Low | Timezone và hypothesis mới; deferred |
| R7 Hashtag pilot | 1 | 1 | 2 | 2 | 1 | 2 | 9 | Low | Ghi đủ tag; hypothesis mới; deferred |

R3 được ưu tiên vì pilot hẹp, dễ triển khai và trực tiếp giảm uncertainty về content execution, **không phải vì caption được chứng minh là nguyên nhân**. R4/R5 chưa chạy đồng thời nếu nguồn lực pilot hạn chế. R6/R7 không phải việc cần làm ngay.

**Artifact:** [Recommendation matrix](artifacts/recommendation_matrix.csv). Chi tiết action/evidence tại [recommendations](01_opportunities_and_recommendations.md); điều kiện scale tại [experiment plan](03_experiment_plan.md).
