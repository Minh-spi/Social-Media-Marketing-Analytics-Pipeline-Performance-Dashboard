"""Rebuild Step 3 notebooks and artifacts. Requires pandas/numpy/matplotlib/tabulate.
Reads Step 2 outputs; never writes to raw data or earlier steps.
"""
from pathlib import Path
import base64
import contextlib
import io
import json
import os
import matplotlib
matplotlib.use('Agg')

OUT = Path(__file__).resolve().parent
os.chdir(OUT.parent)


def md(text):
    return {'cell_type': 'markdown', 'metadata': {}, 'source': text.splitlines(True)}


def code(text):
    return {'cell_type': 'code', 'metadata': {}, 'source': text.splitlines(True),
            'execution_count': None, 'outputs': []}


def execute(name, cells):
    ns = {}
    for count, cell in enumerate((c for c in cells if c['cell_type'] == 'code'), 1):
        outputs = []

        def display(value):
            outputs.append({'output_type': 'display_data', 'metadata': {}, 'data': {
                'text/plain': value.to_string() if hasattr(value, 'to_string') else str(value),
                **({'text/html': value.to_html()} if hasattr(value, 'to_html') else {})}})

        ns['display'] = display
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            exec(compile(''.join(cell['source']), name, 'exec'), ns)
        if stream.getvalue():
            outputs.append({'output_type': 'stream', 'name': 'stdout', 'text': stream.getvalue().splitlines(True)})
        if 'plt' in ns:
            for num in ns['plt'].get_fignums():
                buffer = io.BytesIO()
                ns['plt'].figure(num).savefig(buffer, format='png', dpi=110, bbox_inches='tight')
                outputs.append({'output_type': 'display_data', 'metadata': {}, 'data': {
                    'image/png': base64.b64encode(buffer.getvalue()).decode('ascii'),
                    'text/plain': 'Step 3 descriptive figure'}})
            ns['plt'].close('all')
        cell.update(execution_count=count, outputs=outputs)
    nb = {'cells': cells, 'metadata': {
        'kernelspec': {'display_name': 'Python 3', 'language': 'python', 'name': 'python3'},
        'language_info': {'name': 'python', 'version': '3'}}, 'nbformat': 4, 'nbformat_minor': 4}
    (OUT / name).write_text(json.dumps(nb, ensure_ascii=False, indent=1)+'\n', encoding='utf-8')
    print('Executed:', name)
    return ns


