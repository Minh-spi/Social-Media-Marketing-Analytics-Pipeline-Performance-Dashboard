from dash import html, dcc
from components.cards import card, notice, number
from components.charts import graph, metric_chart
from utils.data_loader import summarize, aggregate, METRICS


def layout():
    return html.Section([html.Div([html.Div([html.Span('01 / PERFORMANCE SNAPSHOT',className='page-kicker'),html.H2('Executive overview'),
        html.P('How much exposure, engagement and action are recorded?')]),
        dcc.Dropdown(id='overview-kpi', options=[{'label': v[0], 'value': k} for k, v in METRICS.items()],
                     value='Views', clearable=False, className='control')], className='section-title'),
        dcc.Loading(html.Div(id='overview-content'))], id='page-overview')


def render(frame, metric):
    stats = summarize(frame)
    colors = {
        'Views': '#2563eb',
        'Impressions': '#6366f1',
        'Engagement': '#059669',
        'Engagement_Rate': '#d97706'
    }
    cards = []
    for key in ['Views','Impressions','Engagement','Engagement_Rate']:
        label,kind = METRICS[key]
        cards.append(card(label.replace(' (%)',''),number(stats[key],kind=='rate',compact=True),
                          f"{stats[key+'_n']:,} valid records"+(' · mean rate' if kind=='rate' else ' · record sum'),
                          full_value=number(stats[key],kind=='rate'),
                          icon_name={'Views':'eye','Impressions':'impressions','Engagement':'engagement','Engagement_Rate':'rate'}[key],
                          icon_color=colors[key]))
    coverage = stats['Clicks_n']/len(frame)*100 if len(frame) else float('nan')
    support = [card('Records',number(stats['records']),'Source rows, not unique posts'),
               card('Observed clicks',number(stats['Clicks'],compact=True),'Missing records excluded',full_value=number(stats['Clicks'])),
               card('Mean source CTR',number(stats['Click_Through_Rate'],True),f"{stats['Click_Through_Rate_n']:,} valid records"),
               card('Click coverage',number(coverage,True),f"{stats['Clicks_n']:,} / {len(frame):,} records")]
    trend = aggregate(frame, 'Month')
    partial = sorted(frame.loc[frame.Partial_Month, 'Month'].unique())
    note = 'Monthly publication cohorts; unknown performance measurement window. '
    if partial:
        note += 'Partial source month: '+', '.join(partial)+'. '
    note += 'Selected date boundaries may truncate other months; totals are not normalized for posting volume.'
    return html.Div([html.Div(cards, className='kpi-grid primary-kpis'),html.Div(support,className='support-kpis'),
        html.Div([html.Div([html.Div([html.H3('Performance over time'),html.P('Explore monthly publication cohorts',className='muted')]),
                           html.Span('MONTHLY',className='pill')],className='chart-heading'),
                  graph(metric_chart(trend, 'Month', metric, METRICS[metric][0], time=True)),
                  html.P('Publication-month cohorts · selected scope',className='chart-footnote')], className='panel'),
        html.Details([html.Summary('Data definitions & coverage'),
                      html.P('Absolute KPI = record sum. ER/CTR = mean source rate, not ratio of totals. Missing Clicks/CTR remain N/A.'),
                      html.P(note)],className='data-notes'),
        notice('No matching records. Adjust the filters.') if frame.empty else html.Div()])
