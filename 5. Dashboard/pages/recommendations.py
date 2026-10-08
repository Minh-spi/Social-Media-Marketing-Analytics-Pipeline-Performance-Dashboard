from dash import html, dcc
from components.cards import notice, card, table
from utils.data_loader import ArtifactError, markdown_for_app


def layout():
    return html.Section([html.H2('Recommendations & experiments'),
        notice('Step 4 plans, not completed experiments. Global data filters do not change priorities or create new recommendations.'),
        html.Div([dcc.Dropdown(id='recommendation-priority',options=['All','High','Medium','Low'],value='All',clearable=False),
                  dcc.Dropdown(id='recommendation-type', options=['All','Direct action','Test-first','Test-first deferred'],
                               value='All',clearable=False)],className='controls-row'),
        html.Div(id='recommendation-content')],id='page-recommendations',style={'display':'none'})


def render(repo, priority, action_type):
    parts = []
    try:
        recommendations = repo.csv('recommendations')
        required = {'priority','action_type','recommendation_id','total_score','action','evidence','confidence','risk_limitation'}
        if not required.issubset(recommendations.columns):
            raise ArtifactError('Recommendation matrix schema is incompatible.')
        parts.append(html.Div([card(level, str(recommendations.priority.eq(level).sum()), 'Saved priority')
                              for level in ['High','Medium','Low']],className='kpi-grid'))
        selected = recommendations
        if priority!='All': selected=selected.loc[selected.priority.eq(priority)]
        if action_type!='All': selected=selected.loc[selected.action_type.eq(action_type)]
        parts.append(html.Div([html.H3('Action matrix'),table(selected)],className='panel'))
    except ArtifactError as exc:
        parts.append(notice(str(exc),error=True))
    try:
        experiments = repo.csv('experiments')
        parts.append(html.Div([html.H3('Experiment registration · design fields remain TBD'),table(experiments,5)],className='panel'))
    except ArtifactError as exc:
        parts.append(notice(str(exc),error=True))
    for key,title in [('experiment_plan','Treatment, control, KPIs & scale / stop / iterate rules'),
                      ('measurement_plan','Measurement framework, owners & action roadmap')]:
        try:
            parts.append(html.Details([html.Summary(title),dcc.Markdown(markdown_for_app(repo.text(key)),className='prose')],open=key=='experiment_plan'))
        except ArtifactError as exc:
            parts.append(notice(str(exc),error=True))
    return html.Div(parts)
