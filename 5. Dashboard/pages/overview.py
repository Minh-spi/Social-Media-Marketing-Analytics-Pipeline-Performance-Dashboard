from dash import html, dcc
from components.cards import card, notice, number
from components.charts import graph, metric_chart
from utils.data_loader import summarize, aggregate, METRICS


def layout():
    return html.Section([html.Div([html.Div([html.H2('Executive overview'),
        html.P('How much exposure, engagement and action are recorded?')]),
        dcc.Dropdown(id='overview-kpi', options=[{'label': v[0], 'value': k} for k, v in METRICS.items()],
                     value='Views', clearable=False, className='control')], className='section-title'),
        dcc.Loading(html.Div(id='overview-content'))], id='page-overview')


def render(frame, metric):
    stats = summarize(frame)
    cards = [card('Records', number(stats['records']), 'Source rows; not unique posts')]
    for key, (label, kind) in METRICS.items():
        cards.append(card(label, number(stats[key], kind == 'rate'),
                          f"{stats[key+'_n']:,} / {len(frame):,} valid records"))
    trend = aggregate(frame, 'Month')
    partial = sorted(frame.loc[frame.Partial_Month, 'Month'].unique())
    note = 'Monthly publication cohorts; unknown performance measurement window. '
    if partial:
        note += 'Partial source month: '+', '.join(partial)+'. '
    note += 'Selected date boundaries may truncate other months; totals are not normalized for posting volume.'
    return html.Div([html.Div(cards, className='kpi-grid'),
        notice('Absolute KPI = record sum. ER/CTR = mean source rate, not ratio of totals. Missing Clicks/CTR remain N/A.'),
        html.Div([graph(metric_chart(trend, 'Month', metric, METRICS[metric][0], time=True)),
                  html.P(note, className='muted')], className='panel'),
        notice('No matching records. Adjust the filters.') if frame.empty else html.Div()])
