"""Small monochrome SVG UI icons, independent of platform branding."""
from urllib.parse import quote
from dash import html

PATHS = {
    'overview': '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
    'performance': '<path d="M4 20V11m8 9V4m8 16v-7M2 21h20"/>',
    'diagnosis': '<circle cx="10" cy="10" r="6"/><path d="m15 15 6 6M7 10h6m-3-3v6"/>',
    'actions': '<rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V2h6v2M9 10l2 2 4-4M9 17h6"/>',
    'eye': '<path d="M2 12s3-7 10-7 10 7 10 7-3 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
    'impressions': '<rect x="3" y="4" width="18" height="13" rx="2"/><path d="M8 21h8m-4-4v4"/>',
    'engagement': '<path d="m12 20-8-8a5 5 0 0 1 8-6 5 5 0 0 1 8 6z"/>',
    'rate': '<path d="m5 19 14-14"/><circle cx="7" cy="7" r="3"/><circle cx="17" cy="17" r="3"/>',
    'arrow': '<path d="M5 12h14m-5-5 5 5-5 5"/>',
    'filter': '<path d="M3 5h18M6 12h12M9 19h6"/>',
}


def icon(name, class_name='ui-icon', color='#64748b'):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{PATHS.get(name, PATHS["overview"])}</svg>'
    return html.Img(src='data:image/svg+xml,' + quote(svg), alt='', className=class_name)
