# FRONTEND — CANON

inherits: /CANONIC/LANGUAGE/TEMPLATES/FRONTEND/
series: *.md

---

## Axiom

**FRONTEND = D∩O∩S grounded. Browser rendering layer.**

---

## Design Tokens

```css
:root {
    --bg: #000;
    --fg: #fff;
    --accent: #00ff88;
    --dim: #888;
    --font: ui-monospace, 'SF Mono', 'Cascadia Code', Menlo, monospace;
}
```

---

## Logo

- **Source**: `https://raw.githubusercontent.com/canonic-foundation/canonic/main/LANGUAGE/TIERS/assets/logo-business.svg`
- **Size**: 240px height
- **Filter**: `filter: invert(1)` (white on black)
- **Position**: Hero section, centered

---

## Page Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{TITLE} | CANONIC</title>
    <link rel="stylesheet" href="https://canonic-foundation.github.io/assets/style.css">
</head>
<body>
    <section class="hero">
        <img src="{LOGO_URL}" alt="{TIER}" style="height: 240px; margin-bottom: 1rem; filter: invert(1);">
        <h1>{HEADING}</h1>
        <p class="tagline">{TAGLINE}</p>
        <span class="badge">{BADGE}</span>
    </section>

    <section class="section">
        <h2 class="section-title">{SECTION}</h2>
        <p class="section-subtitle">{SUBTITLE}</p>
        <div class="grid">
            <!-- cards -->
        </div>
    </section>

    <footer>
        <p>{FOOTER_LINKS}</p>
    </footer>

    <script src="https://canonic-foundation.github.io/assets/nav.js"></script>
</body>
</html>
```

---

## Components

### Timeline (Vertical)

For roadmaps. Vertical flow. Current era highlighted.

```html
<div class="timeline">
    <div class="timeline-item">
        <div class="timeline-marker"></div>
        <div class="timeline-content">
            <h4>v0 ORIGIN</h4>
            <p>Description</p>
        </div>
    </div>
    <div class="timeline-item active">
        <div class="timeline-marker"></div>
        <div class="timeline-content">
            <h4>v2 FOUNDATION</h4>
            <p>Now.</p>
        </div>
    </div>
</div>
```

### Linear Flow

For versioned content (PAPERS). Horizontal badges.

```html
<div class="flow">
    <span class="flow-item">v0</span>
    <span class="flow-arrow">→</span>
    <span class="flow-item">v1</span>
    <span class="flow-arrow">→</span>
    <span class="flow-item active">v2</span>
    <span class="flow-arrow">→</span>
    <span class="flow-item dim">v3</span>
</div>
```

### Cards

Grid layout. 3-column on desktop.

```html
<div class="grid">
    <a href="{URL}" class="card">
        <h3>{TITLE}</h3>
        <p>{DESCRIPTION}</p>
    </a>
</div>
```

---

## CANONVERSE Links

Standard navigation across all frontends:

| Site | URL | Badge |
|------|-----|-------|
| FOUNDATION | canonic-foundation.github.io | FOUNDATION |
| APPS | canonic-apps.github.io | APP STORE |
| DOMAINS | canonic-domains.github.io | DOMAINS |
| USER | {org}.github.io | ENTERPRISE |

---

## Constraints

- No frameworks. Pure CSS/HTML/JS.
- All colors MUST derive from tokens.
- All pages MUST include nav.js.
- Logo MUST be fetched from CDN.
- Level: ENTERPRISE.

---

## Series

- [BACKEND.md](BACKEND.md) — Backend closure spec

---
