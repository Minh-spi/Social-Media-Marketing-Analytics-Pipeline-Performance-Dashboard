import plotly.graph_objects as go
import plotly.express as px
from dash import dcc
from components.platforms import PLATFORM_COLORS

BLUE = '#5A6575'
TEAL = '#D49A35'
ENTERTAINMENT = '#C18B2C'
COMPARATOR = '#A4A8B0'


def finish(fig, title, ylabel=None):
    fig.update_layout(template='plotly_white', title={'text': title, 'font': {'size': 17}},
        font={'family': 'Segoe UI, Arial, sans-serif', 'color': '#8492A6','size':11}, paper_bgcolor='white',plot_bgcolor='white',
        margin={'l': 50, 'r': 25, 't': 55, 'b': 55}, height=370,
        colorway=[BLUE, COMPARATOR], legend={'orientation': 'h', 'y': 1.12,'x':0},
        yaxis_title=ylabel, hoverlabel={'font_size': 13})
    fig.update_xaxes(showline=False,zeroline=False,showgrid=False,tickfont={'size':10,'color':'#9CA9BC'},title_font={'size':10})
    fig.update_yaxes(showline=False,zeroline=False,gridcolor='#EEF2F7',tickfont={'size':10,'color':'#9CA9BC'},title_font={'size':10},tickformat='.3s' if ylabel and '%' not in ylabel else None)
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
        fig.update_traces(connectgaps=False,line={'color':'#7387A4','width':2.5},
                          marker={'size':6,'color':'#fff','line':{'color':'#7387A4','width':2}},
                          fill='tozeroy',fillcolor='rgba(115,135,164,0.055)')
    else:
        horizontal = dimension in ['Platform','Content_Category','Post_Type','Content_Type','Region']
        if horizontal:
            args.update(x=metric,y=dimension,orientation='h')
        if dimension == 'Platform':
            fig = px.bar(**args,color=dimension,color_discrete_map=PLATFORM_COLORS)
            fig.update_layout(showlegend=False)
        else:
            fig = px.bar(**args,color_discrete_sequence=[BLUE])
        if horizontal:
            finish(fig,f'{label} by {dimension}')
            fig.update_yaxes(type='category',autorange='reversed',title=None)
            fig.update_xaxes(title=label,tickformat='.3s' if '%' not in label else '.2f')
            return fig
    fig.update_xaxes(type='category')
    return finish(fig, f'{label} by {dimension}', label)
