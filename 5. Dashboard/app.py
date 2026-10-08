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
        html.Header([html.Div([html.Span('SOCIAL MEDIA ANALYTICS',className='eyebrow'),
                              html.H1('Performance → Evidence → Action'),
                              html.P('Explore the portfolio findings, their limits and the next validation steps.')]),
                     html.Span('READ-ONLY DATA APP',className='badge')],className='hero'),
        html.Main([
            notice(error,error=True) if error else html.Div(),
            filter_layout(frame), html.Div(id='scope-label',className='scope'),
            dcc.Tabs(id='navigation',value='overview',children=[
                dcc.Tab(label='01  Overview',value='overview'),
                dcc.Tab(label='02  Performance',value='performance'),
                dcc.Tab(label='03  Diagnosis',value='diagnosis'),
                dcc.Tab(label='04  Actions & tests',value='recommendations')]),
            html.Div([overview.layout(),performance.layout(),diagnosis.layout(categories,diagnosis.evidence(repo)),recommendations.layout()],className='page-body'),
            html.Footer([html.P('Source ER/CTR definitions and unique-post grain remain unresolved. '
                               'Observed rates and residuals are not causal effects. No official KPI target.'),
                         html.Details([html.Summary('Source artifacts · download read-only originals'),
                            html.Div([html.A(key.replace('_',' ').title(),href='/source/'+key,target='_blank',rel='noopener noreferrer')
                                      for key in SOURCES],className='source-links')])])
        ])
    ])

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

    @app.callback(Output('recommendation-content','children'),Input('recommendation-priority','value'),Input('recommendation-type','value'))
    def update_recommendations(priority,action_type):
        return recommendations.render(repo,priority,action_type)

    return app


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Read-only portfolio dashboard')
    parser.add_argument('--port',type=int,default=8050)
    args = parser.parse_args()
    create_app().run(host='127.0.0.1',port=args.port,debug=False)
