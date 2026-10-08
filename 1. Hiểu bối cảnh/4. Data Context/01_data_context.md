# Data Context

## Data scope và grain / unit of analysis

Nguồn trực tiếp: `data/Social_Media_Content_Performance_Dataset.xlsx`, sheet `Sheet1`, **5.600 dòng × 24 cột** (không tính header). Các kiểm tra không sửa hoặc loại record trong dữ liệu gốc.

Một record ghi nhận metadata và performance của bài đăng gắn với platform, region và thời điểm xuất bản. Đây là dữ liệu tổng hợp cấp record bài đăng, không phải sự kiện tương tác hay người dùng. Chưa có tài liệu xác nhận grain nghiệp vụ hoặc cửa sổ đo performance.

Có **5.000 Post_ID duy nhất**, **600 lượt lặp vượt lần xuất hiện đầu tiên**. Khóa ứng viên `Post_ID + Platform + Post_Published_At` vẫn có **21 lượt lặp**. Không suy ra mã lặp là cross-post, snapshot hay lỗi nhập liệu; chưa xác nhận khóa duy nhất.

## Dimension–metric mapping

| Nhóm | Trường | Vai trò |
| --- | --- | --- |
| Identifier | Post_ID | Mã bài; không duy nhất trong file |
| Channel / distribution | Platform, Content_Type | Nền tảng; Organic/Sponsored |
| Content | Content_Category, Post_Type, Main_Hashtag | Chủ đề, định dạng, hashtag chính |
| Geography | Region, Longitude, Latitude | Nhãn địa lý và tọa độ; chưa rõ là nơi người xem hay thị trường targeting |
| Time | Post_Published_At, Post_Date, Post_Hour | Timestamp, ngày, giờ đăng; không có timezone |
| Exposure metrics | Views, Impressions, Video_Views, Live_Stream_Views | Số lượng hiển thị/xem |
| Engagement metrics | Likes, Shares, Comments, Engagement, Engagement_Rate | Tương tác và rate nguồn cung cấp |
| Action metrics | Clicks, Click_Through_Rate | Click và rate nguồn cung cấp |
| Performance label | Engagement_Level | Nhãn kết quả; không phải dimension lập kế hoạch trước đăng |

Mapping bao gồm đủ 24 cột. Tọa độ và giờ là dimension dù có kiểu số; Engagement_Level là nhãn phân loại, không phải metric số.

## Coverage

| Thuộc tính | Phạm vi quan sát |
| --- | --- |
| Ngày đăng | 2024-01-01 đến 2025-05-01; chưa có đầy đủ tháng 05/2025 |
| Timestamp | 2024-01-01 10:18:00 đến 2025-05-01 17:08:00 |
| Giờ đăng | 8–19; chưa rõ timezone |
| Platform (6) | Facebook, Instagram, LinkedIn, TikTok, X.com, YouTube |
| Region (8) | Australia, Brazil, Canada, Germany, India, Japan, UK, USA |
| Content category (5) | Customer Story, Educational, Entertainment, Event / Webinar, Product Promotion |
| Post type (7) | Article, Carousel, Image, Live Stream, PDF, Text, Video |
| Content type (2) | Organic, Sponsored |
| Engagement label (3) | High, Low, Medium |

Khoảng ngày và tập giá trị không chứng minh dữ liệu đầy đủ ở mọi ngày hoặc mọi tổ hợp dimension. Excel rộng hơn brief về thời gian và nền tảng.

## Missing value và duplicate cơ bản

| Kiểm tra | Kết quả |
| --- | --- |
| Clicks | 3.740 missing / 5.600 record (66,79%) |
| Click_Through_Rate | 3.740 missing / 5.600 record (66,79%); cùng record với Clicks |
| 22 cột còn lại | Không có missing theo kiểm tra null bằng pandas |
| Duplicate toàn bộ 24 cột | 0 lượt lặp vượt lần đầu |
| Duplicate Post_ID | 600 lượt lặp vượt lần đầu |

| Platform | Record có Clicks / tổng record |
| --- | --- |
| Facebook | 299 / 299 |
| Instagram | 0 / 998 |
| LinkedIn | 304 / 525 |
| TikTok | 1.257 / 1.257 |
| X.com | 0 / 1.201 |
| YouTube | 0 / 1.320 |

Đây là độ bao phủ dữ liệu, không phải bảng hiệu suất kênh. Chưa có lý do nghiệp vụ cho missing; missing không đồng nghĩa zero click, không có link hoặc không có khả năng click. Kiểm tra null chưa bao gồm kiểm toán đầy đủ giá trị không hợp lệ.

## Limitation và giới hạn kết luận

**Thông tin business không có:** tên doanh nghiệp/sản phẩm, account/campaign ID, ngân sách/chi phí, doanh thu, đơn hàng, lead, conversion sau click, unique reach, follower base, chân dung người xem, caption/creative, nội dung bình luận, toàn bộ hashtag, timezone, thời điểm trích xuất, cửa sổ đo lường, nguồn thu thập chi tiết, công thức KPI, quy tắc nhãn và target/benchmark.

**Dataset hỗ trợ:** mô tả cơ cấu và kết quả ghi nhận theo kênh, nội dung, hình thức phân phối, thời điểm đăng và nhãn địa lý; nghiên cứu khác biệt hoặc liên hệ quan sát ở bước sau khi xác nhận grain và định nghĩa metric. Click/CTR chỉ có thể xét trên phần được ghi nhận.

**Dataset không đủ để kết luận:** nguyên nhân performance, tác động gia tăng của Sponsored, hiệu quả chi phí/ROI/ROAS, chuyển đổi mua hàng, người dùng duy nhất, hành trình funnel, sentiment, hoặc khả năng khái quát sang thị trường/thời gian ngoài mẫu. Khác biệt quan sát không chứng minh nhân quả hay lựa chọn tối ưu.

**Nguồn tái lập:** [Notebook đọc trực tiếp Excel](02_excel_context_checks.ipynb). Notebook cũ trong folder được giữ nguyên và không dùng làm căn cứ cho tài liệu này.
