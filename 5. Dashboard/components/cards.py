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


def card(label, value, note='', full_value=None, icon_name=None, icon_color='#64748b'):
    top = html.Div([html.Div(label, className='card-label'), html.Span(icon(icon_name, color=icon_color), className='metric-icon')], className='card-top') if icon_name else html.Div(label, className='card-label')
    return html.Div([top, html.Strong(value, className='card-value'),
                     html.Small(note)], className='kpi-card', title=full_value or value)


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
        style_table={'overflowX': 'auto', 'borderRadius': '12px', 'border': '1px solid #e2e8f0'},
        style_cell={'textAlign': 'left', 'fontFamily': 'inherit', 'fontSize': 13,
                    'padding': '12px 16px', 'minWidth': '90px', 'maxWidth': '420px',
                    'whiteSpace': 'normal', 'height': 'auto', 'color': '#1e293b'},
        style_header={'fontWeight': '700', 'backgroundColor': '#f8fafc', 'border': 'none',
                      'borderBottom': '2px solid #e2e8f0', 'color': '#475569', 'fontSize': 12,
                      'textTransform': 'uppercase', 'letterSpacing': '0.04em', 'padding': '14px 16px'},
        style_data={'border': 'none', 'borderBottom': '1px solid #f1f5f9'},
        style_data_conditional=[{'if': {'row_index': 'odd'}, 'backgroundColor': '#fbfcfd'},
                                {'if': {'state': 'selected'}, 'backgroundColor': '#eef2ff'}])
