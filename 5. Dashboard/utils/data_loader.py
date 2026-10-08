"""Read previous-stage artifacts without copying or rewriting them."""
from functools import lru_cache
from pathlib import Path
import re
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
METRICS = {
    'Impressions': ('Impressions', 'absolute'),
    'Views': ('Views', 'absolute'),
    'Engagement': ('Engagement', 'absolute'),
    'Engagement_Rate': ('Mean source ER (%)', 'rate'),
    'Clicks': ('Clicks · observed only', 'absolute'),
    'Click_Through_Rate': ('Mean source CTR (%) · observed only', 'rate'),
}
DIMENSIONS = ['Platform', 'Region', 'Content_Category', 'Post_Type', 'Content_Type']
BREAKDOWNS = ['Platform', 'Content_Category', 'Post_Type', 'Content_Type', 'Region',
              'Month', 'Weekday', 'Post_Hour']
SOURCES = {
    'analysis': ('2.', 'artifacts/analysis_ready.csv'),
    'baseline': ('2.', 'artifacts/tables/baseline.csv'),
    'problem': ('2.', '03_problem_statement.md'),
    'root_cause': ('3.', '03_root_cause_summary.md'),
    'drivers': ('3.', 'artifacts/tables/driver_effect_summary.csv'),
    'interactions': ('3.', 'artifacts/tables/interaction_effect_summary.csv'),
    'robustness': ('3.', 'artifacts/tables/robustness_overall.csv'),
    'recommendations': ('4.', 'artifacts/recommendation_matrix.csv'),
    'experiments': ('4.', 'artifacts/experiment_registration_template.csv'),
    'experiment_plan': ('4.', '03_experiment_plan.md'),
    'measurement_plan': ('4.', '04_measurement_and_action_plan.md'),
}


class ArtifactError(ValueError):
    """A readable error for missing or incompatible source files."""


class Repository:
    def __init__(self, root=PROJECT_ROOT):
        self.root = Path(root)

    def path(self, key):
        if key not in SOURCES:
            raise ArtifactError('Unknown artifact.')
        prefix, relative = SOURCES[key]
        folders = [p for p in self.root.iterdir() if p.is_dir() and p.name.startswith(prefix)]
        if len(folders) != 1:
            raise ArtifactError(f'Expected one folder starting with {prefix}')
        path = folders[0] / relative
        if not path.is_file():
            raise ArtifactError(f'Missing source: {folders[0].name}/{relative}')
        return path

    @lru_cache(maxsize=16)
    def csv(self, key):
        try:
            return pd.read_csv(self.path(key)).drop(columns=['Unnamed: 0'], errors='ignore')
        except (OSError, pd.errors.ParserError, pd.errors.EmptyDataError, UnicodeError) as exc:
            raise ArtifactError(f'Cannot read {key}: {exc}') from exc

    @lru_cache(maxsize=16)
    def text(self, key):
        try:
            return self.path(key).read_text(encoding='utf-8')
        except (OSError, UnicodeError) as exc:
            raise ArtifactError(f'Cannot read {key}: {exc}') from exc

    @lru_cache(maxsize=1)
    def analysis(self):
        frame = self.csv('analysis').copy()
        required = ['Source_Row', 'Post_ID', 'Post_Date', 'Month', 'Weekday', 'Post_Hour',
                    'Partial_Month', *DIMENSIONS, *METRICS,
                    *['Invalid_' + metric for metric in METRICS]]
        missing = sorted(set(required) - set(frame.columns))
        if missing:
            raise ArtifactError('Analysis-ready schema missing: ' + ', '.join(missing))
        try:
            frame['Post_Date'] = pd.to_datetime(frame.Post_Date, errors='raise')
            if frame.Post_Date.isna().any() or not frame.Source_Row.is_unique:
                raise ValueError('Invalid publication dates or duplicate Source_Row')
            for field in ['Partial_Month', *['Invalid_' + m for m in METRICS]]:
                values = frame[field].astype(str).str.lower()
                if not values.isin(['true', 'false']).all():
                    raise ValueError(f'Invalid boolean field: {field}')
                frame[field] = values.eq('true')
            for metric in METRICS:
                frame[metric] = pd.to_numeric(frame[metric], errors='raise')
                # Same KPI-specific masks as Step 2; never mutate source files.
                frame.loc[frame['Invalid_' + metric], metric] = float('nan')
        except (ValueError, TypeError) as exc:
            raise ArtifactError(f'Invalid analysis-ready schema: {exc}') from exc
        return frame


def filter_frame(frame, start=None, end=None, selections=None):
    mask = pd.Series(True, index=frame.index)
    start = pd.Timestamp(start).normalize() if start else None
    end = pd.Timestamp(end).normalize() if end else None
    if start is not None and end is not None and start > end:
        raise ArtifactError('Start date must be on or before end date.')
    if start is not None:
        mask &= frame.Post_Date >= start
    if end is not None:
        mask &= frame.Post_Date < end + pd.Timedelta(days=1)
    for col, selected in (selections or {}).items():
        if col not in DIMENSIONS:
            raise ArtifactError('Invalid filter dimension.')
        if selected:  # clearing a multi-select means all values
            mask &= frame[col].isin(selected)
    return frame.loc[mask].copy()


def summarize(frame):
    result = {'records': len(frame)}
    for metric, (_, kind) in METRICS.items():
        values = frame[metric]
        result[metric] = values.mean() * 100 if kind == 'rate' else values.sum(min_count=1)
        result[metric + '_n'] = int(values.count())
        result[metric + '_median'] = values.median() * (100 if kind == 'rate' else 1) if values.notna().any() else float('nan')
    return result


def aggregate(frame, dimension):
    if dimension not in BREAKDOWNS:
        raise ArtifactError('Invalid breakdown dimension.')
    rows = [{dimension: name, **summarize(g)} for name, g in frame.groupby(dimension, dropna=False)]
    result = pd.DataFrame(rows, columns=[dimension, *summarize(frame).keys()])
    result['Click coverage (%)'] = result.Clicks_n / result.records * 100
    return result


def diagnostic_pairs(frame, dimensions, comparator='Rest'):
    """Repeat existing descriptive gap aggregation only, not root-cause analysis."""
    full = frame.loc[~frame.Partial_Month]
    rows = []
    for key, segment in full.groupby(dimensions, dropna=False):
        keys = key if isinstance(key, tuple) else (key,)
        a = segment.loc[segment.Content_Category.eq('Entertainment'), 'Engagement_Rate'].dropna()
        other = ~segment.Content_Category.eq('Entertainment') if comparator == 'Rest' else segment.Content_Category.eq(comparator)
        b = segment.loc[other, 'Engagement_Rate'].dropna()
        rows.append({**dict(zip(dimensions, keys)), 'n Entertainment': len(a), 'n Comparator': len(b),
                     'Entertainment ER (%)': a.mean()*100, 'Comparator ER (%)': b.mean()*100,
                     'Gap (pp)': (b.mean()-a.mean())*100, 'Supported (n≥30 each)': min(len(a), len(b)) >= 30})
    return pd.DataFrame(rows, columns=[*dimensions, 'n Entertainment', 'n Comparator',
        'Entertainment ER (%)', 'Comparator ER (%)', 'Gap (pp)', 'Supported (n≥30 each)'])


def markdown_for_app(text):
    # Source links are exposed separately through a whitelist; avoid broken relative links.
    return re.sub(r'\[([^\]]+)\]\((?!https?://)[^)]+\)', r'\1', text)
