import pandas as pd
from dash import html, dash_table
from components.icons import icon


def number(value, rate=False, compact=False):
    if pd.isna(value):
        return 'N/A'
    if rate:
        return f'{value:,.2f}%'
    if compact:
        for divisor, suffix in [(1e9,'B'),(1e6,'M'),(1e3,'K')]:
            if abs(value) >= divisor:
                return f'{value/divisor:,.2f}{suffix}'
    return f'{value:,.0f}'


def card(label, value, note='', full_value=None, icon_name=None):
    top = html.Div([html.Div(label,className='card-label'),html.Span(icon(icon_name),className='metric-icon')],className='card-top') if icon_name else html.Div(label,className='card-label')
    return html.Div([top, html.Strong(value, className='card-value'),
                     html.Small(note)], className='kpi-card',title=full_value or value)


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
        style_header={'fontWeight': '600', 'backgroundColor': '#f5f5f5', 'border': 'none','color':'#414141'},
        style_data={'border': 'none', 'borderBottom': '1px solid #e8edf3'},
        style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#fafafa'}])
