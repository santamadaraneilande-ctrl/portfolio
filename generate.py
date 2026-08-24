#!usr/bin/env python3
"""
Portfolio generator - viena lapa, divas sadaļas (Devops augšā, Dizains/3D/Māksla apakšā).

Usage:
    python3 generate.py
    
"""
import json
import html
from pathlib import Path

ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "projects.json"
OUTPUT_HTML = ROOT / "index.html"
OUTPUT_CSS= ROOT / "style.css"

def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def esc(text):
    return html.escape(str(text), quote=True)

def render_button(project):
    title = esc(project.get("title", "Untitled"))
    href = esc(project.get("href", "#"))
    proj_type = project.get("type","image")
    if proj_type == "video":
        return f'<a class="proj-btn" href="{href}" target="_blank" rel="noopener">🎬 {title} (YouTube)</a>'
    else:
        return f'<a class="proj-btn" href="{href}" target="_blank" rel="noopener">{title}</a>'
def render_section(projects,section_id):
    if projects:
        buttons = "\n      ".join(render_button(p) for p in projects)
    else:
        buttons = '<p class="empty-note">Vēl nav pievienots neviens darbs.</p>'
    return f'<div class="btn-grid" id="{section_id}">\n    {buttons}\n</div>'

def render_html(data):
    name = esc(data.get("name",""))
    all_projects = data.get("projects", [])
    programming = [p for p in all_projects if p.get("section") == "programming"]
    design = [p for p in all_projects if p.get("section") == "design"]
    art = [p for p in all_projects if p.get("section") == "art-3D"]

    programming_html = render_section(programming, "programming-grid")
    design_html = render_section(design, "design-grid")
    art_html = render_section(art, "art-grid")

    return f"""<!DOCTYPE html>
<html lang="lv">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Portfolio - {name}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,600;0,900;1,500&family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css">
</head>
<body>

    <header class="hero">
        <h1 class="hero-name">Portfolio</h1>
        <p class="hero-tagline">{name}</p>
    </header>

    <section class="section">
        <h2 class="section-title">Programming</h2>
        {programming_html}
    </section>

    <section class="section">
        <h2 class="section-title">Dizains</h2>
        {design_html}
    </section>

    <section class="section">
        <h2 class="section-title">Art & 3D</h2>
        {art_html}
    </section>

</body>
</html>
"""

CSS = """
:root {
    --ink: #000000;
    --btn-bg: #ffffff;
    --hero-text: #f4f2ec;
    --overlay: rgba(10, 10, 16, 0.45);
}

* { box-sizing: border-box; }

body {
    margin:0;
    color: var(--hero-text);
    font-family: 'Space Grotesk', sans-serif;
    background-image:
        linear-gradient(var(--overlay), var(--overlay)),
        url('images/background.jpg');
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    background-repeat: no-repeat;
    min-height: 100vh;
}

.hero {
    padding: 96px 6vw 56px;
    text-alighn: center;
}

.hero-name {
    font-family: 'Fraunces', serif;
    font-weight: 900;
    font-size: clamp(48px, 9vw, 108px);
    margin: 0;
    letter-spacing: -0.01em;
}

.hero-tagline {
    font-family: 'Fraunces', serif;
    font-style: italic;
    font-weight: 500;
    font-size: clamp(18px, 2.4vw, 26px);
    margin: 14px 0 0;
}

.section {
    padding: 40px 6vw 60px;
}

.section-title {
    font-family: 'Fraunces', serif;
    font-weight: 600;
    font-size: clamp(24px, 3vw, 34px);
    margin: 0 0 24px;
}

.btn-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 16px;
}

.proj-btn {
    background: var(--btn-bg);
    color: var(--ink);
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 600;
    font-size: 15px;
    text-align: center;
    text-decoration: none;
    padding: 22px 18px;
    border-radius: 10px;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    box-shadow:0 2px 0 rgba(0,0,0,0.25);
}

.proj-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 14px rgba(0,0,0,0.3);
}

.empty-note {
    color: var(--hero-text);
    opacity: 0.7;
    font-size: 14px;
    font-style: italic;
}

@media (max-width: 560px) {
    .hero { padding: 64px 6vw 40px; }
    .section { padding: 30px 6vw 40px;}
}
"""

def main():
    data = load_data()
    OUTPUT_HTML.write_text(render_html(data), encoding="utf-8")
    OUTPUT_CSS.write_text(CSS, encoding="utf-8")
    print(f"Uzģenerēts: {OUTPUT_HTML}")
    print(f"Uzģenerēts: {OUTPUT_CSS}")

if __name__ == "__main__":
    main()
    
