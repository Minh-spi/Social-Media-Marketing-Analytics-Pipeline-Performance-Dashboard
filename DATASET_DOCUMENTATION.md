# TÀI LIỆU MÔ TẢ DỮ LIỆU & TỪ ĐIỂN DỮ LIỆU (DATA DICTIONARY)
**Tập dữ liệu:** Social Media Content Performance Dataset  
**Tập tin nguồn:** `Social_Media_Content_Performance_Dataset.xlsx` (kèm bản sao `Social_Media_Content_Performance_Dataset.csv`)  
**Ngày lập tài liệu:** 2026-09-28  

---

## 1. TỔNG QUAN VỀ TẬP DỮ LIỆU (DATASET OVERVIEW)

### 1.1. Mục đích & Bối cảnh
Tập dữ liệu **Social Media Content Performance** ghi nhận chi tiết hiệu suất của các bài đăng truyền thông số đa nền tảng (TikTok, Instagram, YouTube, X.com, LinkedIn, Facebook). Mục tiêu chính của tập dữ liệu là phục vụ việc:
- Phân tích tương tác (Engagement Analysis) theo nền tảng, định dạng bài đăng và danh mục nội dung.
- Đánh giá mức độ hiệu quả của nội dung tự nhiên (Organic) so với quảng cáo/tài trợ (Sponsored).
- Theo dõi các chỉ số chuyển đổi (Clicks, Click-Through Rate - CTR) và hiệu suất video/livestream.
- Tối ưu hóa thời gian đăng bài (Post Timing) và định vị nội dung theo vị trí địa lý (Region).
- Phân loại và xây dựng mô hình dự đoán mức độ tương tác (`Engagement_Level`).

### 1.2. Thống kê chung
- **Tổng số dòng (Records/Rows):** 5,600 dòng.
- **Tổng số cột (Columns/Features):** 24 cột.
- **Số bài đăng duy nhất (Unique Post_ID):** 5,000 bài (có 600 lượt lặp lại do bài đăng được phân phối đa nền tảng/thời điểm).
- **Khoảng thời gian (Date Range):** Từ `01/01/2024` đến `01/05/2025` (17 tháng).
- **Khung giờ đăng bài (Post Hour Range):** Từ `08:00` đến `19:00`.
- **Tình trạng giá trị khuyết (Missing Values):** Chỉ xuất hiện ở 2 cột `Clicks` và `Click_Through_Rate` (3,740 dòng null / 66.79% - đặc trưng cho các nền tảng/bài đăng không có liên kết điều hướng trực tiếp hoặc không phát sinh lượt click).

---

## 2. PHÂN NHÓM DỮ LIỆU (FEATURE GROUPING)

24 trường dữ liệu được phân chia thành 5 nhóm logic:

| Nhóm dữ liệu | Danh sách các cột | Mô tả |
| :--- | :--- | :--- |
| **1. Định danh & Phân loại nội dung** | `Post_ID`, `Platform`, `Content_Type`, `Content_Category`, `Post_Type`, `Main_Hashtag` | Nhận diện bài đăng, nền tảng xuất bản, hình thức sở hữu, chủ đề và định dạng bài đăng. |
| **2. Thông tin Địa lý** | `Region`, `Longitude`, `Latitude` | Vùng quốc gia thị trường mục tiêu và tọa độ địa lý tương ứng. |
| **3. Thời gian đăng bài** | `Post_Published_At`, `Post_Date`, `Post_Hour` | Timestamp đầy đủ, ngày đăng bài và giờ xuất bản (8h - 19h). |
| **4. Chỉ số tương tác & Phân phối** | `Views`, `Impressions`, `Likes`, `Shares`, `Comments`, `Engagement`, `Engagement_Rate`, `Video_Views`, `Live_Stream_Views` | Các chỉ số đo lường mức độ lan tỏa và phản hồi của người xem. |
| **5. Chỉ số Chuyển đổi & Đánh giá** | `Clicks`, `Click_Through_Rate`, `Engagement_Level` | Số lượt nhấp, tỷ lệ nhấp chuột (CTR) và nhãn phân loại mức độ tương tác. |

---

## 3. TỪ ĐIỂN DỮ LIỆU CHI TIẾT (DATA DICTIONARY)

