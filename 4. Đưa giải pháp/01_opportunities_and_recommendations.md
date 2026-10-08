# Opportunities & Recommendations

## Cơ sở hành động

Bước 3 ghi nhận Entertainment có mean source ER **7,51%** so với **16,72%** ở non-Entertainment trong 16 tháng trọn; gap **9,21 pp**. Gap chuẩn hóa vẫn **8,65 pp** trong Platform × Post Type đủ mẫu. Đây là tín hiệu ổn định để ưu tiên kiểm chứng, không phải bằng chứng Entertainment thất bại hoặc thay đổi nội dung sẽ tạo uplift tương đương.

## Opportunity list

| ID | Finding liên quan | Business relevance | Độ chắc chắn | Yếu tố có thể tác động / uncertainty |
| --- | --- | --- | --- | --- |
| O1 | Công thức ER, grain và cửa sổ đo chưa xác nhận | Tất cả quyết định cần KPI nhất quán | Cao về giới hạn dữ liệu | Định nghĩa đo lường, khóa publication, thời điểm thu thập; chưa biết gap có phản ánh cơ chế đo |
| O2 | Entertainment có volume Views đáng kể; không có target theo category | Content decision: xác định vai trò category | Cao về finding; mục tiêu chưa biết | Mục tiêu nội dung và baseline phù hợp; chưa thể coi ER thấp là không đạt mục tiêu |
| O3 | Category-associated residual còn trong segment tương đồng | Content execution | Cao về residual; thấp về cơ chế creative | Thử một biến thể caption; chưa có caption/creative để xác nhận driver |
| O4 | Post Type composition chỉ 0,213 pp trên subset; gap khác nhau giữa joint cell | Content / format decision | Trung bình về liên hệ; thấp về causal uplift | Test định dạng với cùng nội dung; không mặc định Image tốt hơn Video |
| O5 | Product Promotion còn gap 3,17–6,97 pp trong 19 cell đủ mẫu | Secondary content decision | Cao về gap; thấp về cơ chế | Một thử nghiệm nội dung riêng, sau ưu tiên Entertainment |
| O6 | Timing mix giải thích rất ít; Platform × Hour chỉ bao phủ 15,18% Entertainment | Distribution decision | Yếu cho đổi lịch | Chỉ thử giờ khi có hypothesis vận hành mới và timezone rõ |
| O7 | Hashtag chỉ có 5,25% Entertainment đủ common support | Content / distribution decision | Không đủ để tách hashtag effect | Test một tag riêng; không chuyển tag từ category khác theo xếp hạng lịch sử |

## Recommendation set

Confidence dưới đây là mức tin cậy của **cơ sở hành động**, không phải xác suất tạo uplift. Direct action là công việc thiết lập/đo lường có thể bắt đầu ngay; test-first action chỉ được mở rộng sau validation.

| ID / loại | Action cụ thể | Evidence | Expected effect | Confidence | Risk / limitation |
| --- | --- | --- | --- | --- | --- |
| R1 — Direct action | Lập measurement contract cho một platform pilot: xác nhận ER numerator/denominator, unique publication ID, timezone, cửa sổ đo; kiểm tra export mới | O1; rate và grain chưa rõ | Giảm ambiguity, tạo baseline/test có thể đối chiếu; không cam kết tăng ER | Cao | Cần nguồn platform/owner xác nhận; không sửa hoặc tính lại file bước 1/2/3 |
| R2 — Direct action | Content Lead ghi mục tiêu chính của Entertainment và Product Promotion; Analyst lập baseline cùng category/platform/format, cùng cửa sổ đo | O2; chưa có target, Views và ER phản ánh tầng khác nhau | Đánh giá đúng mục tiêu; không lấy non-Entertainment làm target bắt buộc | Cao về nhu cầu làm rõ; mục tiêu cần owner xác nhận | Không tự gán Entertainment chỉ để awareness; ER vẫn được theo dõi |
| R3 — Test-first / E1 | Pilot Entertainment: thêm **một câu hỏi mời phản hồi** ở cuối caption; giữ creative/format và điều kiện phân phối tương đương control | O3; residual lớn, chưa xác định creative driver | Kiểm tra khả năng nâng ER; uplift cần experiment để estimate | Thấp về uplift; cao về tính phù hợp để test | Engagement chất lượng thấp, fatigue; không biết cơ chế creative hiện tại |
| R4 — Test-first / E2 | Sau E1, test cùng ý tưởng Entertainment dưới dạng Video và Image trên một platform hỗ trợ cả hai | O4; format mix giải thích ít, joint gap chưa mất | Estimate effect của gói định dạng, không giả định tăng | Thấp–trung bình về rationale; thấp về uplift | Creative phải thay đổi để chuyển format; effect là cả gói thể hiện, không thuần file type |
| R5 — Test-first / E3 | Pilot riêng Product Promotion: thay một đoạn caption giới thiệu bằng mô tả một tình huống sử dụng; giữ sản phẩm/offer/format | O5; secondary gap | Estimate uplift ER của biến thể nội dung; chưa đủ dự báo click/sales | Thấp về uplift | Không trộn với test Entertainment; giữ thông tin sản phẩm chính xác |
| R6 — Test-first, deferred / E4 | Chỉ khi có hypothesis mới, pilot hai slot giờ cùng timezone, cùng platform/format và ngày trong tuần cân bằng | O6; timing chưa giải thích gap | Estimate effect cục bộ của lịch đăng, không hứa uplift | Thấp | Chưa có timezone, audience overlap; không lấy giờ ER cao nhất làm “giờ tốt nhất” |
| R7 — Test-first, deferred / E5 | Nếu có đủ nguồn lực, test thêm một hashtag liên quan nội dung so với bộ tag hiện tại; giữ các thành phần khác | O7; thiếu common support | Estimate effect tag cục bộ; chưa biết chiều | Thấp | Tag × topic confounding; cần lưu toàn bộ tag và giữ category cố định |

**Chưa đủ evidence để scale:** thay tỷ trọng category, chuyển Views/ngân sách sang platform/region khác, tăng Sponsored, đổi lịch hàng loạt hoặc nhân rộng hashtag. Không xem mức ER của category khác là mức Entertainment chắc chắn có thể đạt.

**Nguồn:** [Root-cause summary](../3.%20Phân%20tích%20nguyên%20nhân/03_root_cause_summary.md), [driver effects](../3.%20Phân%20tích%20nguyên%20nhân/artifacts/tables/driver_effect_summary.csv). Kế hoạch dưới đây là đề xuất triển khai, chưa phải experiment đã chạy.
