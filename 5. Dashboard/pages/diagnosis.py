from dash import html, dcc
import plotly.graph_objects as go
from components.cards import notice, table
from components.charts import graph, finish, empty, ENTERTAINMENT, COMPARATOR
from components.platforms import platform_legend
from utils.data_loader import diagnostic_pairs, markdown_for_app, ArtifactError


def layout(categories, saved_evidence=None, problem=None):
    comparators = [{'label':'All non-Entertainment', 'value':'Rest'}] + [
        {'label': c, 'value': c} for c in categories if c!='Entertainment']
    return html.Section([html.Span('03 / DIAGNOSTIC EVIDENCE',className='page-kicker'),html.H2('Problem diagnosis'),
        problem,
        notice('Association / diagnostic evidence. Residual is not a causal effect. '
               'Live gap charts use filters and full source months only. Saved evidence below retains the Step 3 scope.'),
        html.Div([dcc.Dropdown(id='diagnosis-dimension', options=['Month','Platform','Post_Type','Region','Content_Type'],
                              value='Month', clearable=False),
                  dcc.Dropdown(id='diagnosis-comparator', options=comparators, value='Rest', clearable=False),
                  dcc.Dropdown(id='diagnosis-interaction', options=[
                      {'label':'Platform × Post Type','value':'Platform|Post_Type'},
                      {'label':'Platform × Content Type','value':'Platform|Content_Type'},
                      {'label':'Region × Post Type','value':'Region|Post_Type'}],
                      value='Platform|Post_Type', clearable=False)], className='controls-row'),
        dcc.Loading(html.Div(id='diagnosis-content')), html.Div(saved_evidence,id='diagnosis-evidence')],
        id='page-diagnosis', style={'display':'none'})


def render(frame, dimension, comparator, interaction):
    comparison = diagnostic_pairs(frame, [dimension], comparator)
    supported = comparison.loc[comparison['Supported (n≥30 each)']]
    if supported.empty:
        fig = empty('No common support: both groups need ≥30 recorded ER values per segment')
    else:
        fig = go.Figure()
        for col, label, color in [('Entertainment ER (%)', 'Entertainment', ENTERTAINMENT), ('Comparator ER (%)', comparator, COMPARATOR)]:
            if dimension == 'Month':
                fig.add_scatter(x=supported[dimension], y=supported[col], name=label, mode='lines+markers',
                                line={'color': color, 'width': 3, 'shape': 'spline'},
                                marker={'size': 7, 'color': '#ffffff', 'line': {'color': color, 'width': 2}})
            else:
                fig.add_bar(x=supported[dimension], y=supported[col], name=label, marker_color=color, marker=dict(cornerradius=5))
        finish(fig, f'Entertainment vs {comparator} · same {dimension}', 'Mean source ER (%)')
        fig.update_layout(barmode='group'); fig.update_xaxes(type='category')
    axes = interaction.split('|')
    joint = diagnostic_pairs(frame, axes, comparator)
    eligible = joint.loc[joint['Supported (n≥30 each)']]
    if eligible.empty:
        heatmap = empty('No joint cells with sufficient common support')
    else:
        pivot = eligible.pivot(index=axes[0], columns=axes[1], values='Gap (pp)')
        heatmap = go.Figure(go.Heatmap(z=pivot.values, x=pivot.columns, y=pivot.index,
            colorscale=[[0, '#eff6ff'], [0.35, '#fde68a'], [0.7, '#f97316'], [1, '#dc2626']], text=pivot.round(2).values, texttemplate='%{text}',
            hovertemplate='%{y} / %{x}<br>Comparator − Entertainment: %{z:.2f} pp<extra></extra>',
            hoverongaps=False, colorbar={'title': 'Gap (pp)'}))
        finish(heatmap, 'Where does the recorded ER gap remain?'); heatmap.update_layout(height=410)
    subset = frame.loc[~frame.Partial_Month]
    e_count = subset.Content_Category.eq('Entertainment').sum()
    r_count = (~subset.Content_Category.eq('Entertainment')).sum() if comparator=='Rest' else subset.Content_Category.eq(comparator).sum()
    return html.Div([notice(f'Selected full-month scope: {e_count:,} Entertainment / {r_count:,} comparator records. '
        'A Content Category filter can remove either group; missing support is not zero gap. '
        'n≥30 is the existing descriptive screening rule, not a significance threshold.'),
        html.Div([html.Div([platform_legend(supported[dimension].tolist()) if dimension=='Platform' else html.Div(),graph(fig)],className='panel'),
                  html.Div(graph(heatmap),className='panel')],className='two-columns'),
        html.Details([html.Summary('Segment sample sizes and gaps'),table(comparison),table(joint)])])


def evidence(repo):
    parts = [html.H3('Saved evidence'),html.P('Original Step 3 scope · independent of live filters',className='muted')]
    for key, title in [('drivers','Driver mix decomposition'), ('interactions','Interaction coverage'),
                       ('robustness','Robustness checks')]:
        try:
            parts.append(html.Details([html.Summary(title),table(repo.csv(key))]))
        except ArtifactError as exc:
            parts.append(notice(str(exc),error=True))
    for key, title in [('problem','Problem statement · Step 2'), ('root_cause','Root-cause synthesis, unsupported hypotheses & limitations')]:
        try:
            parts.append(html.Details([html.Summary(title),dcc.Markdown(markdown_for_app(repo.text(key)),className='prose')]))
        except ArtifactError as exc:
            parts.append(notice(str(exc),error=True))
    return html.Div(parts,className='panel')


def problem_summary(repo):
    try:
        text = repo.text('problem').split('## Kết luận chính',1)[1].split('\n## ',1)[0]
        return html.Div([html.Span('ESTABLISHED PROBLEM · STEP 2 · ORIGINAL SCOPE',className='eyebrow'),
                         dcc.Markdown(markdown_for_app(text),className='prose')],className='finding-card')
    except (ArtifactError,IndexError):
        return html.Div()
