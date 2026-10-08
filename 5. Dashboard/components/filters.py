from dash import dcc, html
from utils.data_loader import DIMENSIONS
from components.platforms import platform_label

LABELS = {'Platform': 'Platform', 'Region': 'Region', 'Content_Category': 'Content Category',
          'Post_Type': 'Post Type', 'Content_Type': 'Content Type'}


def layout(frame):
    dates = frame.Post_Date if not frame.empty else None
    start = dates.min().date().isoformat() if dates is not None else None
    end = dates.max().date().isoformat() if dates is not None else None
    date = html.Div([html.Label('Publication date'), dcc.DatePickerRange(
        id='date-filter', start_date=start, end_date=end, min_date_allowed=start,
        max_date_allowed=end, display_format='DD/MM/YYYY')], className='filter-date')
    controls = {}
    for col in DIMENSIONS:
        options = sorted(frame[col].dropna().unique()) if col in frame else []
        controls[col] = html.Div([html.Label(LABELS[col]), dcc.Dropdown(
            id='filter-'+col, options=[{'label': platform_label(x) if col=='Platform' else x,
                                      'value': x, 'search': x} for x in options],
            value=[], multi=True, placeholder='All '+LABELS[col].lower(),
            persistence=True, persistence_type='memory')],className='filter-field')
    return html.Section([
        html.Div([date,controls['Platform'],html.Button('Reset filters',id='reset-filters',n_clicks=0,className='reset-button')],className='filter-primary'),
        html.Details([html.Summary('More filters'),html.Div([controls[c] for c in DIMENSIONS if c!='Platform'],className='filter-secondary')],className='more-filters'),
        html.Div(id='filter-chips',className='filter-chips')],className='filter-panel')
