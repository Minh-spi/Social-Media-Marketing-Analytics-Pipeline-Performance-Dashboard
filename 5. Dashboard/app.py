"""Launch from project root: python \"5. Dashboard/app.py\"."""
from pathlib import Path
import sys

# Optional local dependency directory; never write into prior-stage folders.
LOCAL_DEPS = Path(__file__).resolve().parent / '.deps'
if LOCAL_DEPS.is_dir():
    sys.path.insert(0, str(LOCAL_DEPS))
try:
    from dash import Dash, html, dcc, Input, Output
except ImportError as exc:
    raise SystemExit('Missing Dash dependencies. Run: python -m pip install -r "5. Dashboard/requirements.txt"') from exc

import pandas as pd
from flask import send_file, abort
from utils.data_loader import Repository, ArtifactError, DIMENSIONS, METRICS, SOURCES, filter_frame
from components.filters import layout as filter_layout
from components.cards import notice
from components.platforms import platform_label
from components.icons import icon
from pages import overview, performance, diagnosis, recommendations


def create_app(repository=None):
    repo = repository or Repository()
    app = Dash(__name__, title='Social Media · Performance & Decisions',
               assets_folder=str(Path(__file__).resolve().parent/'assets'),
               update_title='Updating scope…')
    error = None
    try:
        frame = repo.analysis()
    except ArtifactError as exc:
        error = str(exc)
        frame = pd.DataFrame(columns=['Post_Date','Partial_Month',*DIMENSIONS,*METRICS])
        frame['Post_Date'] = pd.to_datetime(frame.Post_Date)
    categories = sorted(frame.Content_Category.dropna().unique())
    app.layout = html.Div([
        html.Aside([
            html.Div([html.Span(icon('performance', color='#ffffff'), className='brand-mark'),
                      html.Div([html.Strong('Social Analytics'), html.Small('MARKETING WORKSPACE')])], className='brand'),
            html.P('WORKSPACE', className='nav-caption'),
            dcc.RadioItems(id='navigation', value='overview', className='sidebar-menu', options=[
                {'label': html.Span([icon('overview', color='#94a3b8'), html.Span('Overview')], className='nav-label'), 'value': 'overview'},
                {'label': html.Span([icon('performance', color='#94a3b8'), html.Span('Performance')], className='nav-label'), 'value': 'performance'},
                {'label': html.Span([icon('diagnosis', color='#94a3b8'), html.Span('Diagnosis')], className='nav-label'), 'value': 'diagnosis'},
                {'label': html.Span([icon('actions', color='#94a3b8'), html.Span('Actions & tests')], className='nav-label'), 'value': 'recommendations'}]),
            html.Div([html.Span('PORTFOLIO PROJECT',className='eyebrow'),html.P('Social Media Marketing Analytics'),
                      html.Small('Evidence from steps 1–4. Read-only exploration.')],className='sidebar-bottom')],className='sidebar'),
        html.Main([
            html.Header([html.Div([html.Span('Workspace',className='breadcrumb'),html.Span(' / ',className='breadcrumb'),
                                  html.Span('Social media marketing',className='breadcrumb current')]),
                         html.Span([html.Span(className='status-dot'), 'Read-only analytics'],className='workspace-status')],className='topbar'),
            notice(error,error=True) if error else html.Div(),
            filter_layout(frame), html.Div(id='scope-label',className='scope'),
            html.Div([overview.layout(),performance.layout(),diagnosis.layout(categories,diagnosis.evidence(repo),diagnosis.problem_summary(repo)),recommendations.layout(repo)],className='page-body'),
            html.Footer([html.P('Source ER/CTR definitions and unique-post grain remain unresolved. '
                               'Observed rates and residuals are not causal effects. No official KPI target.'),
                         html.Details([html.Summary('Source artifacts · download read-only originals'),
                            html.Div([html.A(key.replace('_',' ').title(),href='/source/'+key,target='_blank',rel='noopener noreferrer')
                                      for key in SOURCES],className='source-links')])])
        ],className='workspace')
    ],className='app-shell')

    @app.server.get('/source/<key>')
    def source_download(key):
        # Whitelist only. No user-supplied filesystem paths.
        if key not in SOURCES: abort(404)
        try:
            return send_file(repo.path(key),as_attachment=True)
        except ArtifactError:
            abort(404)

    @app.callback([Output('page-'+name,'style') for name in ['overview','performance','diagnosis','recommendations']],
                  Input('navigation','value'))
    def navigate(page):
        return [{'display':'block' if page==name else 'none'} for name in ['overview','performance','diagnosis','recommendations']]

    filter_inputs = [Input('date-filter','start_date'),Input('date-filter','end_date'),
                     *[Input('filter-'+col,'value') for col in DIMENSIONS]]

    @app.callback(Output('scope-label','children'),Output('overview-content','children'),
                  Output('performance-content','children'),Output('diagnosis-content','children'),
                  *filter_inputs, Input('overview-kpi','value'), Input('performance-dimension','value'),
                  Input('performance-kpi','value'),Input('diagnosis-dimension','value'),
                  Input('diagnosis-comparator','value'),Input('diagnosis-interaction','value'))
    def update_scope(start,end,platform,region,category,post_type,content_type,
                     overview_metric,dimension,performance_metric,diagnosis_dimension,comparator,interaction):
        if error:
            return ('Source unavailable', *[notice(error,error=True) for _ in range(3)])
        try:
            selected = filter_frame(frame,start,end,dict(zip(DIMENSIONS,[platform,region,category,post_type,content_type])))
            label = f'{len(selected):,} / {len(frame):,} source records · publication-date scope'
            return (label,overview.render(selected,overview_metric),
                    performance.render(selected,dimension,performance_metric),
                    diagnosis.render(selected,diagnosis_dimension,comparator,interaction))
        except (ArtifactError,ValueError,KeyError) as exc:
            return ('Selection unavailable', *[notice(f'Cannot display this selection: {exc}',error=True) for _ in range(3)])

    @app.callback(Output('date-filter','start_date'),Output('date-filter','end_date'),
                  *[Output('filter-'+col,'value') for col in DIMENSIONS],Input('reset-filters','n_clicks'),prevent_initial_call=True)
    def reset_filters(_):
        start = frame.Post_Date.min().date().isoformat() if not frame.empty else None
        end = frame.Post_Date.max().date().isoformat() if not frame.empty else None
        return (start,end,*[[] for _ in DIMENSIONS])

    @app.callback(Output('filter-chips','children'),*[Input('filter-'+col,'value') for col in DIMENSIONS])
    def selected_filter_chips(*values):
        chips = [html.Span(platform_label(value) if col=='Platform' else f'{col.replace("_"," ")}: {value}',
                           className='filter-chip') for col,selected in zip(DIMENSIONS,values) for value in selected or []]
        return chips or html.Span('All platforms and segments · filters apply to live charts',className='filter-hint')

    @app.callback(Output('recommendation-content','children'),Input('recommendation-priority','value'),Input('recommendation-type','value'),Input('experiment-select','value'))
    def update_recommendations(priority,action_type,experiment):
        return recommendations.render(repo,priority,action_type,experiment)

    return app


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Read-only portfolio dashboard')
    parser.add_argument('--port',type=int,default=8050)
    args = parser.parse_args()
    create_app().run(host='127.0.0.1',port=args.port,debug=False)
