# Social Media Marketing Analytics Pipeline & Performance Dashboard

Portfolio project phân tích hiệu suất nội dung social media: bối cảnh → xác định vấn đề → kiểm tra driver → thiết kế hành động và experiment → dashboard Dash.

| Bước | Tài liệu |
| --- | --- |
| 1. Hiểu bối cảnh | [Business understanding](1.%20Hiểu%20bối%20cảnh/README.md) |
| 2. Xác định vấn đề | [Baseline & problem detection](2.%20Xác%20định%20vấn%20đề/README.md) |
| 3. Phân tích nguyên nhân | [Driver analysis & limitations](3.%20Phân%20tích%20nguyên%20nhân/README.md) |
| 4. Đưa giải pháp | [Recommendations & validation plan](4.%20Đưa%20giải%20pháp/README.md) |
| 5. Dashboard / Data App | [Dash app](5.%20Dashboard/README.md) |

Các finding là observational; residual không phải causal effect. Source ER/CTR chưa xác nhận công thức, không có official KPI target. Kế hoạch experiment chưa phải kết quả test đã chạy.

## Môi trường riêng

Sử dụng **Python 3.12**. `.venv` nằm tại project root và không dùng global site-packages. Từ project root trên Windows PowerShell:

```powershell
python -m venv .venv
& ".venv/Scripts/python.exe" -m pip install -r requirements.txt
& ".venv/Scripts/python.exe" -m pip check
```

Trên máy hiện tại `.venv` đã được tạo; không cần tạo lại nếu folder vẫn tồn tại. Cần cài thành công dependencies trước khi chạy app/notebook. Luôn gọi interpreter `.venv` như trên để tránh dùng Python global; không bắt buộc activate hoặc đổi Execution Policy.

Nếu muốn activate:

```powershell
.\.venv\Scripts\Activate.ps1
```

Nếu PowerShell chặn activation, dùng trực tiếp `.venv/Scripts/python.exe` thay vì thay đổi policy.

Trên macOS/Linux, sau khi clone:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python "5. Dashboard/app.py"
```

## Chạy dashboard và notebook

Cách nhanh: launcher tự kiểm tra dependencies, cài vào `.venv` nếu thiếu, rồi chạy app. Không dùng packages global và không cần activate:

```powershell
python run_dashboard.py
```

Nếu pip thất bại, launcher hiển thị lỗi và dừng; không coi dependencies đã cài. `python run_dashboard.py --check` chỉ kiểm tra, không cài hoặc chạy server.

```powershell
& ".venv/Scripts/python.exe" "5. Dashboard/app.py"
& ".venv/Scripts/python.exe" -m unittest discover -s "5. Dashboard/tests" -v
& ".venv/Scripts/python.exe" -m jupyterlab
```

Dashboard: **http://127.0.0.1:8050**. App đọc trực tiếp artifacts bước 2–4. JupyterLab chạy từ project root; trong VS Code chọn `.venv/Scripts/python.exe` làm interpreter/kernel. Nếu cần tên kernel riêng, đăng ký **bên trong venv**, không ghi vào global/user kernel:

```powershell
& ".venv/Scripts/python.exe" -m ipykernel install --sys-prefix --name social-media-analytics --display-name "Social Media Analytics (.venv)"
```

Dependencies app/phân tích ở [requirements.txt](requirements.txt); dependencies app tối thiểu ở [dashboard requirements](5.%20Dashboard/requirements.txt). JupyterLab và kernel được tách vào [requirements-notebooks.txt](requirements-notebooks.txt): `python -m pip install -r requirements-notebooks.txt` bằng interpreter venv. Các phiên bản scientific packages được chọn theo môi trường đã dùng để tạo output; dependency ranges chưa phải lock toàn bộ transitive dependencies.

Windows có thể báo đường dẫn quá dài khi cài JupyterLab vào folder project này. Dashboard không cần JupyterLab. Có thể dùng VS Code với kernel `.venv` để làm notebook; launcher chỉ cài dependencies dashboard, không cài JupyterLab.

## Đưa lên GitHub

Commit code, `requirements.txt`, Markdown, notebooks và artifacts cần cho app. **Không commit `.venv`**, `.deps`, cache hoặc `.env`: root `.gitignore` đã loại các file này. Máy clone mới phải tạo venv và cài requirements; không copy venv giữa máy.

Repository hiện chưa được khởi tạo Git và chưa được push. `.gitignore` giữ datasets/artifacts cần cho dashboard chạy từ clone.

Nếu cần snapshot dependency chính xác, chỉ tạo sau khi cài thành công và `pip check` pass:

```powershell
& ".venv/Scripts/python.exe" -m pip freeze > requirements-lock.txt
```

Không tạo lock từ môi trường cài thiếu packages. Xem [environment status](ENVIRONMENT.md) cho trạng thái cài đặt trên máy hiện tại.
