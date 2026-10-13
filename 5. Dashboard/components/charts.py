import plotly.graph_objects as go
import plotly.express as px
from dash import dcc
from components.platforms import PLATFORM_COLORS

BLUE = '#4F46E5'
TEAL = '#06B6D4'
ENTERTAINMENT = '#F59E0B'
COMPARATOR = '#94A3B8'


def finish(fig, title, ylabel=None):
    fig.update_layout(
        template='plotly_white',
        title={'text': f'<b>{title}</b>' if title else '', 'font': {'size': 15, 'color': '#0F172A', 'family': 'Plus Jakarta Sans, Inter, Segoe UI, sans-serif'}},
        font={'family': 'Plus Jakarta Sans, Inter, Segoe UI, sans-serif', 'color': '#64748B', 'size': 11},
        paper_bgcolor='white', plot_bgcolor='white',
        margin={'l': 55, 'r': 25, 't': 55, 'b': 55}, height=380,
        colorway=[BLUE, COMPARATOR],
        legend={'orientation': 'h', 'y': 1.14, 'x': 0, 'font': {'size': 11, 'color': '#334155'}},
        yaxis_title=ylabel,
        hoverlabel={'bgcolor': '#0F172A', 'font_size': 12, 'font_color': '#FFFFFF', 'bordercolor': '#1E293B', 'font_family': 'Plus Jakarta Sans, Inter, Segoe UI, sans-serif'}
    )
    fig.update_xaxes(showline=True, linecolor='#E2E8F0', zeroline=False, showgrid=False,
                     tickfont={'size': 10, 'color': '#64748B', 'family': 'Plus Jakarta Sans, Inter, Segoe UI, sans-serif'},
                     title_font={'size': 11, 'color': '#475569'})
    fig.update_yaxes(showline=False, zeroline=False, gridcolor='#F1F5F9',
                     tickfont={'size': 10, 'color': '#64748B', 'family': 'Plus Jakarta Sans, Inter, Segoe UI, sans-serif'},
                     title_font={'size': 11, 'color': '#475569'},
                     tickformat='.3s' if ylabel and '%' not in ylabel else None)
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
        fig.update_traces(connectgaps=False, line={'color': BLUE, 'width': 3, 'shape': 'spline'},
                          marker={'size': 7, 'color': '#FFFFFF', 'line': {'color': BLUE, 'width': 2.5}},
                          fill='tozeroy', fillcolor='rgba(79, 70, 229, 0.08)')
    else:
        horizontal = dimension in ['Platform','Content_Category','Post_Type','Content_Type','Region']
        if horizontal:
            args.update(x=metric, y=dimension, orientation='h')
        if dimension == 'Platform':
            fig = px.bar(**args, color=dimension, color_discrete_map=PLATFORM_COLORS)
            fig.update_layout(showlegend=False)
            fig.update_traces(marker=dict(cornerradius=6))
        else:
            fig = px.bar(**args, color_discrete_sequence=[BLUE])
            fig.update_traces(marker=dict(cornerradius=6))
        if horizontal:
            finish(fig, f'{label} by {dimension}')
            fig.update_yaxes(type='category', autorange='reversed', title=None)
            fig.update_xaxes(title=label, tickformat='.3s' if '%' not in label else '.2f')
            return fig
    fig.update_xaxes(type='category')
    return finish(fig, f'{label} by {dimension}', label)
