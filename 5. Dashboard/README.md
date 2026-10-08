# Social Media Marketing — Dashboard / Data App

Plotly Dash app trình bày và khám phá kết quả bước 1–4. App chỉ đọc các artifact hiện có; không ghi dữ liệu, chạy lại pipeline, tạo model hoặc sinh root-cause/recommendation mới.

## Chạy từ project root

Requires **Python 3.10+**, Dash 3.x, Plotly 6.x, pandas 2.x. Flask và dependencies bổ trợ được cài qua Dash. Nên dùng môi trường riêng nằm trong folder dashboard:

```powershell
python -m venv "5. Dashboard/.venv"
& "5. Dashboard/.venv/Scripts/python.exe" -m pip install -r "5. Dashboard/requirements.txt"
& "5. Dashboard/.venv/Scripts/python.exe" "5. Dashboard/app.py"
```

Nếu interpreter hiện tại đã có dependencies:

```powershell
python "5. Dashboard/app.py"
```

Mở **http://127.0.0.1:8050**. Đổi port nếu cần:

```powershell
python "5. Dashboard/app.py" --port 8051
```

App bind localhost, debug tắt. Không cần Excel engine vì app đọc CSV/Markdown đã xuất. Path nguồn được xác định theo vị trí app, không phụ thuộc working directory. Không cần copy dataset. Restart app sau khi artifact nguồn được cập nhật bên ngoài app; cache chỉ đọc tồn tại trong process.

## Các trang

| Trang | Câu hỏi / chức năng |
| --- | --- |
| Overview | Bao nhiêu record, exposure, engagement và click được ghi nhận? 4 KPI chính, hàng supporting KPI/coverage; chọn KPI cho monthly trend |
| Performance Explorer | Volume/rate khác nhau thế nào giữa segment? Chọn dimension/KPI, chart và table có n/median/coverage |
| Problem Diagnosis | Gap Entertainment còn ở segment nào? Comparison theo Month/Platform/Post Type/Region/Content Type; heatmap interaction; saved evidence và summary bước 2/3 |
| Recommendations & Experiments | Hành động nào đã được đề xuất, mức ưu tiên và rule kiểm chứng? Filter priority/type; matrix, experiment registration, full experiment/measurement plan |

Filter chung: publication date, Platform, Region, Content Category, Post Type, Content Type. Clear dropdown = tất cả; Reset trả về toàn bộ scope. Overview/Performance/live Diagnosis cập nhật theo filter. Priority/type là filter riêng của recommendations.

**Phạm vi evidence:** saved driver decomposition, robustness và kế hoạch bước 4 giữ phạm vi gốc, không tự tính lại theo filter. Live diagnosis chỉ thực hiện lại phép group/mean/gap đã có để khám phá, loại `Partial_Month` và dùng n≥30 mỗi nhóm như bước 3. Không rerun decomposition, sensitivity, inference hoặc chấm lại recommendation. Category filter có thể loại comparator; khi thiếu support, app không hiển thị gap giả.

## Quy ước KPI

- Absolute metrics = tổng record của scope, chưa xác nhận unique-post/person grain.
- ER/CTR = **mean source rate × 100**, kèm valid n; table có median. Không dùng ratio of totals hoặc coi source formula đã xác nhận.
- Missing Clicks/CTR giữ missing; nếu toàn scope không có dữ liệu thì card/chart là N/A, không phải 0. Click coverage được thể hiện trong table.
- Mask `Invalid_<KPI>` giống bước 2, chỉ trong bản dữ liệu memory; không fill, deduplicate, recode category hoặc sửa nguồn.
- Monthly trend gắn với **ngày đăng**, không phải ngày phát sinh interaction. Tháng cuối partial và boundary date filter có thể làm giảm total; không tự diễn giải thành performance decline.
- Residual = association/diagnostic finding, không causal effect; không có official KPI target. Experiment fields TBD và guardrail chưa thu thập không phải kết quả thử nghiệm.

## Nguồn và cấu trúc

App đọc `analysis_ready.csv` và baseline/problem artifacts bước 2; tables/root-cause summary bước 3; recommendation matrix, experiment registration và kế hoạch Markdown bước 4. Footer cho tải artifact qua whitelist read-only. Folder bước được nhận diện bằng prefix `2.`, `3.`, `4.`; mỗi prefix phải có đúng một folder.

```text
5. Dashboard/
├── app.py                  # app factory, callback wiring, read-only source routes
├── pages/                  # overview / performance / diagnosis / recommendations
├── components/             # filters / cards & tables / charts
├── utils/data_loader.py    # artifact repository, filters, existing metric aggregation
├── assets/style.css        # base styling
assets/visual.css       # presentation layer: cards, navigation, filters
├── tests/test_app.py       # data checks and real Dash HTTP/callback smoke tests
├── verification/           # validation status and hashes of unchanged prior outputs
└── requirements.txt
```

Missing/invalid analysis source hiển thị error thay vì app crash; optional evidence thiếu được báo riêng. Không có fallback dataset giả. Data table có sort, search/filter và pagination. Layout responsive; mỗi trang chỉ có 1–2 chart chính.

## Kiểm tra

```powershell
python -m unittest discover -s "5. Dashboard/tests" -v
```

Nếu dùng venv, thay `python` bằng interpreter venv ở trên. HTTP/callback tests chỉ chạy khi Dash/Plotly thực sự được cài; skip không đồng nghĩa pass runtime.

**Trạng thái kiểm chứng cập nhật:** dependencies trong root `.venv` đã sẵn sàng; cả 18 data/Dash HTTP/callback tests pass. Launcher root `python run_dashboard.py` khởi động server. Chưa kiểm tra visual rendering bằng browser. Xem [verification report](verification/validation.md). Launcher chỉ cài dashboard requirements, tránh lỗi đường dẫn dài khi cài JupyterLab trên Windows.

## Visual design

Nền trắng, typography trung tính, sidebar navigation; Date/Platform hiện trực tiếp và các filter khác trong More filters. Các lựa chọn được nhắc lại bằng chips. KPI dùng số rút gọn, giá trị đầy đủ trong tooltip; coverage vẫn hiện trực tiếp.

Platform color mapping chỉ áp dụng cho biểu đồ phân Platform: Facebook blue, Instagram magenta, LinkedIn blue đậm, YouTube đỏ, TikTok cyan, X charcoal. Các icon SVG nhận diện được lưu cục bộ trong assets, không cần tải từ CDN. Logo/tên hỗ trợ phân biệt hai platform gần màu; tên platform luôn hiện cùng màu.

Các biểu đồ khác dùng neutral slate; so Entertainment/comparator dùng amber/xám để tránh nhầm với màu platform. Recommendations có cards theo priority và experiment selector; bảng đầy đủ và nguồn Markdown vẫn mở rộng được. CSS có layout cho desktop/tablet/mobile; resize chart khi chuyển trang.

App debug tắt: sau khi sửa Python cần dừng process cũ bằng Ctrl+C và chạy lại launcher. Ctrl+F5 để refresh CSS/assets nếu browser giữ cache. Có thể preview song song bằng `python run_dashboard.py --port 8051`.

Tham khảo API: [Dash callbacks](https://dash.plotly.com/basic-callbacks), [Dash RadioItems](https://dash.plotly.com/dash-core-components/radioitems).

Visual refresh: monochrome SVG UI icons, compact sidebar menu, larger KPI typography, chart headers and responsive white surfaces. Presentation overrides live in `assets/visual.css`; reusable icons live in `components/icons.py`.
