import plotly.graph_objects as go
import plotly.express as px
from dash import dcc

BLUE = '#3568df'
TEAL = '#008b80'


def finish(fig, title, ylabel=None):
    fig.update_layout(template='plotly_white', title={'text': title, 'font': {'size': 17}},
        font={'family': 'Arial, sans-serif', 'color': '#243249'}, paper_bgcolor='white',
        margin={'l': 50, 'r': 25, 't': 65, 'b': 65}, height=370,
        colorway=[BLUE, TEAL], legend={'orientation': 'h', 'y': -0.3},
        yaxis_title=ylabel, hoverlabel={'font_size': 13})
    return fig


def empty(title='No matching data'):
    fig = go.Figure()
    fig.add_annotation(text=title, showarrow=False, x=.5, y=.5, xref='paper', yref='paper')
    fig.update_xaxes(visible=False); fig.update_yaxes(visible=False)
    return finish(fig, '')


def graph(fig):
    return dcc.Graph(figure=fig, config={'displaylogo': False, 'responsive': True,
                                       'modeBarButtonsToRemove': ['lasso2d', 'select2d']})


def metric_chart(data, dimension, metric, label, time=False):
    if data.empty or data[metric].notna().sum() == 0:
        return empty('No recorded values for this KPI in the selected scope')
    args = dict(data_frame=data, x=dimension, y=metric,
                hover_data={'records': True, metric+'_n': True},
                labels={'records': 'Records', metric+'_n': 'Valid KPI records', metric: label})
    if time:
        fig = px.line(**args, markers=True)
        fig.update_traces(connectgaps=False)
    else:
        fig = px.bar(**args, color_discrete_sequence=[BLUE])
    fig.update_xaxes(type='category')
    return finish(fig, f'{label} by {dimension}', label)