| STT | Tên cột (Column Name) | Kiểu dữ liệu (Data Type) | Giá trị khuyết (Nulls) | Mô tả ý nghĩa (Description) | Miền giá trị / Quy tắc tính toán / Ví dụ |
|:---:|:---|:---|:---:|:---|:---|
| 1 | `Post_ID` | String (Object) | 0 (0%) | Mã định danh duy nhất của nội dung bài đăng. | `Post_1`, `Post_2`, ..., `Post_5000` (5,000 mã duy nhất). |
| 2 | `Platform` | Categorical (String) | 0 (0%) | Nền tảng mạng xã hội đăng tải nội dung. | Gồm 6 nền tảng: `YouTube` (1,320), `TikTok` (1,257), `X.com` (1,201), `Instagram` (998), `LinkedIn` (525), `Facebook` (299). |
| 3 | `Content_Type` | Categorical (String) | 0 (0%) | Hình thức phân phối nội dung. | - `Organic`: Nội dung tự nhiên (4,646 - 82.96%)<br>- `Sponsored`: Nội dung quảng cáo/tài trợ (954 - 17.04%). |
| 4 | `Content_Category` | Categorical (String) | 0 (0%) | Danh mục / Mục đích truyền thông của bài viết. | - `Educational`: Kiến thức, giáo dục (2,026)<br>- `Product Promotion`: Quảng bá sản phẩm (1,385)<br>- `Entertainment`: Giải trí (877)<br>- `Customer Story`: Câu chuyện khách hàng (735)<br>- `Event / Webinar`: Sự kiện, hội thảo (577). |
| 5 | `Post_Type` | Categorical (String) | 0 (0%) | Định dạng thể hiện của bài đăng. | Gồm 7 loại: `Video` (2,948), `Image` (996), `Live Stream` (924), `Text` (458), `Article` (207), `Carousel` (51), `PDF` (16). |
| 6 | `Region` | Categorical (String) | 0 (0%) | Quốc gia / Thị trường phát hành bài viết. | 8 quốc gia: `USA` (752), `Canada` (735), `UK` (732), `Brazil` (718), `India` (691), `Australia` (679), `Japan` (666), `Germany` (627). |
| 7 | `Longitude` | Float | 0 (0%) | Kinh độ trung tâm của vùng/quốc gia. | Tương ứng theo `Region` (ví dụ: USA: `-95.7129`, UK: `-3.4360`, India: `78.9629`). |
| 8 | `Latitude` | Float | 0 (0%) | Vĩ độ trung tâm của vùng/quốc gia. | Tương ứng theo `Region` (ví dụ: USA: `37.0902`, UK: `55.3781`, India: `20.5937`). |
| 9 | `Engagement` | Integer | 0 (0%) | Tổng số lượt tương tác tổng hợp ghi nhận được trên bài đăng. | Min: 73 \| Max: 1,032,271 \| Mean: ~115,445. |
| 10 | `Views` | Integer | 0 (0%) | Số lượt xem thực tế bài đăng. | Min: 1,000 \| Max: 4,430,104 \| Mean: ~858,263. |
| 11 | `Likes` | Integer | 0 (0%) | Số lượt yêu thích / thả tim (Likes/Reactions). | Min: 101 \| Max: 981,669 \| Mean: ~150,720. |
| 12 | `Shares` | Integer | 0 (0%) | Số lượt chia sẻ / đăng lại (Shares/Retweets). | Min: 32 \| Max: 304,982 \| Mean: ~47,685. |
| 13 | `Comments` | Integer | 0 (0%) | Số lượt bình luận / thảo luận. | Min: 20 \| Max: 232,658 \| Mean: ~34,515. |
| 14 | `Engagement_Rate` | Float | 0 (0%) | Tỷ lệ tương tác trên tổng số lượt xem. | Công thức: $\text{Engagement\_Rate} = \frac{\text{Engagement}}{\text{Views}}$.<br>Min: 0.0500 (5.0%) \| Max: 0.2693 (26.93%) \| Mean: 0.1528 (15.28%). |
| 15 | `Impressions` | Integer | 0 (0%) | Số lần hiển thị của bài đăng trên màn hình người dùng. | Min: 1,125 \| Max: 5,282,874 \| Mean: ~1,029,742. ($\text{Impressions} \ge \text{Views}$). |
| 16 | `Video_Views` | Integer | 0 (0%) | Số lượt xem riêng cho định dạng Video (bằng 0 nếu không phải video). | Min: 0 \| Max: 5,474,756 \| Mean: ~640,968. |
| 17 | `Live_Stream_Views` | Integer | 0 (0%) | Số lượt xem phát trực tiếp (bằng 0 nếu không phải livestream). | Min: 0 \| Max: 1,998,724 \| Mean: ~98,092. |
| 18 | `Clicks` | Float / Integer | 3,740 (66.79%) | Số lượt nhấp chuột vào liên kết hoặc nội dung bài đăng. | Có dữ liệu trên 1,860 dòng (TikTok, LinkedIn, Facebook).<br>Min: 12 \| Max: 134,139 \| Mean: ~19,036. |
| 19 | `Click_Through_Rate` | Float | 3,740 (66.79%) | Tỷ lệ nhấp chuột trên tổng số lượt hiển thị (CTR). | Công thức: $\text{CTR} = \frac{\text{Clicks}}{\text{Impressions}}$.<br>Min: 0.0100 (1.0%) \| Max: 0.0300 (3.0%) \| Mean: 0.0184 (1.84%). |
| 20 | `Main_Hashtag` | Categorical (String) | 0 (0%) | Thẻ hashtag chủ đạo đính kèm bài viết. | 18 Hashtags: `#SuccessStory` (1,523), `#CustomerStory` (1,005), `#ProductDemo` (927), `#TrendingNow` (535), `#EventRecap` (365), `#FeatureHighlight` (354), `#FunContent` (299), `#WebinarReplay` (170), `#DidYouKnow` (124), ... |
| 21 | `Post_Published_At` | Datetime (`YYYY-MM-DD HH:MM:SS`) | 0 (0%) | Thời điểm xuất bản bài đăng chính xác đến phút. | Từ `2024-01-01 10:18:00` đến `2025-05-01 17:08:00`. |
| 22 | `Post_Date` | Date (`YYYY-MM-DD`) | 0 (0%) | Ngày xuất bản bài viết (trích xuất từ `Post_Published_At`). | Từ `2024-01-01` đến `2025-05-01`. |
| 23 | `Post_Hour` | Integer | 0 (0%) | Khung giờ xuất bản bài đăng (trích xuất từ `Post_Published_At`). | Các giá trị nguyên từ `8` đến `19` (8h sáng đến 7h tối). |
| 24 | `Engagement_Level` | Categorical (String) | 0 (0%) | Mức độ phân loại tương tác của bài viết. | - `Low` (1,170 dòng): Khi $\text{Engagement\_Rate} < 0.10$ (10%).<br>- `Medium` (3,110 dòng): Khi $0.10 \le \text{Engagement\_Rate} < 0.20$ (10% - 20%).<br>- `High` (1,320 dòng): Khi $\text{Engagement\_Rate} \ge 0.20$ (20% trở lên). |