setup = '''from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

root = next(p for p in [Path.cwd(), *Path.cwd().parents]
            if (p / "data/Social_Media_Content_Performance_Dataset.xlsx").exists())
step2 = next(p for p in root.iterdir() if p.is_dir() and p.name.startswith("2."))
out = next(p for p in root.iterdir() if p.is_dir() and p.name.startswith("3."))
tables = out / "artifacts/tables"
figures = out / "artifacts/figures"
for path in [tables, figures]:
    path.mkdir(parents=True, exist_ok=True)
source = pd.read_csv(step2 / "artifacts/analysis_ready.csv",
                     parse_dates=["Post_Date", "Post_Published_At"])
assert source.Source_Row.is_unique
for col in ["Engagement_Rate", "Views", "Impressions", "Engagement"]:
    source.loc[source["Invalid_"+col], col] = np.nan
# No new cleaning, imputation, recoding or deduplication.
# Main analysis uses full publication-month cohorts; partial month is sensitivity only.
data = source.loc[~source.Partial_Month].copy()
data["Group"] = np.where(data.Content_Category.eq("Entertainment"), "Entertainment", "Rest")
N_E = int(data.Group.eq("Entertainment").sum())
N_R = len(data)-N_E
THRESHOLD = 30  # per group per cell; descriptive screening, not a power calculation

def save(table, name):
    table.to_csv(tables / (name+".csv"), index=True)

def pairs(frame, columns, threshold=THRESHOLD):
    groups = {label: g for label, g in frame.groupby(columns, dropna=False)}
    rows = []
    for label, group in groups.items():
        labels = label if isinstance(label, tuple) else (label,)
        row = dict(zip(columns, labels))
        for short, mask in [("E", group.Content_Category.eq("Entertainment")),
                            ("R", ~group.Content_Category.eq("Entertainment"))]:
            g = group.loc[mask]
            row.update({"n_"+short: len(g), "er_n_"+short: g.Engagement_Rate.count(),
                "mean_"+short: g.Engagement_Rate.mean()*100,
                "median_"+short: g.Engagement_Rate.median()*100 if len(g) else np.nan,
                "views_"+short: g.Views.sum(min_count=1),
                "impressions_"+short: g.Impressions.sum(min_count=1),
                "engagement_"+short: g.Engagement.sum(min_count=1)})
        row['gap_pp'] = row['mean_R']-row['mean_E']
        row['median_gap_pp'] = row['median_R']-row['median_E']
        row['eligible'] = min(row['er_n_E'], row['er_n_R']) >= threshold
        rows.append(row)
    result = pd.DataFrame(rows).set_index(columns)
    result['mix_E_pct'] = result.n_E / frame.Content_Category.eq('Entertainment').sum()*100
    result['mix_R_pct'] = result.n_R / (~frame.Content_Category.eq('Entertainment')).sum()*100
    return result

def decomposition(table, driver):
    # Common support with adequate sample in BOTH groups; excluded cells retained in tables.
    t = table.loc[table.eligible].copy()
    if t.empty:
        return {"driver": driver, "eligible_cells": 0}
    pE, pR = t.n_E/t.n_E.sum(), t.n_R/t.n_R.sum()
    mE, mR = t.mean_E, t.mean_R
    composition = ((pR-pE)*(mR+mE)/2).sum()
    within = ((pR+pE)/2*(mR-mE)).sum()
    subset_gap = (pR*mR).sum()-(pE*mE).sum()
    assert np.isclose(composition+within, subset_gap)
    return {"driver": driver, "eligible_cells": len(t),
        "coverage_E_pct": t.n_E.sum()/N_E*100, "coverage_R_pct": t.n_R.sum()/N_R*100,
        "supported_subset_gap_pp": subset_gap, "composition_pp": composition,
        "within_segment_pp": within,
        "rest_standardized_to_E_pct": (pE*mR).sum(), "E_supported_mean_pct": (pE*mE).sum(),
        "E_mix_standardized_gap_pp": (pE*(mR-mE)).sum(),
        "min_cell_gap_pp": t.gap_pp.min(), "max_cell_gap_pp": t.gap_pp.max(),
        "cells_E_at_or_above_rest": int((t.gap_pp<=0).sum())}

def category_table(columns):
    t = data.groupby(columns+["Content_Category"]).agg(
        records=("Source_Row", "size"), er_records=("Engagement_Rate", "count"),
        mean_source_er=("Engagement_Rate", "mean"), median_source_er=("Engagement_Rate", "median"),
        views=("Views", "sum"), impressions=("Impressions", "sum"), engagement=("Engagement", "sum"))
    t['mean_source_er_pct'] = t.pop('mean_source_er')*100
    t['median_source_er_pct'] = t.pop('median_source_er')*100
    t['small_sample'] = t.er_records < THRESHOLD
    return t

baseline = category_table([])
display(baseline.round(3))
save(baseline, "category_baseline_full_months")
print("Full-month records E / Rest:", N_E, N_R)
print("Main metric: source ER mean/median, not Engagement/Views computed from totals.")
'''

