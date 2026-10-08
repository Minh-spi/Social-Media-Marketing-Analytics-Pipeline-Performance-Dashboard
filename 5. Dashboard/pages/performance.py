from dash import html, dcc
from components.cards import notice, table
from components.charts import graph, metric_chart
from utils.data_loader import aggregate, METRICS, BREAKDOWNS
from components.platforms import platform_legend


def layout():
    return html.Section([html.Span('02 / SEGMENT COMPARISON',className='page-kicker'),html.H2('Performance explorer'),
        html.P('How do volume and recorded rates compare across segments?'),
        html.Div([dcc.Dropdown(id='performance-dimension', options=BREAKDOWNS, value='Content_Category', clearable=False),
                  dcc.Dropdown(id='performance-kpi', options=[{'label': v[0], 'value': k} for k,v in METRICS.items()],
                               value='Engagement_Rate', clearable=False)], className='controls-row'),
        dcc.Loading(html.Div(id='performance-content'))], id='page-performance', style={'display':'none'})


def render(frame, dimension, metric):
    grouped = aggregate(frame, dimension)
    kind = METRICS[metric][1]
    if dimension == 'Weekday':
        order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        grouped = grouped.set_index(dimension).reindex([x for x in order if x in grouped[dimension].values]).reset_index()
    columns = [dimension, 'records', metric, metric+'_n', metric+'_median',
               'Views', 'Engagement', 'Click coverage (%)']
    summary = grouped[list(dict.fromkeys(columns))].rename(columns={metric: METRICS[metric][0],
        metric+'_n':'Valid KPI records', metric+'_median':'Median source rate (%)' if kind=='rate' else 'Median per record'})
    return html.Div([
        html.Div([platform_legend(grouped.Platform.tolist()) if dimension=='Platform' else html.Div(),
                  graph(metric_chart(grouped, dimension, metric, METRICS[metric][0], time=dimension=='Month'))],className='panel'),
        html.Div([html.H3('Segment summary'),html.P('Volume, efficiency and valid sample size',className='muted'),table(summary)],className='panel'),
        html.Details([html.Summary('How to read this comparison'),html.P(
            'Rate comparison = unweighted mean/median source rate at record level; absolute comparison = sum. '
            'Read sample size and exposure alongside rates. Comparisons are descriptive, not causal or a business target.')],className='data-notes')])
