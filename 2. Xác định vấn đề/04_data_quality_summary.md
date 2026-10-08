# Data quality summary

Nguồn: Excel raw, sheet Sheet1. File analysis-ready là CSV UTF-8 riêng; không ghi đè raw. Đơn vị phân tích là record nguồn, không phải unique post đã xác nhận.

| Hạng mục | Rule xử lý |
| --- | --- |
| Data type | Parse date/numeric; dừng nếu chuyển kiểu làm mất giá trị. String giữ nguyên label; count nullable. Khi đọc CSV, parse lại date theo notebook. |
| Missing | Giữ nguyên null; không fill 0. Click/CTR chỉ tính trên record hợp lệ có dữ liệu; luôn kèm coverage. |
| Duplicate | Giữ nguyên record và thêm cờ mã/khóa lặp; chưa có cơ sở chọn record đại diện. Source_Row định vị dòng Excel, không thay cho business key. |
| KPI bất hợp lý | Gắn cờ count âm, không hữu hạn, không nguyên và rate ngoài [0,1]. Chỉ mask KPI tương ứng trong phân tích; không xóa dòng. Miền rate là rule kiểm tra, không xác nhận công thức. |
| Quan hệ KPI | Không sửa Engagement theo tổng Likes/Shares/Comments hoặc tính lại rate. Chênh lệch giữa các chỉ số được ghi nhận là định nghĩa chưa rõ. |
| Outlier | Không winsorize/cắt/drop; dùng cả trung bình và median để đọc phân phối. |
| Format | Tên cột và label nguồn giữ nguyên; thêm Month, Weekday, Partial_Month và các cờ kiểm tra. |
| Time | Tháng cuối chỉ đến 01/05/2025 được đánh dấu partial; không so total tháng này với tháng trọn. Performance gắn với ngày đăng, không phải ngày phát sinh tương tác. |

Raw: **5,600 dòng, 24 cột**; analysis-ready: **5,600 dòng, 41 cột**. Số dòng bị xóa: **0**; missing bị fill: **0**; số lỗi chuyển kiểu: **0**.

| field              | check                                              |   records |
|:-------------------|:---------------------------------------------------|----------:|
| Engagement         | nonnegative finite integer count                   |         0 |
| Views              | nonnegative finite integer count                   |         0 |
| Likes              | nonnegative finite integer count                   |         0 |
| Shares             | nonnegative finite integer count                   |         0 |
| Comments           | nonnegative finite integer count                   |         0 |
| Impressions        | nonnegative finite integer count                   |         0 |
| Video_Views        | nonnegative finite integer count                   |         0 |
| Live_Stream_Views  | nonnegative finite integer count                   |         0 |
| Clicks             | nonnegative finite integer count                   |         0 |
| Engagement_Rate    | finite decimal within [0, 1]; screening convention |         0 |
| Click_Through_Rate | finite decimal within [0, 1]; screening convention |         0 |
| all raw columns    | exact duplicate beyond first                       |         0 |
| Post_ID            | duplicate beyond first                             |       600 |
| candidate key      | duplicate beyond first                             |        21 |
| Post_Date          | timestamp/date mismatch                            |         0 |
| Post_Hour          | timestamp/hour mismatch                            |         0 |
| Post_Hour          | outside [0, 23]                                    |         0 |
| Longitude          | outside [-180, 180]                                |         0 |
| Latitude           | outside [-90, 90]                                  |         0 |
| dimensions         | whitespace-only label                              |         0 |
| columns            | duplicate column names                             |         0 |

Missing ở Clicks và Click_Through_Rate: 3.740 mỗi cột (66,79%); các cột raw còn lại không có null.

Grain, thời điểm trích xuất, cửa sổ đo KPI, timezone và công thức rate chưa xác nhận. Tổng absolute là tổng record trong file, chưa thể coi là lượng duy nhất của doanh nghiệp. Rate dùng mean/median nguồn ở cấp record, không phải rate tổng hợp có mẫu số xác nhận.

Các mã bài có thể khác category giữa record; không chọn category đầu tiên để đại diện. Kiểm tra độ nhạy dùng trọng số 1 / số record của Post_ID và vẫn giữ category của từng record.
