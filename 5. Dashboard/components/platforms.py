"""Platform identity is reserved for platform dimensions, never category KPIs."""
from dash import html

PLATFORMS = {
    'Facebook': ('facebook', '#1877F2'),
    'Instagram': ('instagram', '#B33B91'),
    'LinkedIn': ('linkedin', '#0A66C2'),
    'YouTube': ('youtube', '#E52428'),
    'TikTok': ('tiktok', '#00A6AD'),
    'X.com': ('x', '#242424'),
}
PLATFORM_COLORS = {name: value[1] for name, value in PLATFORMS.items()}


def platform_label(name):
    slug, _ = PLATFORMS.get(name, ('x', '#242424'))
    return html.Span([html.Img(src=f'/assets/platforms/{slug}.svg', alt='', className='platform-logo'),
                      html.Span(name)], className='platform-label')


def platform_legend(names):
    return html.Div([platform_label(name) for name in names if name in PLATFORMS], className='platform-legend')