hypotheses = '''# Hypothesis Setup

Đối tượng chính: Entertainment so với non-Entertainment trong 16 cohort tháng trọn (01/2024–04/2025). Tháng 05/2025 partial chỉ dùng kiểm tra độ nhạy. Secondary: Product Promotion, kiểm tra riêng ở mức giới hạn.

| ID | Driver / giả thuyết | Logic | Metric | Cách kiểm tra |
| --- | --- | --- | --- | --- |
| H1 | Platform mix | Entertainment tập trung ở kênh có ER thấp | Source ER mean/median, record mix, Views | So cùng platform; chuẩn hóa mix và decomposition |
| H2 | Post Type | Cơ cấu định dạng liên quan đến một phần gap | ER, record mix, Views/Engagement | So cùng post type; chuẩn hóa mix; kiểm tra platform × post type |
| H3 | Organic/Sponsored | Cơ cấu phân phối khác nhau liên quan đến gap | ER, record mix | So cùng Content_Type; decomposition |
| H4 | Region | Entertainment tập trung ở region có ER thấp | ER, record mix | So cùng Region; decomposition, leave-one-region-out |
| H5 | Month/Day/Hour | Cơ cấu thời điểm đăng liên quan đến gap | ER, số record | So cùng Month/Weekday/Post_Hour; không quy đổi timezone |
| H6 | Main hashtag | Nhóm hashtag gắn với ER thấp | ER, số record và common support | Cross-tab category × hashtag; chỉ so tag có cả hai nhóm đủ mẫu |
| H7 | Interaction | Một tổ hợp platform/định dạng/phân phối tập trung phần lớn gap | ER, cell n, Views; gap chuẩn hóa | So cùng platform × post type, platform × Content_Type, region × post type; xác định coverage |
| H8 | Độ nhạy | Gap phụ thuộc mẫu nhỏ/outlier/mã lặp/cách đo | Mean/median, gap pp | Ngưỡng 10/30/50; winsor 1%; trọng số mã; loại lần lượt platform/region |

Không giả thuyết nào được coi là causal từ phép so sánh observational. “Driver” là yếu tố liên quan được kiểm tra; không mặc định mọi hypothesis phải được ủng hộ.
'''
(OUT / '00_hypothesis_setup.md').write_text(hypotheses, encoding='utf-8')

first = [md('''# 01 — Hypothesis & Driver Analysis

Phạm vi chỉ bước 3: chẩn đoán mô tả, không recommendation/model/dashboard. Đọc analysis-ready bước 2; raw và bước 1/2 không thay đổi. Mean source ER có công thức chưa xác nhận và không phải rate tổng hợp. Tổng volume là tổng record, chưa xác nhận unique-post grain.
'''), md(hypotheses), code(setup), md('''## Driver riêng và chuẩn hóa cơ cấu

So cùng segment, n ≥ 30 mỗi nhóm. Chuẩn hóa non-Entertainment theo record mix Entertainment ở các cell đủ mẫu. Decomposition đối xứng:

`gap = sum((p_R-p_E)*(m_R+m_E)/2) + sum((p_R+p_E)/2*(m_R-m_E))`.

Thành phần thứ nhất là composition; thứ hai là within-segment. p là tỷ trọng record, m là mean source ER (%). Công thức là đẳng thức mô tả trên common support, không phải mediation/causal attribution. Mỗi driver phân rã riêng; không cộng các phần composition giữa driver. Gap của subset khác gap toàn mẫu nếu có cell bị loại; luôn kèm coverage.
'''), code('''drivers = {}
effects = []
for col in ["Platform", "Post_Type", "Content_Type", "Region", "Month", "Weekday", "Post_Hour", "Main_Hashtag"]:
    t = pairs(data, [col])
    drivers[col] = t
    save(t, "driver_"+col.lower())
    effects.append(decomposition(t, col))
    print(col)
    display(t[["n_E", "n_R", "mean_E", "mean_R", "median_E", "median_R", "gap_pp",
               "mix_E_pct", "mix_R_pct", "eligible"]].round(3))
    save(category_table([col]), "categories_by_"+col.lower())
effects = pd.DataFrame(effects).set_index('driver')
save(effects, "driver_effect_summary")
display(effects.round(4))
'''), code('''fig, axes = plt.subplots(2, 3, figsize=(15, 9))
for ax, col in zip(axes.flat, ["Platform", "Post_Type", "Content_Type", "Region", "Weekday", "Post_Hour"]):
    t = drivers[col].loc[drivers[col].eligible]
    x = np.arange(len(t))
    ax.bar(x-.18, t.mean_E, width=.36, label='Entertainment')
    ax.bar(x+.18, t.mean_R, width=.36, label='Rest: same segment')
    ax.set_xticks(x, t.index.astype(str), rotation=45, ha='right')
    ax.set_title(col+" (n >= 30 each)")
    ax.set_ylabel('Mean source ER (%)')
    ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(figures / 'driver_comparison.png', dpi=150, bbox_inches='tight')
fig, ax = plt.subplots(figsize=(9, 4))
t = effects.drop('Main_Hashtag')
ax.barh(t.index, t.composition_pp)
ax.axvline(0, color='gray')
ax.set_xlabel('Composition component (pp); each driver analyzed separately')
ax.set_title('Eligible common support: record-mix decomposition')
fig.tight_layout()
fig.savefig(figures / 'composition_components.png', dpi=150, bbox_inches='tight')
'''), md('''## Hashtag: common support và khả năng tách effect

Một tag không có comparator đủ mẫu không thể xác định effect độc lập. Tag chỉ là Main_Hashtag và gắn chặt với category. Không diễn giải ER thấp ở tag của Entertainment thành nguyên nhân từ hashtag.
'''), code('''cross = pd.crosstab(data.Main_Hashtag, data.Content_Category)
save(cross, 'hashtag_category_counts')
display(cross)
tag_purity = cross.max(axis=1)/cross.sum(axis=1)
print('Hashtags appearing in only one category:', int(cross.gt(0).sum(axis=1).eq(1).sum()), '/', len(cross))
print('Entertainment coverage in eligible hashtag comparisons:', effects.loc['Main_Hashtag', 'coverage_E_pct'])
''')]
one = execute('01_hypothesis_and_driver_analysis.ipynb', first)

