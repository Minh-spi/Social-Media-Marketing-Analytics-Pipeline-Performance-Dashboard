# Measurement Context

## KPI framework

Exposure → Engagement → Action là các tầng quan sát phù hợp với brief. **Absolute metric** đo số lượng; **rate metric** biểu diễn tỷ lệ. Chưa có ngưỡng để kết luận thành công business.

| Business stage | Metric | Loại | Ý nghĩa |
| --- | --- | --- | --- |
| Exposure | Impressions | Absolute | Số lần hiển thị; không đồng nghĩa số người duy nhất |
| Exposure | Views | Absolute | Lượt xem nội dung được ghi nhận |
| Exposure | Video_Views | Absolute | Lượt xem video; cần đọc theo định dạng |
| Exposure | Live_Stream_Views | Absolute | Lượt xem livestream; cần đọc theo định dạng |
| Engagement | Likes | Absolute | Lượt thích |
| Engagement | Shares | Absolute | Lượt chia sẻ |
| Engagement | Comments | Absolute | Lượt bình luận; không cho biết sentiment |
| Engagement | Engagement | Absolute | Chỉ số tương tác tổng hợp do nguồn cung cấp; thành phần chưa xác nhận |
| Engagement | Engagement_Rate | Rate | Tỷ lệ tương tác do nguồn cung cấp; mẫu số/cách tính chưa xác nhận |
| Action | Clicks | Absolute | Lượt nhấp; không đồng nghĩa lead hoặc mua hàng |
| Action | Click_Through_Rate | Rate | Tỷ lệ nhấp do nguồn cung cấp; mẫu số/cách tính chưa xác nhận |

`Engagement_Level` là nhãn Low/Medium/High, không phải absolute/rate KPI hay target business. Nguồn chưa mô tả quy tắc gán nhãn.

## Target / benchmark và quy ước đọc KPI

- PDF và Excel không cung cấp KPI target, benchmark ngành hoặc ngưỡng thành công được doanh nghiệp phê duyệt.
- Trong Excel, `Engagement` không bằng `Likes + Shares + Comments` ở bất kỳ record nào. Không mặc định tổng này là định nghĩa Engagement.
- Rate nguồn không khớp hoàn toàn `Engagement / Views` và `Clicks / Impressions`. Kiểm tra này không xác nhận công thức, cũng không tự kết luận lỗi dữ liệu.
- Rate được lưu dưới dạng số thập phân; nhân 100 khi hiển thị phần trăm. Chưa tổng hợp rate khi định nghĩa và mẫu số chưa rõ.
- Không cộng Views với Video_Views/Live_Stream_Views, hoặc Engagement với các thành phần tương tác, khi chưa xác nhận khả năng chồng lặp.
- Click/CTR bị thiếu trên nhiều record; không chuyển missing thành 0 hoặc coi các kênh có độ bao phủ tương đương.

**Nguồn:** [Business brief](../../Social%20Media%20Marketing%20Performance%20Analytics.pdf); [Kiểm tra Excel](../Data%20Context/02_excel_context_checks.ipynb).