---

## 4. QUY TẮC NGHIỆP VỤ & QUAN HỆ TOÁN HỌC (BUSINESS RULES & FORMULAS)

1. **Quan hệ hiển thị và lượt xem:**
   $$\text{Impressions} \ge \text{Views} \ge \text{Video\_Views} / \text{Live\_Stream\_Views}$$
2. **Công thức Tỷ lệ tương tác (Engagement Rate):**
   $$\text{Engagement\_Rate} = \frac{\text{Engagement}}{\text{Views}}$$
3. **Công thức Tỷ lệ nhấp chuột (Click Through Rate - CTR):**
   $$\text{Click\_Through\_Rate} = \frac{\text{Clicks}}{\text{Impressions}}$$
4. **Phân cấp Engagement Level:**
   $$\text{Engagement\_Level} = \begin{cases} \text{Low} & \text{khi } \text{Engagement\_Rate} < 10\% \\ \text{Medium} & \text{khi } 10\% \le \text{Engagement\_Rate} < 20\% \\ \text{High} & \text{khi } \text{Engagement\_Rate} \ge 20\% \end{cases}$$
5. **Xử lý Missing Data:**
   - Cột `Clicks` và `Click_Through_Rate` chứa `NaN` ở các bài đăng không có URL/CTA nhấp chuột. Khi phân tích tương tác thông thường, không cần loại bỏ các dòng này; khi phân tích chuyển đổi (Conversion/CTR), lọc các dòng `Clicks IS NOT NULL`.

---

## 5. HƯỚNG DẪN ỨNG DỤNG PHÂN TÍCH (ANALYTICS USE CASES)
- **Dashboarding / Trực quan hóa (Tableau/Power BI):** Sử dụng các chiều phân tích `Platform`, `Post_Type`, `Region`, `Content_Category`, `Post_Hour` kết hợp với các chỉ số đo lường `Views`, `Engagement`, `Engagement_Rate`, `Clicks`.
- **Mô hình học máy (Machine Learning):**
  - *Classification:* Dự đoán `Engagement_Level` (Low/Medium/High) từ các đặc trưng bài viết trước khi đăng (Platform, Category, Post Type, Post Hour, Region, Main Hashtag).
  - *Regression:* Dự đoán số lượng `Views` hoặc `Engagement_Rate`.
