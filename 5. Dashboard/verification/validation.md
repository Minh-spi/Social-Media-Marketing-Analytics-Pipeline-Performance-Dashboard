# Validation status

## Đã kiểm tra

- 11 data tests pass: baseline đối chiếu artifact; inclusive date + combined filters; reversed dates; empty scope; missing Clicks/CTR; clear filter; source rate aggregation; diagnostic monthly gaps; thiếu comparator; không mutate frame; missing file error.
- Hai phép aggregations chính lấy trực tiếp analysis-ready và khớp baseline/diagnostic artifacts trước đó; không sinh finding mới.
- Python sources được compile kiểm tra cú pháp. Local README/source links được kiểm tra.
- Snapshot SHA-256 trong `prior_outputs_sha256.json` dùng để xác nhận raw và bước 1–4 không thay đổi trong quá trình tạo app.

## Runtime kiểm chứng cập nhật

Dash/Plotly/pandas đã import thành công từ root `.venv`. Cả 15 test pass, không còn skip. `pip check`: No broken requirements found. Launcher `python run_dashboard.py --port 8050` khởi động server; GET live `http://127.0.0.1:8050/` trả 200.

4 Dash/HTTP tests đã pass: layout/assets/dependency endpoints; callback full/empty/missing comparator; missing-source layout; download whitelist. Browser responsiveness/visual rendering chưa xác nhận.

## Lệnh kiểm tra lại

```powershell
python -m pip install -r "5. Dashboard/requirements.txt"
python -m unittest discover -s "5. Dashboard/tests" -v
python "5. Dashboard/app.py"
```

Mở `http://127.0.0.1:8050`; kiểm tra visual rendering cả 4 tab trên desktop/mobile, filters/reset, KPI dropdown, recommendation filters và source links. Kiểm tra browser trực quan còn lại; không đồng nhất HTTP tests với visual validation.
