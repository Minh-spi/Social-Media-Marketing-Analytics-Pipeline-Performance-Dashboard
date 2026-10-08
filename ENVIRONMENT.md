# Local environment status

- Interpreter dự kiến: Python 3.12, `.venv/Scripts/python.exe` tại project root.
- Venv được tạo với `include-system-site-packages = false`: không kế thừa packages global.
- Root requirements bao gồm dashboard và các dependencies dùng cho phân tích/notebook.
- `.venv`, `.deps`, cache và `.env` được ignore khi đưa lên GitHub.

**Venv đã tạo thành công**, dùng Python 3.12.5. Đã xác nhận `sys.prefix != sys.base_prefix` và global site-packages không nằm trong import path.

**Dashboard dependencies đã sẵn sàng:** Dash/Plotly/pandas import thành công; `pip check` không báo broken requirements. Cả 15 test dữ liệu/HTTP/callback pass. Launcher đã chạy server trên `http://127.0.0.1:8050/`; live HTTP trả 200.

Lần cài full dependencies bị lỗi đường dẫn dài ở static asset JupyterLab trên Windows. Đã tách JupyterLab vào `requirements-notebooks.txt`; launcher chỉ cài dashboard dependencies. JupyterLab runtime chưa kiểm tra; chưa tạo lock file hoặc đăng ký kernel riêng.

Chạy từ PowerShell của bạn tại project root:

```powershell
& ".venv/Scripts/python.exe" -m pip install -r requirements.txt
& ".venv/Scripts/python.exe" -m pip check
& ".venv/Scripts/python.exe" "5. Dashboard/app.py"
```