second = [md('''# 02 — Interaction & Robustness

So cùng các tổ hợp quan sát là segment comparison, không phải kiểm soát mọi confounder. Cell nhỏ/không overlap được giữ trong bảng nhưng không dùng kết luận chính; ngưỡng n ≥ 30 cho mỗi nhóm là sàng lọc mô tả. Không kiểm định significance; không suy luận về quần thể hay nhân quả.
'''), code(setup), code('''interaction_effects = []
interactions = {}
for cols in [["Platform", "Post_Type"], ["Platform", "Content_Type"],
             ["Region", "Post_Type"], ["Post_Type", "Content_Type"],
             ["Platform", "Post_Hour"]]:
    name = "_x_".join(cols)
    t = pairs(data, cols)
    interactions[name] = t
    save(t, "interaction_"+name.lower())
    interaction_effects.append(decomposition(t, name))
interaction_effects = pd.DataFrame(interaction_effects).set_index('driver')
display(interaction_effects.round(3))
save(interaction_effects, 'interaction_effect_summary')
for cols in [["Platform"], ["Post_Type"], ["Region"], ["Content_Type"],
             ["Month"], ["Weekday"], ["Post_Hour"], ["Platform", "Post_Type"]]:
    table = category_table(cols)
    save(table, 'interaction_categories_'+'_x_'.join(cols).lower())
    if len(cols)==1 and cols[0] in ['Platform','Post_Type','Region','Content_Type']:
        print(cols[0], 'x category (mean source ER %)')
        display(table.mean_source_er_pct.unstack('Content_Category').round(3))
print('Platform x Post_Type eligible gap:')
display(interactions['Platform_x_Post_Type'].loc[lambda t: t.eligible,
    ['n_E','n_R','mean_E','mean_R','gap_pp','median_gap_pp','views_E','views_R']].round(3))
'''), code('''def heatmap(ax, values, title, cmap='viridis'):
    arr = values.to_numpy(dtype=float)
    masked = np.ma.masked_invalid(arr)
    im = ax.imshow(masked, aspect='auto', cmap=cmap)
    ax.set_xticks(range(len(values.columns)), values.columns, rotation=40, ha='right')
    ax.set_yticks(range(len(values)), values.index)
    for i in range(len(values)):
        for j in range(len(values.columns)):
            if np.isfinite(arr[i,j]):
                ax.text(j,i,f'{arr[i,j]:.1f}',ha='center',va='center',fontsize=8,
                        bbox={'facecolor':'white','alpha':.65,'edgecolor':'none'})
    ax.set_title(title)
    plt.colorbar(im, ax=ax, label='pp / % as labeled')

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
c = category_table(['Platform'])
heatmap(axes[0], c.mean_source_er_pct.where(~c.small_sample).unstack('Content_Category'),
        'Platform x Category: mean source ER (%), n >= 30')
t = interactions['Platform_x_Post_Type']
heatmap(axes[1], t.gap_pp.where(t.eligible).unstack('Post_Type'),
        'Platform x Post Type: Rest minus Entertainment (pp)')
fig.tight_layout()
fig.savefig(figures / 'interaction_heatmaps.png', dpi=150, bbox_inches='tight')
'''), md('''## Robustness

Mean/median so toàn mẫu và trong cell. Kiểm tra tháng/platform/region, ngưỡng n=10/30/50 và leave-one-group-out. Winsor 1% áp dụng cùng ngưỡng pooled ER cho hai nhóm, chỉ là sensitivity, không cập nhật dataset. Loại top 1% Views chỉ là phép kiểm tra xem record exposure lớn có làm thay đổi kết quả, không khẳng định outlier là lỗi.

Mã bài lặp: trọng số từng record bằng 1/số record Post_ID. Giữ category của từng record; một số ID có nhiều category. Đây không phải deduplication hoặc xác nhận grain. Các sensitivity không phải tập kết quả độc lập để tính significance.

Trong dòng trọng số Post_ID, chỉ mean được weighted; cột median vẫn là median record không trọng số để đối chiếu. Các ô trống trên heatmap là thiếu common support hoặc n < 30, không phải ER bằng 0.
'''), code('''def gap_summary(frame, label, er_col='Engagement_Rate', weights=None):
    mask = frame.Content_Category.eq('Entertainment')
    a,b = frame.loc[mask], frame.loc[~mask]
    ma,mb = a[er_col].mean()*100,b[er_col].mean()*100
    if weights is not None:
        ma=np.average(a[er_col],weights=weights.loc[mask])*100
        mb=np.average(b[er_col],weights=weights.loc[~mask])*100
    return {'check':label,'n_E':len(a),'n_R':len(b),'mean_E_pct':ma,'mean_R_pct':mb,
            'mean_gap_pp':mb-ma,'median_gap_pp':(b[er_col].median()-a[er_col].median())*100}

robust = [gap_summary(data,'Full months'), gap_summary(source,'Including partial May')]
weights = 1/data.groupby('Post_ID').Post_ID.transform('size')
robust.append(gap_summary(data,'Each Post_ID total weight=1',weights=weights))
lo,hi = data.Engagement_Rate.quantile([.01,.99])
winsor = data.copy()
winsor['ER_sensitivity'] = winsor.Engagement_Rate.clip(lo,hi)
robust.append(gap_summary(winsor,'Pooled ER winsor 1%/99% (sensitivity only)','ER_sensitivity'))
exposure = data.loc[data.Views <= data.Views.quantile(.99)]
robust.append(gap_summary(exposure,'Exclude Views above pooled p99 (sensitivity only)'))
robust = pd.DataFrame(robust).set_index('check')
display(robust.round(4)); save(robust,'robustness_overall')
print('Winsor thresholds:',lo,hi,'; changed records:',int(winsor.ER_sensitivity.ne(winsor.Engagement_Rate).sum()))
print('Top exposure records excluded:',len(data)-len(exposure))
leave = []
for col in ['Platform','Region']:
    for value in sorted(data[col].unique()):
        leave.append(gap_summary(data.loc[data[col].ne(value)], 'Exclude '+col+': '+value))
leave = pd.DataFrame(leave).set_index('check')
save(leave,'leave_one_segment_out');display(leave.round(3))
thresholds = []
for threshold in [10,30,50]:
    for cols in [['Platform'],['Post_Type'],['Region'],['Month'],['Platform','Post_Type']]:
        row = decomposition(pairs(data,cols,threshold),'_x_'.join(cols))
        row['minimum_n_each'] = threshold
        thresholds.append(row)
thresholds = pd.DataFrame(thresholds)
save(thresholds,'sample_threshold_sensitivity');display(thresholds.round(3))
by_month = pairs(data,['Month'])
save(by_month,'robustness_monthly')
fig, ax = plt.subplots(figsize=(11,4))
ax.plot(by_month.index,by_month.mean_E,marker='o',label='Entertainment')
ax.plot(by_month.index,by_month.mean_R,marker='o',label='Rest: same publication month')
ax.set_ylabel('Mean source ER (%)'); ax.tick_params(axis='x',rotation=50);ax.legend()
fig.tight_layout();fig.savefig(figures/'monthly_gap_robustness.png',dpi=150,bbox_inches='tight')
'''), md('''## Secondary scope: Product Promotion

Chỉ kiểm tra xem secondary gap có còn trong segment cùng platform/post type/region. Không đổi trọng tâm và không xây dựng thêm mô hình giải thích.
'''), code('''secondary = []
for col in ['Platform','Post_Type','Region']:
    for label,g in data.groupby(col):
        a=g.loc[g.Content_Category.eq('Product Promotion')]
        b=g.loc[~g.Content_Category.eq('Product Promotion')]
        secondary.append({'driver':col,'segment':label,'n_product':len(a),'n_rest':len(b),
                          'product_er_pct':a.Engagement_Rate.mean()*100,
                          'rest_er_pct':b.Engagement_Rate.mean()*100,
                          'gap_pp':(b.Engagement_Rate.mean()-a.Engagement_Rate.mean())*100,
                          'eligible':min(len(a),len(b))>=THRESHOLD})
secondary = pd.DataFrame(secondary)
save(secondary,'secondary_product_promotion')
display(secondary.round(3))
print('Primary E gap positive in all eligible Platform/Region/Month cells:')
for col in ['Platform','Region','Month']:
    t=pairs(data,[col]); t=t.loc[t.eligible]
    print(col,len(t),bool(t.gap_pp.gt(0).all()))
''')]
two = execute('02_interaction_and_robustness.ipynb', second)

