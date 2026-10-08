from dash import html, dcc
import pandas as pd
from components.cards import notice, card, table
from utils.data_loader import ArtifactError, markdown_for_app


def layout(repo=None):
    try:
        ids = repo.csv('experiments').experiment_id.tolist() if repo else []
    except (ArtifactError,AttributeError):
        ids = []
    return html.Section([html.Span('04 / ACTION & VALIDATION',className='page-kicker'),html.H2('Recommendations & experiments'),
        notice('Step 4 plans, not completed experiments. Global data filters do not change priorities or create new recommendations.'),
        html.Div([dcc.Dropdown(id='recommendation-priority',options=['All','High','Medium','Low'],value='All',clearable=False),
                  dcc.Dropdown(id='recommendation-type', options=['All','Direct action','Test-first','Test-first deferred'],
                               value='All',clearable=False)],className='controls-row'),
        html.Div([html.Label('Experiment plan'),dcc.Dropdown(id='experiment-select',options=ids,
                    value=ids[0] if ids else None,clearable=False)],className='experiment-picker'),
        html.Div(id='recommendation-content')],id='page-recommendations',style={'display':'none'})


def experiment_card(row):
    fields = [('Hypothesis','hypothesis'),('Treatment','treatment'),('Control','control'),
              ('Primary KPI','primary_kpi'),('Supporting KPI','secondary_kpi'),('Guardrails','guardrails')]
    return html.Div([html.Div([html.H3(str(row.get('experiment_id','Experiment'))),
                             html.Span(str(row.get('status','Planned')),className='pill')],className='section-title'),
                    html.Div([html.Div([html.H4(label),html.P(str(row.get(field,'Not provided')))]) for label,field in fields],className='experiment-grid'),
                    html.Div([html.H4('Validation readiness'),html.P(str(row.get('measurement_window','Not provided'))),
                              html.P('Minimum uplift: '+str(row.get('delta_min_pp','TBD'))+
                                     ' · Sample per arm: '+str(row.get('sample_size_each_arm','TBD')))],className='experiment-readiness')],className='panel experiment-card')


def render(repo, priority, action_type, experiment=None):
    parts = []
    try:
        recommendations = repo.csv('recommendations')
        required = {'priority','action_type','recommendation_id','total_score','action','evidence','confidence','risk_limitation'}
        if not required.issubset(recommendations.columns):
            raise ArtifactError('Recommendation matrix schema is incompatible.')
        parts.append(html.Div([card(level, str(recommendations.priority.eq(level).sum()), 'Saved priority')
                              for level in ['High','Medium','Low']],className='kpi-grid priority-kpis'))
        selected = recommendations
        if priority!='All': selected=selected.loc[selected.priority.eq(priority)]
        if action_type!='All': selected=selected.loc[selected.action_type.eq(action_type)]
        action_cards = []
        for _,row in selected.iterrows():
            action_cards.append(html.Article([
                html.Div([html.Span(row.recommendation_id,className='action-id'),
                          html.Div([html.Span(row.priority+' priority',className='pill priority-'+row.priority.lower()),
                                    html.Span(row.action_type,className='pill')],className='action-badges')],className='section-title'),
                html.H3(row.action),html.P(row.evidence,className='muted'),
                html.Details([html.Summary('Evidence, confidence & limits'),
                    html.H4('Expected effect'),html.P(row.get('expected_effect','Not provided')),
                    html.H4('Confidence'),html.P(row.confidence),html.H4('Risk / limitation'),html.P(row.risk_limitation),
                    html.H4('Dependency'),html.P(row.get('dependency','Not provided')),
                    html.Small('Linked experiment: '+('Direct action' if pd.isna(row.get('experiment_id')) or not row.get('experiment_id')
                                                      else str(row.get('experiment_id'))))])],className='action-card'))
        parts.append(html.Div(action_cards,className='action-grid'))
        if selected.empty:
            parts.append(notice('No recommendations match these selections.'))
        parts.append(html.Details([html.Summary('Full recommendation matrix'),table(selected)]))
    except ArtifactError as exc:
        parts.append(notice(str(exc),error=True))
    try:
        experiments = repo.csv('experiments')
        if not experiments.empty:
            selected_experiment = experiments.loc[experiments.experiment_id.eq(experiment)]
            row = selected_experiment.iloc[0] if not selected_experiment.empty else experiments.iloc[0]
            parts.append(experiment_card(row))
        parts.append(html.Details([html.Summary('Full experiment registration · design fields remain TBD'),table(experiments,5)]))
    except ArtifactError as exc:
        parts.append(notice(str(exc),error=True))
    for key,title in [('experiment_plan','Treatment, control, KPIs & scale / stop / iterate rules'),
                      ('measurement_plan','Measurement framework, owners & action roadmap')]:
        try:
            text = repo.text(key)
            if key=='experiment_plan' and '## Validation và decision rules' in text:
                rules = text.split('## Validation và decision rules',1)[1]
                parts.append(html.Div([html.H3('Scale / Stop / Iterate'),dcc.Markdown(markdown_for_app(rules),className='prose')],className='panel'))
            parts.append(html.Details([html.Summary(title),dcc.Markdown(markdown_for_app(text),className='prose')]))
        except ArtifactError as exc:
            parts.append(notice(str(exc),error=True))
    return html.Div(parts)
