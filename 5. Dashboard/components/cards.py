import pandas as pd
from dash import html, dash_table


def number(value, rate=False):
    if pd.isna(value):
        return 'N/A'
    return f'{value:,.2f}%' if rate else f'{value:,.0f}'


def card(label, value, note=''):
    return html.Div([html.Div(label, className='card-label'), html.Strong(value, className='card-value'),
                     html.Small(note)], className='kpi-card')


def notice(text, error=False):
    return html.Div(text, className='notice error' if error else 'notice', role='alert' if error else 'note')


def table(frame, page_size=10):
    clean = frame.copy()
    for col in clean.select_dtypes('number').columns:
        clean[col] = clean[col].round(3)
    clean = clean.astype(object).where(pd.notna(clean), None)
    return dash_table.DataTable(
        data=clean.to_dict('records'), columns=[{'name': c, 'id': c} for c in clean.columns],
        page_size=page_size, sort_action='native', filter_action='native',
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'fontFamily': 'inherit', 'fontSize': 13,
                    'padding': '12px', 'minWidth': '90px', 'maxWidth': '420px',
                    'whiteSpace': 'normal', 'height': 'auto'},
        style_header={'fontWeight': '600', 'backgroundColor': '#eef3f8', 'border': 'none'},
        style_data={'border': 'none', 'borderBottom': '1px solid #e8edf3'},
        style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#f8fafc'}])