effects = one['effects']; interactions = two['interaction_effects']
robust = two['robust']; monthly = two['by_month']; leave = two['leave']
joint = interactions.loc['Platform_x_Post_Type']
joint_cells = two['interactions']['Platform_x_Post_Type']
eligible_joint = joint_cells.loc[joint_cells.eligible]
secondary_supported = two['secondary'].loc[two['secondary'].eligible]
post = effects.loc['Post_Type']; tag = effects.loc['Main_Hashtag']
baseline = robust.loc['Full months']
summary = f'''# Root-cause summary — Bước 3

## Kết luận

**ER thấp của Entertainment liên quan mạnh nhất đến khoảng cách gắn với Content Category (category-associated residual), chưa được giải thích bởi các mix quan sát. Post Type mix chỉ giải thích một phần nhỏ trên common support. Khoảng cách vẫn còn khi so trong cùng platform, region và platform × post type; kết quả consistent with phần chênh lệch chưa được giải thích, chưa xác định nguyên nhân business hoặc creative cụ thể.**

Không có bằng chứng để viết “ER thấp chủ yếu vì platform/hashtag/thời điểm”. Primary finding là residual quan sát, không phải category gây ER thấp. Không có target nên đây không phải kết luận không đạt mục tiêu marketing.

## Primary / secondary / unsupported

| Phân loại | Yếu tố / hypothesis | Evidence |
| --- | --- | --- |
| Primary finding | Category-associated residual; driver thực tế chưa xác định | 16 tháng trọn: n=876 Entertainment / 4.714 non-Entertainment; mean source ER {baseline.mean_E_pct:.2f}% vs {baseline.mean_R_pct:.2f}%, gap {baseline.mean_gap_pp:.2f} pp; median gap {baseline.median_gap_pp:.2f} pp |
| Primary finding | Residual trong segment tương đồng | Platform: gap {effects.loc['Platform','min_cell_gap_pp']:.2f}–{effects.loc['Platform','max_cell_gap_pp']:.2f} pp, 6/6 platform. Region: {effects.loc['Region','min_cell_gap_pp']:.2f}–{effects.loc['Region','max_cell_gap_pp']:.2f} pp, 8/8 region |
| Secondary, giải thích một phần nhỏ | Post Type mix | Composition {post.composition_pp:.3f} pp trên {post.eligible_cells:.0f} định dạng đủ mẫu; subset gap {post.supported_subset_gap_pp:.2f} pp; coverage Entertainment {post.coverage_E_pct:.2f}%, Rest {post.coverage_R_pct:.2f}%. Đây không phải phần trăm gap toàn mẫu |
| Secondary, khác biệt mức gap | Platform × Post Type | LinkedIn Video gap 4,00 pp (n=66/33), TikTok Video 10,03 pp (n=193/803). Cả hai vẫn thấp hơn Rest; không phải interaction được xác nhận causal |
| Weak / unsupported | Platform, Content_Type, Region mix | Composition lần lượt {effects.loc['Platform','composition_pp']:.3f}, {effects.loc['Content_Type','composition_pp']:.3f}, {effects.loc['Region','composition_pp']:.3f} pp; không giải thích mức gap khoảng 9 pp |
| Weak / unsupported | Month, Weekday, Hour mix | Composition {effects.loc['Month','composition_pp']:.3f}, {effects.loc['Weekday','composition_pp']:.3f}, {effects.loc['Post_Hour','composition_pp']:.3f} pp trên common support tương ứng; không có tín hiệu timing mix giải thích gap lớn |
| Không tách được effect độc lập | Main hashtag | Chỉ 1 tag có ≥30 record ở cả hai nhóm; coverage Entertainment {tag.coverage_E_pct:.2f}%. #TrendingNow có 515 Entertainment vs 20 Rest; n Rest nhỏ. Không quy kết hashtag là nguyên nhân |

Post Type là secondary yếu về mức giải thích, không phải driver mạnh. Các decomposition phân tích riêng từng chiều, không được cộng lại thành tỷ lệ giải thích chung. Composition âm nghĩa là khác biệt mix đang bù nhẹ gap trên subset, không tạo ra gap.

## Interaction

Platform × Post Type có **{joint.eligible_cells:.0f} cell đủ mẫu**, bao phủ **{joint.coverage_E_pct:.2f}% Entertainment** và **{joint.coverage_R_pct:.2f}% Rest**. Không cell đủ mẫu nào có mean ER Entertainment bằng hoặc cao hơn Rest; gap cell **{joint.min_cell_gap_pp:.2f}–{joint.max_cell_gap_pp:.2f} pp**. Nếu chuẩn hóa Rest theo mix Entertainment trên subset này, gap vẫn **{joint.E_mix_standardized_gap_pp:.2f} pp**.

Composition của joint platform × post type là **{joint.composition_pp:.3f} pp**, within-segment **{joint.within_segment_pp:.2f} pp**, tổng gap subset **{joint.supported_subset_gap_pp:.2f} pp**. Không thấy tổ hợp này giải thích phần lớn gap. Các joint platform × Content_Type, region × post type, post type × Content_Type và platform × hour cũng có bảng coverage/gap riêng; các cell nhỏ được giữ nhưng không overclaim.

Trong 8 cell này, mean ER Entertainment chỉ dao động **{eligible_joint.mean_E.min():.2f}%–{eligible_joint.mean_E.max():.2f}%**, còn Rest **{eligible_joint.mean_R.min():.2f}%–{eligible_joint.mean_R.max():.2f}%**. Mức gap khác nhau đi cùng mức benchmark Rest khác nhau; không đủ chứng minh hiệu ứng interaction độc lập. Platform × hour chỉ có **{interactions.loc['Platform_x_Post_Hour','coverage_E_pct']:.2f}%** Entertainment đủ common support, nên kết luận tổ hợp thời gian bị hạn chế phạm vi.

Platform/Region/Content_Type × Category và Time × Category đều được xuất mean/median, n và volume. Đối chiếu từng category không dùng một benchmark business chung. Không có cell Entertainment “tốt hơn Rest” trong các so sánh chính đủ mẫu; điều này không chứng minh mọi tổ hợp hiếm đều như vậy.

## Robustness

| Kiểm tra | Evidence |
| --- | --- |
| Theo tháng | Gap dương trong 16/16 tháng trọn; khoảng {monthly.gap_pp.min():.2f}–{monthly.gap_pp.max():.2f} pp; tất cả n≥30 mỗi nhóm |
| Mean vs median | Gap {baseline.mean_gap_pp:.2f} vs {baseline.median_gap_pp:.2f} pp; không đổi chiều |
| Thêm tháng partial | Gap {robust.loc['Including partial May','mean_gap_pp']:.2f} pp |
| Giảm trọng số mã lặp | Gap {robust.loc['Each Post_ID total weight=1','mean_gap_pp']:.2f} pp; không deduplicate hoặc chọn category đại diện |
| Winsor ER pooled 1%/99% | Gap {robust.loc['Pooled ER winsor 1%/99% (sensitivity only)','mean_gap_pp']:.2f} pp; chỉ sensitivity, không sửa dataset |
| Loại top 1% Views | Gap {robust.loc['Exclude Views above pooled p99 (sensitivity only)','mean_gap_pp']:.2f} pp; không xem record lớn là lỗi |
| Leave-one-platform / region-out | Gap {leave.mean_gap_pp.min():.2f}–{leave.mean_gap_pp.max():.2f} pp; không phụ thuộc một platform/region duy nhất |

Bảng ngưỡng n=10/30/50 lưu số cell và coverage cho từng phép so. Các gap còn dương trên common support; ngưỡng lớn làm giảm phạm vi, không được diễn giải như kết quả toàn bộ dataset. Không thấy thay đổi mạnh về chiều khoảng cách giữa các sensitivity chính.

## Secondary problem

Product Promotion được kiểm tra riêng trong cùng platform, post type và region với n mỗi nhóm ≥30: gap còn dương trong **{len(secondary_supported)} cell đủ mẫu**, từ **{secondary_supported.gap_pp.min():.2f} đến {secondary_supported.gap_pp.max():.2f} pp**. Evidence lưu tại [bảng secondary](artifacts/tables/secondary_product_promotion.csv). Đây là kiểm tra mô tả giới hạn; không chọn thêm root cause hoặc chuyển trọng tâm khỏi Entertainment.

## Giới hạn

- Observational segment comparison không kiểm soát mọi confounder; không chứng minh category, mix hoặc hashtag gây gap. Không dùng mô hình predictive/prescriptive.
- Công thức source ER chưa xác nhận; chưa biết có quy tắc tạo dữ liệu/nhãn gắn với category hay không. Không thể phân biệt hiệu ứng nội dung thực với cơ chế đo lường từ file này.
- Post_ID lặp, có ID khác category; grain nghiệp vụ và cửa sổ đo chưa rõ. Mean/median là ở cấp record; tổng Views/Impressions/Engagement không được coi là lượng unique post/person.
- Không có creative/caption, audience, follower base, campaign objective, spend, timezone hoặc dữ liệu thử nghiệm; chưa xác định mechanism business/creative.
- Common support hạn chế với tag và một số interaction. Ngưỡng mẫu là rule sàng lọc, không phải kiểm định significance; không suy rộng ra ngoài mẫu.

**Kết thúc bước 3:** driver mix quan sát chưa giải thích phần lớn gap; bằng chứng mạnh nhất là category-associated residual ổn định. Không đưa recommendation, giải pháp hoặc sang bước 4.

**Nguồn:** [Hypotheses](00_hypothesis_setup.md), [Driver notebook](01_hypothesis_and_driver_analysis.ipynb), [Interaction & robustness notebook](02_interaction_and_robustness.ipynb), [Driver effects](artifacts/tables/driver_effect_summary.csv), [Interaction effects](artifacts/tables/interaction_effect_summary.csv), [Robustness](artifacts/tables/robustness_overall.csv).
'''
(OUT/'03_root_cause_summary.md').write_text(summary, encoding='utf-8')
(OUT/'README.md').write_text('''# Bước 3 — Phân tích nguyên nhân

Đọc [root-cause summary](03_root_cause_summary.md) để xem kết luận, evidence và giới hạn. Các mix quan sát chưa giải thích phần lớn khoảng cách ER; category-associated residual là phát hiện chính, không phải nguyên nhân causal được xác nhận.

| Deliverable | Nội dung |
| --- | --- |
| [Hypothesis setup](00_hypothesis_setup.md) | Driver, logic, metric và cách kiểm tra |
| [Driver analysis](01_hypothesis_and_driver_analysis.ipynb) | Single-driver comparisons, record mix, common-support decomposition, hashtag overlap |
| [Interaction & robustness](02_interaction_and_robustness.ipynb) | Joint segments, heatmaps, coverage, sensitivity và secondary problem |
| [Summary](03_root_cause_summary.md) | Primary finding, secondary driver, unsupported hypotheses và giới hạn |
| [Tables](artifacts/tables) / [Figures](artifacts/figures) | Evidence đầy đủ; cell nhỏ vẫn giữ, gắn cờ |

**Tái tạo:** chạy từng notebook từ project root hoặc folder notebook. Hai notebook đọc dataset bước 2 độc lập. Hoặc chạy `python "3. Phân tích nguyên nhân/build_step3.py"` từ project root. Requires Python, pandas, numpy, matplotlib, tabulate; cần `2. Xác định vấn đề/artifacts/analysis_ready.csv` đã tạo ở bước 2.

Chỉ ghi output vào folder bước 3. Không sửa raw/bước 1/2, không recommendation, giải pháp, prescriptive/predictive model hoặc dashboard.
''', encoding='utf-8')
print('Saved Step 3 reports.')
