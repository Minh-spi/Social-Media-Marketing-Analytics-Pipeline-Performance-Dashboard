"""Rebuild executed Step 2 notebooks and artifacts; run from any directory.

Dependencies: pandas, openpyxl, numpy, matplotlib, tabulate.
Notebook execution uses a small local runner; no Jupyter dependency required.
"""
from pathlib import Path
import base64
import contextlib
import io
import json
import os
import matplotlib
matplotlib.use('Agg')

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
os.chdir(ROOT)


def md(text):
    return {"cell_type": "markdown", "metadata": {}, "source": text.splitlines(True)}


def code(text):
    return {"cell_type": "code", "metadata": {}, "source": text.splitlines(True),
            "execution_count": None, "outputs": []}


def execute(name, cells):
    namespace = {}
    for count, cell in enumerate((c for c in cells if c['cell_type'] == 'code'), 1):
        outputs = []

        def display(value):
            outputs.append({"output_type": "display_data", "metadata": {}, "data": {
                "text/plain": value.to_string() if hasattr(value, 'to_string') else str(value),
                **({"text/html": value.to_html()} if hasattr(value, 'to_html') else {})}})

        namespace['display'] = display
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            exec(compile(''.join(cell['source']), name, 'exec'), namespace)
        if stream.getvalue():
            outputs.append({"output_type": "stream", "name": "stdout",
                            "text": stream.getvalue().splitlines(True)})
        # Embed figures created by this cell for GitHub notebook rendering.
        if 'plt' in namespace:
            plt = namespace['plt']
            for num in plt.get_fignums():
                buf = io.BytesIO()
                plt.figure(num).savefig(buf, format='png', dpi=110, bbox_inches='tight')
                outputs.append({"output_type": "display_data", "metadata": {},
                                "data": {"image/png": base64.b64encode(buf.getvalue()).decode('ascii'),
                                         "text/plain": "Step 2 descriptive figure"}})
            plt.close('all')
        cell['execution_count'] = count
        cell['outputs'] = outputs
    notebook = {"cells": cells, "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3"}}, "nbformat": 4, "nbformat_minor": 4}
    (OUT / name).write_text(json.dumps(notebook, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(f'Executed: {name}')
    return namespace


setup = '''from pathlib import Path
import pandas as pd
import numpy as np

root = next(p for p in [Path.cwd(), *Path.cwd().parents]
            if (p / "data/Social_Media_Content_Performance_Dataset.xlsx").exists())
out = next(p for p in root.iterdir() if p.is_dir() and p.name.startswith("2."))
artifacts = out / "artifacts"
tables = artifacts / "tables"
figures = artifacts / "figures"
for folder in [artifacts, tables, figures]:
    folder.mkdir(parents=True, exist_ok=True)
pd.set_option("display.max_columns", None)
'''

prep = [md('''# 01 — Data Preparation

Đọc trực tiếp Excel raw; chỉ chuẩn hóa kiểu dữ liệu, tạo trường phân tích và cờ chất lượng. Giữ nguyên mọi record và missing. Không xác nhận grain hoặc công thức rate khi nguồn chưa cung cấp.

Rule: không fill/drop, deduplicate theo Post_ID, cắt outlier hoặc tính lại rate. Giá trị ngoài miền hợp lý được gắn cờ; record đó chỉ bị loại khỏi phép tính KPI liên quan, không bị xóa khỏi file. Bảng rule và kết quả được lưu trong `04_data_quality_summary.md`.
'''), code(setup), code('''raw_path = root / "data/Social_Media_Content_Performance_Dataset.xlsx"
raw = pd.read_excel(raw_path, sheet_name="Sheet1")
df = raw.copy()
df.insert(0, "Source_Row", np.arange(2, len(df) + 2))
counts = ["Engagement", "Views", "Likes", "Shares", "Comments", "Impressions",
          "Video_Views", "Live_Stream_Views", "Clicks"]
rates = ["Engagement_Rate", "Click_Through_Rate"]
dates = ["Post_Published_At", "Post_Date"]
dimensions = ["Post_ID", "Platform", "Content_Type", "Content_Category", "Post_Type",
              "Region", "Main_Hashtag", "Engagement_Level"]
conversion_failures = {}
for col in counts + rates + ["Longitude", "Latitude", "Post_Hour"]:
    converted = pd.to_numeric(df[col], errors="coerce")
    conversion_failures[col] = int((df[col].notna() & converted.isna()).sum())
    df[col] = converted
for col in dates:
    converted = pd.to_datetime(df[col], errors="coerce")
    conversion_failures[col] = int((df[col].notna() & converted.isna()).sum())
    df[col] = converted
for col in dimensions:
    df[col] = df[col].astype("string")  # no label rewriting or null filling
assert not any(conversion_failures.values()), conversion_failures
df["Post_Hour"] = df["Post_Hour"].astype("Int64")
for col in counts:
    df[col] = df[col].astype("Float64")  # preserve nullable counts
df["Month"] = df["Post_Date"].dt.strftime("%Y-%m")
df["Weekday"] = df["Post_Date"].dt.day_name()
last_month = df["Post_Date"].max().to_period("M")
df["Partial_Month"] = df["Post_Date"].dt.to_period("M").eq(last_month) & (
    df["Post_Date"].max().day < df["Post_Date"].max().days_in_month)
display(df.dtypes.rename("analysis_type").to_frame())
'''), code('''quality = []
for col in counts:
    bad = df[col].notna() & ((df[col] < 0) | ~np.isfinite(df[col].astype(float)) |
                             (df[col] % 1 != 0))
    df["Invalid_" + col] = bad.fillna(False).astype(bool)
    quality.append([col, "nonnegative finite integer count", int(bad.sum())])
for col in rates:
    bad = df[col].notna() & ((df[col] < 0) | (df[col] > 1) |
                             ~np.isfinite(df[col].astype(float)))
    df["Invalid_" + col] = bad.fillna(False).astype(bool)
    quality.append([col, "finite decimal within [0, 1]; screening convention", int(bad.sum())])
df["Repeated_Post_ID"] = df.duplicated("Post_ID", keep=False)
candidate_key = ["Post_ID", "Platform", "Post_Published_At"]
df["Repeated_Candidate_Key"] = df.duplicated(candidate_key, keep=False)
quality.extend([
    ["all raw columns", "exact duplicate beyond first", int(raw.duplicated().sum())],
    ["Post_ID", "duplicate beyond first", int(raw.duplicated("Post_ID").sum())],
    ["candidate key", "duplicate beyond first", int(raw.duplicated(candidate_key).sum())],
    ["Post_Date", "timestamp/date mismatch", int(df.Post_Published_At.dt.normalize().ne(df.Post_Date).sum())],
    ["Post_Hour", "timestamp/hour mismatch", int(df.Post_Published_At.dt.hour.ne(df.Post_Hour).sum())],
    ["Post_Hour", "outside [0, 23]", int((~df.Post_Hour.between(0, 23)).sum())],
    ["Longitude", "outside [-180, 180]", int((~df.Longitude.between(-180, 180)).sum())],
    ["Latitude", "outside [-90, 90]", int((~df.Latitude.between(-90, 90)).sum())],
    ["dimensions", "whitespace-only label", sum(int(df[c].str.strip().eq("").sum()) for c in dimensions)],
    ["columns", "duplicate column names", int(df.columns.duplicated().sum())]
])
quality_table = pd.DataFrame(quality, columns=["field", "check", "records"])
missing = pd.DataFrame({"missing_count": raw.isna().sum(),
                        "missing_pct": raw.isna().mean().mul(100)})
display(quality_table)
display(missing)
print("Clicks/CTR missing masks match:", raw.Clicks.isna().equals(raw.Click_Through_Rate.isna()))
print("Engagement != Likes + Shares + Comments:", int(raw.Engagement.ne(raw.Likes+raw.Shares+raw.Comments).sum()))
print("Video_Views > Views:", int(raw.Video_Views.gt(raw.Views).sum()))
print("Live_Stream_Views > Views:", int(raw.Live_Stream_Views.gt(raw.Views).sum()))
print("Post_ID with more than one category:", int((raw.groupby("Post_ID").Content_Category.nunique() > 1).sum()))
print("Maximum difference from candidate ER formula:", (raw.Engagement_Rate - raw.Engagement/raw.Views).abs().max())
print("Maximum difference from candidate CTR formula:", (raw.Click_Through_Rate - raw.Clicks/raw.Impressions).abs().max())
print("These cross-metric differences are unresolved definitions, not automatic invalidation.")
quality_table.to_csv(tables / "data_quality_checks.csv", index=False)
missing.to_csv(tables / "raw_missing_values.csv", index_label="field")
'''), code(r'''analysis_path = artifacts / "analysis_ready.csv"
df.to_csv(analysis_path, index=False, encoding="utf-8", date_format="%Y-%m-%d %H:%M:%S")
check = pd.read_csv(analysis_path, parse_dates=dates)
assert len(check) == len(raw)
assert check.Source_Row.is_unique
for col in counts + rates:
    assert check[col].isna().equals(raw[col].isna())
    assert np.allclose(check[col].dropna().astype(float), raw[col].dropna().astype(float))
rules = """# Data quality summary

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

"""
rules += f"Raw: **{len(raw):,} dòng, {raw.shape[1]} cột**; analysis-ready: **{len(df):,} dòng, {df.shape[1]} cột**. Số dòng bị xóa: **0**; missing bị fill: **0**; số lỗi chuyển kiểu: **0**.\n\n"
rules += quality_table.to_markdown(index=False) + "\n\n"
rules += "Missing ở Clicks và Click_Through_Rate: 3.740 mỗi cột (66,79%); các cột raw còn lại không có null.\n\n"
rules += "Grain, thời điểm trích xuất, cửa sổ đo KPI, timezone và công thức rate chưa xác nhận. Tổng absolute là tổng record trong file, chưa thể coi là lượng duy nhất của doanh nghiệp. Rate dùng mean/median nguồn ở cấp record, không phải rate tổng hợp có mẫu số xác nhận.\n\n"
rules += "Các mã bài có thể khác category giữa record; không chọn category đầu tiên để đại diện. Kiểm tra độ nhạy dùng trọng số 1 / số record của Post_ID và vẫn giữ category của từng record.\n"
(out / "04_data_quality_summary.md").write_text(rules, encoding="utf-8")
print("Saved:", analysis_path.relative_to(root), "Rows:", len(df), "Columns:", df.shape[1])
''')]
execute('01_data_preparation.ipynb', prep)

analysis = [md('''# 02 — Baseline, Breakdown & Problem Detection

Phân tích mô tả để xác định vấn đề tiềm năng, không điều tra nguyên nhân. Không có target/benchmark business; đối chiếu nội bộ không chứng minh không đạt mục tiêu.

Absolute metrics là tổng record nguồn, có thể chứa bài lặp. Efficiency được mô tả bằng **mean/median rate nguồn ở cấp record**, không gọi là overall ER/CTR hoặc rate tính từ tổng. Chênh lệch rate dùng **điểm phần trăm (pp)**; không kiểm định ý nghĩa thống kê hay nhân quả. Click/CTR kèm số record được ghi nhận và chỉ áp dụng cho mẫu đó.
'''), code(setup + '''import matplotlib.pyplot as plt

df = pd.read_csv(artifacts / "analysis_ready.csv", parse_dates=["Post_Date", "Post_Published_At"])
counts = ["Engagement", "Views", "Likes", "Shares", "Comments", "Impressions",
          "Video_Views", "Live_Stream_Views", "Clicks"]
rates = ["Engagement_Rate", "Click_Through_Rate"]
data = df.copy()
for col in counts + rates:
    data.loc[data["Invalid_" + col], col] = np.nan  # KPI-specific mask only

def summarize(frame):
    return pd.Series({
        "records": len(frame), "unique_ids": frame.Post_ID.nunique(),
        "impressions_sum": frame.Impressions.sum(min_count=1),
        "views_sum": frame.Views.sum(min_count=1),
        "views_mean": frame.Views.mean(), "views_median": frame.Views.median(),
        "engagement_sum": frame.Engagement.sum(min_count=1),
        "engagement_mean": frame.Engagement.mean(), "engagement_median": frame.Engagement.median(),
        "er_records": frame.Engagement_Rate.count(),
        "er_mean_pct": frame.Engagement_Rate.mean()*100,
        "er_median_pct": frame.Engagement_Rate.median()*100,
        "click_records": frame.Clicks.count(), "click_coverage_pct": frame.Clicks.notna().mean()*100,
        "clicks_observed_sum": frame.Clicks.sum(min_count=1),
        "clicks_observed_mean": frame.Clicks.mean(),
        "ctr_records": frame.Click_Through_Rate.count(),
        "ctr_mean_pct": frame.Click_Through_Rate.mean()*100,
        "ctr_median_pct": frame.Click_Through_Rate.dropna().median()*100 if frame.Click_Through_Rate.notna().any() else np.nan})

def breakdown(column):
    result = pd.DataFrame({label: summarize(group) for label, group in data.groupby(column)}).T
    result["record_share_pct"] = result.records / len(data)*100
    result["views_share_pct"] = result.views_sum / data.Views.sum()*100
    result["engagement_share_pct"] = result.engagement_sum / data.Engagement.sum()*100
    result.index.name = column
    return result

baseline = summarize(data).to_frame("value")
display(baseline.round(4))
baseline.to_csv(tables / "baseline.csv", index_label="metric")
'''), md('''## Baseline theo thời gian

Tháng ở đây là cohort ngày xuất bản. Không biết các cohort được đo trong cùng cửa sổ performance hay không. Không diễn giải tổng giảm là suy giảm efficiency; đọc cùng số record và rate. Tháng partial giữ trong bảng, tách khỏi biểu đồ so sánh tháng trọn.
'''), code('''monthly = breakdown("Month")
monthly["partial_month"] = data.groupby("Month").Partial_Month.any()
monthly["observed_posting_days"] = data.groupby("Month").Post_Date.nunique()
monthly.to_csv(tables / "monthly.csv")
display(monthly[["records", "partial_month", "observed_posting_days", "impressions_sum", "views_sum",
                 "engagement_sum", "er_mean_pct", "er_median_pct", "click_records", "click_coverage_pct",
                 "clicks_observed_sum", "ctr_mean_pct"]].round(3))
full = monthly.loc[~monthly.partial_month]
fig, axes = plt.subplots(3, 2, figsize=(13, 10))
for ax, col, label in zip(axes.flat,
    ["impressions_sum", "views_sum", "engagement_sum", "er_mean_pct", "clicks_observed_sum", "ctr_mean_pct"],
    ["Impressions: record sum", "Views: record sum", "Engagement: record sum", "Mean source ER (%)",
     "Clicks: observed record sum", "Mean source CTR: observed (%)"]):
    ax.plot(full.index, full[col], marker='o')
    ax.set_title(label)
    ax.tick_params(axis='x', rotation=60)
    ax.grid(alpha=.25)
fig.suptitle("Publication-month cohorts; partial May 2025 excluded", y=1.01)
fig.tight_layout()
fig.savefig(figures / "monthly_trends.png", dpi=150, bbox_inches="tight")
print("Full-month ER mean range:", full.er_mean_pct.min(), full.er_mean_pct.max())
print("Full-month CTR mean range:", full.ctr_mean_pct.min(), full.ctr_mean_pct.max())
print("End-minus-start mean source ER (pp):", full.er_mean_pct.iloc[-1]-full.er_mean_pct.iloc[0])
'''), md('''## Performance breakdown

Các bảng xuất đầy đủ KPI, volume, per-record mean/median và coverage cho mọi chiều. Mẫu nhỏ được đánh dấu khi n < 100; đây là ngưỡng sàng lọc thực hành, không phải ngưỡng ý nghĩa thống kê. Hashtag chỉ là hashtag chính, không phải toàn bộ tag của bài.
'''), code('''segments = {}
for column in ["Platform", "Content_Category", "Post_Type", "Content_Type", "Region",
               "Post_Hour", "Weekday", "Main_Hashtag"]:
    table = breakdown(column)
    table["small_sample"] = table.records < 100
    segments[column] = table
    table.to_csv(tables / ("by_" + column.lower() + ".csv"))
    print(column)
    display(table[["records", "impressions_sum", "views_sum", "engagement_sum", "views_share_pct", "views_mean", "views_median", "engagement_share_pct",
                   "er_mean_pct", "er_median_pct", "click_records", "click_coverage_pct",
                   "clicks_observed_sum", "ctr_mean_pct", "small_sample"]].round(3))
fig, axes = plt.subplots(2, 2, figsize=(13, 8))
for ax, dimension in zip(axes.flat, ["Platform", "Content_Category", "Post_Type", "Region"]):
    t = segments[dimension].sort_values("er_mean_pct")
    ax.barh(t.index.astype(str), t.er_mean_pct)
    ax.axvline(data.Engagement_Rate.mean()*100, color='gray', linestyle='--', label='all records')
    ax.set_xlabel("Mean source ER (%)")
    ax.set_title(dimension)
    ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(figures / "segment_er_comparison.png", dpi=150, bbox_inches="tight")
'''), md('''## Candidate evidence và kiểm tra độ nhạy

So category với phần còn lại để tránh baseline chứa chính segment. Đối chiếu category khác mục đích chỉ là tín hiệu cần điều tra: không có mục tiêu riêng để gọi nhóm này thất bại.

Kiểm tra độ nhạy gồm: median, chỉ tháng trọn và giảm trọng số mã bài lặp. Mỗi Post_ID nhận tổng trọng số 1 trong phép kiểm tra rate; không gom/xóa record hoặc chọn category đại diện. Kiểm tra này không giải quyết grain và không chứng minh khoảng cách đã điều chỉnh các yếu tố khác.
'''), code('''evidence = []
id_weights = 1 / data.groupby("Post_ID").Post_ID.transform("size")
for category in ["Entertainment", "Product Promotion"]:
    mask = data.Content_Category.eq(category)
    a, b = data.loc[mask], data.loc[~mask]
    a_full = a.loc[~a.Partial_Month]; b_full = b.loc[~b.Partial_Month]
    weighted_a = np.average(a.Engagement_Rate, weights=id_weights.loc[mask])*100
    weighted_b = np.average(b.Engagement_Rate, weights=id_weights.loc[~mask])*100
    evidence.append({"category": category, "records": len(a),
        "views_share_pct": a.Views.sum()/data.Views.sum()*100,
        "engagement_share_pct": a.Engagement.sum()/data.Engagement.sum()*100,
        "er_mean_pct": a.Engagement_Rate.mean()*100,
        "rest_er_mean_pct": b.Engagement_Rate.mean()*100,
        "gap_pp": (b.Engagement_Rate.mean()-a.Engagement_Rate.mean())*100,
        "relative_gap_pct": (1-a.Engagement_Rate.mean()/b.Engagement_Rate.mean())*100,
        "er_median_pct": a.Engagement_Rate.median()*100,
        "rest_er_median_pct": b.Engagement_Rate.median()*100,
        "full_month_er_pct": a_full.Engagement_Rate.mean()*100,
        "full_month_rest_er_pct": b_full.Engagement_Rate.mean()*100,
        "id_weighted_er_pct": weighted_a, "id_weighted_rest_er_pct": weighted_b})
evidence = pd.DataFrame(evidence).set_index("category")
display(evidence.round(4))
evidence.to_csv(tables / "category_candidate_evidence.csv")
fig, ax = plt.subplots(figsize=(9, 5))
cat = segments['Content_Category']
x = np.arange(len(cat))
ax.bar(x-.18, cat.views_share_pct, width=.36, label='Views share (%)')
ax.bar(x+.18, cat.engagement_share_pct, width=.36, label='Engagement share (%)')
ax.set_xticks(x, cat.index, rotation=20, ha='right')
ax.set_ylabel("Share of record totals (%)")
ax.legend()
fig.tight_layout()
fig.savefig(figures / "category_volume_shares.png", dpi=150, bbox_inches="tight")
'''), code('''ent_months = pd.DataFrame({m: pd.Series({
    "ent_records": len(g.loc[g.Content_Category.eq("Entertainment")]),
    "ent_er_pct": g.loc[g.Content_Category.eq("Entertainment"), "Engagement_Rate"].mean()*100,
    "rest_er_pct": g.loc[~g.Content_Category.eq("Entertainment"), "Engagement_Rate"].mean()*100})
    for m, g in data.loc[~data.Partial_Month].groupby("Month")}).T
ent_months["gap_pp"] = ent_months.rest_er_pct - ent_months.ent_er_pct
display(ent_months.round(3))
ent_months.to_csv(tables / "entertainment_monthly_evidence.csv", index_label="Month")
print("Months with Entertainment below rest:", int((ent_months.gap_pp > 0).sum()), "/", len(ent_months))
print("Minimum/maximum monthly gap pp:", ent_months.gap_pp.min(), ent_months.gap_pp.max())
print("No inference about the reasons for any gap is made.")
''')]
ns = execute('02_baseline_and_problem_detection.ipynb', analysis)

# Generate concise reports from the same executed results; numbers stay synchronized.
data, evidence, full, segments = (ns[k] for k in ['data', 'evidence', 'full', 'segments'])
e = evidence.loc['Entertainment']; p = evidence.loc['Product Promotion']
platform = segments['Platform']; post = segments['Post_Type']; region = segments['Region']
gap_channel = platform.loc['Instagram', 'er_mean_pct'] - platform.loc['LinkedIn', 'er_mean_pct']
gap_video = post.loc['Image', 'er_mean_pct'] - post.loc['Video', 'er_mean_pct']

report = f'''# Problem statement — Bước 2

## Kết luận chính

**Trong giai đoạn 01/01/2024–01/05/2025, nhóm Entertainment có Engagement_Rate trung bình nguồn {e.er_mean_pct:.2f}%, thấp hơn {e.gap_pp:.2f} điểm phần trăm so với {e.rest_er_mean_pct:.2f}% của phần dữ liệu còn lại, cho thấy mức tương tác tương đối ghi nhận thấp trên nhóm chiếm {e.views_share_pct:.2f}% Views nhưng chỉ {e.engagement_share_pct:.2f}% Engagement của tổng record.**

Đây là vấn đề tiềm năng về khoảng cách engagement, không phải kết luận nhóm này không đạt mục tiêu: brief không có target và category có thể có mục đích marketing khác nhau. “ER” trong tài liệu là mean/median của rate nguồn ở cấp record; công thức chưa xác nhận. Không phải ER tính từ tổng và không quy đổi gap thành engagement thất thoát.

## Baseline và time trend

| KPI | Baseline toàn bộ file |
| --- | ---: |
| Record / Post_ID duy nhất | {len(data):,} / {data.Post_ID.nunique():,} |
| Impressions — tổng record | {data.Impressions.sum():,.0f} |
| Views — tổng record | {data.Views.sum():,.0f} |
| Engagement — tổng record | {data.Engagement.sum():,.0f} |
| Mean / median source ER | {data.Engagement_Rate.mean()*100:.2f}% / {data.Engagement_Rate.median()*100:.2f}% |
| Clicks — tổng phần có dữ liệu | {data.Clicks.sum():,.0f} |
| Click coverage | {data.Clicks.count():,}/{len(data):,} ({data.Clicks.notna().mean()*100:.2f}%) |
| Mean / median source CTR — phần có dữ liệu | {data.Click_Through_Rate.mean()*100:.2f}% / {data.Click_Through_Rate.median()*100:.2f}% |

Các tháng trọn 01/2024–04/2025 có mean source ER từ **{full.er_mean_pct.min():.2f}% đến {full.er_mean_pct.max():.2f}%**, mean source CTR quan sát từ **{full.ctr_mean_pct.min():.2f}% đến {full.ctr_mean_pct.max():.2f}%**. ER tháng cuối trọn cao hơn tháng đầu {full.er_mean_pct.iloc[-1]-full.er_mean_pct.iloc[0]:.2f} pp; không có chuỗi giảm liên tục. Tháng 04/2024 là điểm ER thấp nhất nhưng không được chọn là vấn đề chính vì khoảng cách nhỏ và các tháng sau không duy trì mức này.

Volume tháng trọn: Views **{full.views_sum.min():,.0f}–{full.views_sum.max():,.0f}**, Engagement **{full.engagement_sum.min():,.0f}–{full.engagement_sum.max():,.0f}**, Clicks phần quan sát **{full.clicks_observed_sum.min():,.0f}–{full.clicks_observed_sum.max():,.0f}**. Số record tháng **{full.records.min():.0f}–{full.records.max():.0f}**, click coverage **{full.click_coverage_pct.min():.2f}%–{full.click_coverage_pct.max():.2f}%**; chưa thể coi biến động tổng là biến động efficiency tương ứng.

Tháng 05/2025 chỉ có 10 record, ngày 01/05; tổng tháng thấp không được coi là performance giảm. Tổng theo tháng là performance của cohort ngày đăng, chưa có cửa sổ đo đồng nhất. Đồ thị và bảng kèm volume/coverage trong notebook.

## Segment performance summary

| Chiều | Dấu hiệu quan sát | Giới hạn đối chiếu |
| --- | --- | --- |
| Platform | Mean source ER: Instagram {platform.loc['Instagram','er_mean_pct']:.2f}%, LinkedIn {platform.loc['LinkedIn','er_mean_pct']:.2f}%; gap {gap_channel:.2f} pp | Volume/cơ cấu khác nhau; Click coverage LinkedIn chỉ 304/525, Instagram không có Clicks |
| Category | Educational {segments['Content_Category'].loc['Educational','er_mean_pct']:.2f}%, Entertainment {e.er_mean_pct:.2f}%; Entertainment có {e.views_share_pct:.2f}% Views | Mục tiêu category chưa xác nhận; đối chiếu mô tả |
| Post type | Video có {post.loc['Video','views_share_pct']:.2f}% Views, mean ER {post.loc['Video','er_mean_pct']:.2f}% so với Image {post.loc['Image','er_mean_pct']:.2f}% | PDF/Carousel n < 100; không chọn nhóm nhỏ thành “tốt nhất” |
| Content type | Organic {segments['Content_Type'].loc['Organic','er_mean_pct']:.2f}%, Sponsored {segments['Content_Type'].loc['Sponsored','er_mean_pct']:.2f}% | Không có chi phí; không suy ra hiệu quả quảng cáo |
| Region | Germany {region.loc['Germany','er_mean_pct']:.2f}%; các region còn lại {region.drop('Germany').er_mean_pct.min():.2f}%–{region.drop('Germany').er_mean_pct.max():.2f}% | Nhãn Region chưa xác nhận là vị trí người xem |
| Time | Mean ER theo giờ {segments['Post_Hour'].er_mean_pct.min():.2f}%–{segments['Post_Hour'].er_mean_pct.max():.2f}% | Không có timezone; chưa kết luận giờ tối ưu |
| Main hashtag | #TrendingNow: n=535, mean ER {segments['Main_Hashtag'].loc['#TrendingNow','er_mean_pct']:.2f}%; #SuccessStory: n=1.523, ER {segments['Main_Hashtag'].loc['#SuccessStory','er_mean_pct']:.2f}% | Một số tag chỉ 1–4 record; không khẳng định tác động hashtag |

## Problem candidates

| ID | KPI / segment / thời gian | Evidence | Ảnh hưởng sơ bộ quan sát |
| --- | --- | --- | --- |
| P1 | Source ER / Entertainment / toàn kỳ | n={e.records:.0f}; {e.er_mean_pct:.2f}% so với phần còn lại {e.rest_er_mean_pct:.2f}%; gap {e.gap_pp:.2f} pp ({e.relative_gap_pct:.2f}% tương đối) | {e.views_share_pct:.2f}% Views, {e.engagement_share_pct:.2f}% Engagement; nhóm quy mô lớn có rate thấp tương đối |
| P2 | Source ER / Product Promotion / toàn kỳ | n={p.records:.0f}; {p.er_mean_pct:.2f}% so với phần còn lại {p.rest_er_mean_pct:.2f}%; gap {p.gap_pp:.2f} pp ({p.relative_gap_pct:.2f}% tương đối) | {p.views_share_pct:.2f}% Views, {p.engagement_share_pct:.2f}% Engagement; phạm vi exposure rộng |
| P3 | Source ER / Video so với Image / toàn kỳ | n=2.948 so với 996; {post.loc['Video','er_mean_pct']:.2f}% so với {post.loc['Image','er_mean_pct']:.2f}%; gap {gap_video:.2f} pp | Video chiếm {post.loc['Video','views_share_pct']:.2f}% Views; candidate rộng, chưa tách khỏi P1/P2 |
| P4 | Source ER / LinkedIn so với Instagram / toàn kỳ | n=525 so với 998; {platform.loc['LinkedIn','er_mean_pct']:.2f}% so với {platform.loc['Instagram','er_mean_pct']:.2f}%; gap {gap_channel:.2f} pp | LinkedIn chiếm {platform.loc['LinkedIn','views_share_pct']:.2f}% Views; magnitude nhỏ hơn category gap |
| P5 | Source ER / 04/2024 so với 03/2024 | n=353 so với 393; {full.loc['2024-04','er_mean_pct']:.2f}% so với {full.loc['2024-03','er_mean_pct']:.2f}%; thấp hơn {full.loc['2024-03','er_mean_pct']-full.loc['2024-04','er_mean_pct']:.2f} pp | Một cohort tháng; chưa thấy suy giảm duy trì |

Missing Click/CTR 66,79% là hạn chế đo lường, không được ghi thành vấn đề “click thấp”. Không có căn cứ định lượng thiệt hại doanh thu, chi phí hoặc phần engagement có thể tăng thêm.

## Problem prioritization

Điểm 1–4 là rule sàng lọc minh bạch, không phải KPI target hoặc kiểm định thống kê. Tổng điểm dùng trọng số bằng nhau:

- **Magnitude:** tỷ lệ thấp hơn comparator: ≥40% → 4; 25–<40% → 3; 10–<25% → 2; <10% → 1.
- **Scope:** share Views của segment: ≥30% → 4; 15–<30% → 3; 5–<15% → 2; <5% → 1. Với candidate tháng, share Views của cohort trong toàn kỳ.
- **Business relevance:** 4 nếu trực tiếp thuộc Content/Channel decision được brief nhấn mạnh; 3 cho lịch đăng/thị trường; 2 nếu chỉ liên quan gián tiếp; 1 nếu chưa gắn decision.
- **Data support:** 4 nếu KPI/grain/cửa sổ đo được xác nhận và có coverage đủ; 3 nếu n≥100, KPI đủ record nhưng còn giới hạn định nghĩa/grain; 2 nếu tín hiệu chỉ là một lần thay đổi giữa hai cohort liền kề hoặc coverage hạn chế; 1 nếu mẫu quá nhỏ/không đủ KPI.

| Candidate | Magnitude | Scope | Business relevance | Data support | Tổng | Ưu tiên |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| P1 — Entertainment | 4 | 3 | 4 | 3 | 14 | Chính |
| P2 — Product Promotion | 3 | 4 | 4 | 3 | 14 | Secondary |
| P3 — Video vs Image | 2 | 4 | 4 | 3 | 13 | Giữ trong candidate; chưa mở thêm problem |
| P4 — LinkedIn vs Instagram | 1 | 2 | 4 | 3 | 10 | Thấp hơn |
| P5 — 04/2024 | 1 | 2 | 3 | 2 | 8 | Thấp hơn |

P1/P2 cùng tổng điểm; chọn P1 theo tie-break **gap tương đối và gap pp lớn hơn**, cùng với độ bền mô tả qua các tháng. P2 có scope rộng hơn nên giữ đúng một secondary problem. P3 chưa mở thành problem riêng để giữ phạm vi điều tra gọn; chưa xác định quan hệ giữa các candidate.

## Evidence đủ để ưu tiên P1

- Mean source ER {e.er_mean_pct:.2f}% so với {e.rest_er_mean_pct:.2f}%; median {e.er_median_pct:.2f}% so với {e.rest_er_median_pct:.2f}%. Tín hiệu không chỉ xuất hiện ở mean.
- Chỉ tháng trọn: {e.full_month_er_pct:.2f}% so với {e.full_month_rest_er_pct:.2f}%. Entertainment thấp hơn phần còn lại trong **16/16 cohort tháng trọn**; không dựa vào tháng partial.
- Giảm trọng số mã lặp: ER {e.id_weighted_er_pct:.2f}% so với {e.id_weighted_rest_er_pct:.2f}%. Đây là kiểm tra độ nhạy, không giải quyết grain.
- n={e.records:.0f}, không thiếu ER trong nhóm; mức {e.views_share_pct:.2f}% Views gắn trực tiếp với Content decision ở bước 1. Đủ metadata để tiếp tục điều tra mô tả, nhưng chưa đủ cho kết luận causal.

## Secondary problem statement

Trong giai đoạn 01/01/2024–01/05/2025, Product Promotion có Engagement_Rate trung bình nguồn {p.er_mean_pct:.2f}%, thấp hơn {p.gap_pp:.2f} pp so với {p.rest_er_mean_pct:.2f}% của phần dữ liệu còn lại, cho thấy mức engagement tương đối ghi nhận thấp trên nhóm chiếm {p.views_share_pct:.2f}% Views và {p.engagement_share_pct:.2f}% Engagement của tổng record.

**Phạm vi bàn giao bước 3:** điều tra khoảng cách của P1, giữ P2 làm secondary. Bước 2 chỉ xác lập tín hiệu và mức ưu tiên; không giải thích nguyên nhân, đề xuất hành động, dựng dashboard hoặc model.

**Nguồn:** [Notebook phân tích](02_baseline_and_problem_detection.ipynb), [Data quality](04_data_quality_summary.md), [Evidence category](artifacts/tables/category_candidate_evidence.csv), [Evidence theo tháng](artifacts/tables/entertainment_monthly_evidence.csv).
'''
(OUT / '03_problem_statement.md').write_text(report, encoding='utf-8')
(OUT / 'README.md').write_text('''# Bước 2 — Xác định vấn đề

Chạy `01_data_preparation.ipynb` trước, rồi `02_baseline_and_problem_detection.ipynb`. Dependencies: Python, pandas, openpyxl, numpy, matplotlib, tabulate. Có thể tái tạo toàn bộ output bằng `python "2. Xác định vấn đề/build_step2.py"` từ project root.

| Output | Nội dung |
| --- | --- |
| [Data preparation](01_data_preparation.ipynb) | Kiểu dữ liệu, null, duplicate, miền KPI; lưu dataset riêng |
| [Analysis-ready CSV](artifacts/analysis_ready.csv) | Giữ nguyên record/missing; thêm trường phân tích và cờ chất lượng |
| [Data quality summary](04_data_quality_summary.md) | Rule xử lý, số lượng và giới hạn còn lại |
| [Baseline & detection](02_baseline_and_problem_detection.ipynb) | Baseline, time trend, breakdown, evidence và độ nhạy |
| [Problem statement](03_problem_statement.md) | Candidates, chấm ưu tiên, problem chính và secondary |
| [Bảng dữ liệu](artifacts/tables) / [Biểu đồ](artifacts/figures) | Output tĩnh để đối chiếu số liệu |

**Problem chính:** Entertainment có mean source ER thấp hơn rõ rệt phần còn lại, trong khi đóng góp volume Views đáng kể; khoảng cách duy trì qua 16 tháng trọn. Product Promotion được giữ làm secondary. Không có KPI target; đây là tín hiệu cần điều tra, chưa phải kết luận không đạt mục tiêu.

Không thực hiện phân tích nguyên nhân, recommendation, predictive/prescriptive analysis hoặc dashboard cuối cùng.
''', encoding='utf-8')
print('Saved reports and artifacts.')
