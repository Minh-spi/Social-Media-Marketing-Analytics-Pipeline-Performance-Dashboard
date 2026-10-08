# Validation status

## Đã kiểm tra

- 11 data tests pass: baseline đối chiếu artifact; inclusive date + combined filters; reversed dates; empty scope; missing Clicks/CTR; clear filter; source rate aggregation; diagnostic monthly gaps; thiếu comparator; không mutate frame; missing file error.
- Hai phép aggregations chính lấy trực tiếp analysis-ready và khớp baseline/diagnostic artifacts trước đó; không sinh finding mới.
- Python sources được compile kiểm tra cú pháp. Local README/source links được kiểm tra.
- Snapshot SHA-256 trong `prior_outputs_sha256.json` dùng để xác nhận raw và bước 1–4 không thay đổi trong quá trình tạo app.

## Runtime kiểm chứng cập nhật

Dash/Plotly/pandas đã import thành công từ root `.venv`. Sau redesign, cả 18 test pass, không còn skip. Thêm kiểm tra recommendation/experiment callback, local platform SVG assets và color mapping ở platform charts. Launcher preview khởi động server trên port 8051; live endpoints trả 200. Các 88 raw/output files trong snapshot giữ nguyên SHA-256.

4 Dash/HTTP tests đã pass: layout/assets/dependency endpoints; callback full/empty/missing comparator; missing-source layout; download whitelist. Browser responsiveness/visual rendering chưa xác nhận.

## Lệnh kiểm tra lại

```powershell
python -m pip install -r "5. Dashboard/requirements.txt"
python -m unittest discover -s "5. Dashboard/tests" -v
python "5. Dashboard/app.py"
```

Mở `http://127.0.0.1:8050`; kiểm tra visual rendering cả 4 tab trên desktop/mobile, filters/reset, KPI dropdown, recommendation filters và source links. Kiểm tra browser trực quan còn lại; không đồng nhất HTTP tests với visual validation.

Latest visual refresh: 18 tests pass. Live preview on port 8052 returned HTTP 200 for the page, Dash layout and visual.css; layout includes the new sidebar navigation. All 88 prior files retain their recorded hashes. Browser visual rendering remains unverified.
