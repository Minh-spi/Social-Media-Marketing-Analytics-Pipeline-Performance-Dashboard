from dash import dcc, html
from utils.data_loader import DIMENSIONS

LABELS = {'Platform': 'Platform', 'Region': 'Region', 'Content_Category': 'Content Category',
          'Post_Type': 'Post Type', 'Content_Type': 'Content Type'}


def layout(frame):
    dates = frame.Post_Date if not frame.empty else None
    start = dates.min().date().isoformat() if dates is not None else None
    end = dates.max().date().isoformat() if dates is not None else None
    controls = [html.Div([html.Label('Publication date'), dcc.DatePickerRange(
        id='date-filter', start_date=start, end_date=end, min_date_allowed=start,
        max_date_allowed=end, display_format='DD/MM/YYYY')], className='filter-date')]
    for col in DIMENSIONS:
        options = sorted(frame[col].dropna().unique()) if col in frame else []
        controls.append(html.Div([html.Label(LABELS[col]), dcc.Dropdown(
            id='filter-'+col, options=[{'label': x, 'value': x} for x in options],
            value=[], multi=True, placeholder='All', persistence=True, persistence_type='memory')]))
    return html.Section([html.Div([html.H3('Explore your scope'), html.Button('Reset', id='reset-filters', n_clicks=0)],
                                  className='section-title'), html.Div(controls, className='filter-grid'),
                         html.Small('Clear a selection to include all values. Filters apply to live charts; saved evidence and plans keep their original scope.')],
                        className='panel filter-panel')
