#!/usr/bin/env python3
"""
FRONTEND Generator — CANON compliant

inherits: /CANONIC/APPS/STORE/FRONTEND/CANON.md

Generates {org}.github.io from config.
"""

import json
import os
from pathlib import Path

# Design tokens from CANON
LOGO_URL = "https://raw.githubusercontent.com/canonic-foundation/canonic/main/LANGUAGE/TIERS/assets/logo-business.svg"
STYLE_URL = "https://canonic-foundation.github.io/assets/style.css"
NAV_URL = "https://canonic-foundation.github.io/assets/nav.js"

def generate_page(config: dict) -> str:
    """Generate index.html from config."""

    title = config.get('title', 'CANONIC')
    heading = config.get('heading', 'CANONIC')
    tagline = config.get('tagline', 'Constitutional AI Governance')
    badge = config.get('badge', 'ENTERPRISE')
    sections = config.get('sections', [])
    footer_links = config.get('footer_links', [])

    # Build sections HTML
    sections_html = ""
    for section in sections:
        section_title = section.get('title', '')
        section_subtitle = section.get('subtitle', '')
        section_type = section.get('type', 'grid')  # grid, timeline, flow
        items = section.get('items', [])

        if section_type == 'timeline':
            items_html = generate_timeline(items)
        elif section_type == 'flow':
            items_html = generate_flow(items)
        else:
            items_html = generate_grid(items)

        subtitle_html = f'<p class="section-subtitle">{section_subtitle}</p>' if section_subtitle else ''

        sections_html += f'''
    <section class="section">
        <h2 class="section-title">{section_title}</h2>
        {subtitle_html}
        {items_html}
    </section>
'''

    # Build footer HTML
    footer_html = ' | '.join([f'<a href="{link["url"]}">{link["text"]}</a>' for link in footer_links])

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | CANONIC</title>
    <link rel="stylesheet" href="{STYLE_URL}">
</head>
<body>
    <section class="hero">
        <img src="{LOGO_URL}" alt="CANONIC" style="height: 240px; margin-bottom: 1rem; filter: invert(1);">
        <h1>{heading}</h1>
        <p class="tagline">{tagline}</p>
        <span class="badge">{badge}</span>
    </section>
{sections_html}
    <footer>
        <p>{footer_html}</p>
    </footer>

    <script src="{NAV_URL}"></script>
</body>
</html>
'''

def generate_grid(items: list) -> str:
    """Generate grid of cards."""
    cards = []
    for item in items:
        title = item.get('title', '')
        desc = item.get('description', '')
        url = item.get('url', '')
        active = item.get('active', False)
        dim = item.get('dim', False)

        style = ''
        if active:
            style = ' style="border-color: var(--accent);"'
        elif dim:
            style = ' style="opacity: 0.5;"'

        if url:
            cards.append(f'''            <a href="{url}" class="card"{style}>
                <h3>{title}</h3>
                <p>{desc}</p>
            </a>''')
        else:
            cards.append(f'''            <div class="card"{style}>
                <h3>{title}</h3>
                <p>{desc}</p>
            </div>''')

    return f'''        <div class="grid">
{chr(10).join(cards)}
        </div>'''

def generate_timeline(items: list) -> str:
    """Generate vertical timeline."""
    timeline_items = []
    for item in items:
        title = item.get('title', '')
        desc = item.get('description', '')
        active = item.get('active', False)

        active_class = ' active' if active else ''
        timeline_items.append(f'''            <div class="timeline-item{active_class}">
                <div class="timeline-marker"></div>
                <div class="timeline-content">
                    <h4>{title}</h4>
                    <p>{desc}</p>
                </div>
            </div>''')

    return f'''        <div class="timeline">
{chr(10).join(timeline_items)}
        </div>'''

def generate_flow(items: list) -> str:
    """Generate linear flow."""
    flow_items = []
    for i, item in enumerate(items):
        title = item.get('title', '')
        active = item.get('active', False)
        dim = item.get('dim', False)

        classes = 'flow-item'
        if active:
            classes += ' active'
        if dim:
            classes += ' dim'

        flow_items.append(f'<span class="{classes}">{title}</span>')
        if i < len(items) - 1:
            flow_items.append('<span class="flow-arrow">→</span>')

    return f'''        <div class="flow">
            {' '.join(flow_items)}
        </div>'''

def build_frontend(config_path: str, output_dir: str):
    """Build frontend from config file."""
    with open(config_path, 'r') as f:
        config = json.load(f)

    # Generate main page
    html = generate_page(config)

    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Write index.html
    output_path = os.path.join(output_dir, 'index.html')
    with open(output_path, 'w') as f:
        f.write(html)

    print(f"Generated: {output_path}")

    # Generate subpages if any
    subpages = config.get('subpages', {})
    for path, subconfig in subpages.items():
        subdir = os.path.join(output_dir, path)
        Path(subdir).mkdir(parents=True, exist_ok=True)
        subhtml = generate_page(subconfig)
        subpath = os.path.join(subdir, 'index.html')
        with open(subpath, 'w') as f:
            f.write(subhtml)
        print(f"Generated: {subpath}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3:
        print("Usage: python generator.py <config.json> <output_dir>")
        sys.exit(1)

    build_frontend(sys.argv[1], sys.argv[2])
