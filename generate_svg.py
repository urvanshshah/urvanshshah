import json
import xml.sax.saxutils as saxutils

def generate_svg():
    with open('gitascii.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Global styles
    gs = data.get('globalStyles', {})
    bg_color = gs.get('backgroundColor', '#060606')
    text_color = gs.get('textColor', '#e5e5e5')
    accent_color = gs.get('accentColor', '#c5ff4a')
    border_color = gs.get('borderColor', '#252525')
    font_family = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"

    # Find widgets
    widgets = {w['widgetId']: w for w in data.get('widgets', [])}
    ascii_w = widgets.get('ascii-art', {})
    ascii_text = ascii_w.get('config', {}).get('asciiText', [])
    ascii_colors = ascii_w.get('config', {}).get('asciiColors', [])

    svg_width = 800
    svg_height = 630

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="100%" height="100%">')
    svg.append(f'''<defs>
    <style>
      .mono {{ font-family: {font_family}; }}
      .bold {{ font-weight: 700; }}
      .dim {{ fill: #8b949e; }}
      .accent {{ fill: {accent_color}; }}
      .text-main {{ fill: {text_color}; }}
      .cyan {{ fill: #58a6ff; }}
      .magenta {{ fill: #bc8cff; }}
      .yellow {{ fill: #d29922; }}
      .green {{ fill: #3fb950; }}
      .orange {{ fill: #f0883e; }}
      .border {{ stroke: {border_color}; stroke-width: 1; }}
      .panel {{ fill: #0d1117; }}
      .card-bg {{ fill: #11141a; }}
      .progress-bg {{ fill: #21262d; }}
      @keyframes blink {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
      .cursor {{ animation: blink 1s infinite; }}
    </style>
  </defs>''')

    # Background card
    svg.append(f'<rect width="{svg_width}" height="{svg_height}" rx="12" fill="{bg_color}" stroke="{border_color}" stroke-width="1.5"/>')

    # 1. Header Widget (0, 0, 800, 90)
    svg.append('<!-- Header Widget -->')
    svg.append('<g transform="translate(0, 0)">')
    svg.append(f'<rect width="800" height="42" rx="12" fill="#161b22"/>')
    svg.append(f'<rect y="30" width="800" height="12" fill="#161b22"/>') # square bottom corners of topbar
    svg.append(f'<line x1="0" y1="42" x2="800" y2="42" stroke="{border_color}" stroke-width="1"/>')
    # Window controls
    svg.append('<circle cx="24" cy="21" r="6" fill="#ff5f56"/>')
    svg.append('<circle cx="44" cy="21" r="6" fill="#ffbd2e"/>')
    svg.append('<circle cx="64" cy="21" r="6" fill="#27c93f"/>')
    # Terminal title
    svg.append(f'<text x="400" y="26" text-anchor="middle" class="mono dim" font-size="12">urvansh@asu: ~ (zsh) — 800×630</text>')
    
    # Prompt line
    svg.append(f'<text x="24" y="72" class="mono text-main bold" font-size="14">')
    svg.append(f'<tspan fill="{accent_color}">➜ </tspan>')
    svg.append(f'<tspan class="cyan bold">~ </tspan>')
    svg.append(f'<tspan class="dim">git:(</tspan><tspan fill="#ff7b72">main</tspan><tspan class="dim">) </tspan>')
    svg.append(f'<tspan fill="#e5e5e5">fastfetch --profile urvanshshah</tspan>')
    svg.append(f'<tspan fill="{accent_color}" class="cursor"> █</tspan>')
    svg.append(f'</text>')
    svg.append('</g>')

    # 2. ASCII Art Widget (x: 20, y: 95, w: 260, h: 280)
    svg.append('<!-- ASCII Art Widget -->')
    svg.append('<g transform="translate(20, 95)">')
    svg.append(f'<rect width="265" height="280" rx="8" fill="#0b0e14" stroke="{border_color}" stroke-width="1"/>')
    
    char_w = 3.65
    char_h = 7.8
    num_text_rows = len(ascii_text)
    num_color_rows = len(ascii_colors)

    for r_idx, line in enumerate(ascii_text):
        y_pos = 18 + r_idx * char_h
        color_r = int(r_idx * num_color_rows / num_text_rows)
        color_r = min(color_r, num_color_rows - 1)
        colors_for_row = ascii_colors[color_r]
        num_colors_in_row = len(colors_for_row)
        line_len = len(line)

        # Batch characters of the same color into tspans for rendering performance
        current_color = None
        current_chars = []
        start_c = 0
        
        svg.append(f'<text x="8" y="{y_pos:.1f}" class="mono bold" font-size="7.2" xml:space="preserve">')
        for c_idx, ch in enumerate(line):
            color_c = int(c_idx * num_colors_in_row / line_len)
            color_c = min(color_c, num_colors_in_row - 1)
            char_color = colors_for_row[color_c]
            
            if char_color != current_color:
                if current_chars:
                    escaped_chunk = saxutils.escape(''.join(current_chars))
                    svg.append(f'<tspan fill="{current_color}">{escaped_chunk}</tspan>')
                    current_chars = []
                current_color = char_color
            current_chars.append(ch)
        if current_chars:
            escaped_chunk = saxutils.escape(''.join(current_chars))
            svg.append(f'<tspan fill="{current_color}">{escaped_chunk}</tspan>')
        svg.append('</text>')
    svg.append('</g>')

    # 3. Terminal Info Widget (x: 300, y: 95, w: 480, h: 280)
    svg.append('<!-- Terminal Info Widget -->')
    svg.append('<g transform="translate(300, 95)">')
    svg.append(f'<rect width="480" height="280" rx="8" fill="#0b0e14" stroke="{border_color}" stroke-width="1"/>')
    
    # Title
    svg.append(f'<text x="20" y="32" class="mono bold" font-size="16">')
    svg.append(f'<tspan fill="{accent_color}">urvansh</tspan><tspan class="dim">@</tspan><tspan class="cyan">asu-terminal</tspan>')
    svg.append(f'</text>')
    svg.append(f'<line x1="20" y1="42" x2="460" y2="42" stroke="{border_color}" stroke-width="1"/>')

    info_items = [
        ("Role", "Senior Data Science Analyst & SDE", "#58a6ff"),
        ("Education", "M.S. Data Science @ ASU (GPA: 3.9/4.0) '26", "#3fb950"),
        ("Research", "Graduate Research Assistant @ ASU", "#bc8cff"),
        ("Experience", "Microsoft · Sila Nano · Merkle · Mahaveer", "#f0883e"),
        ("Achievements", "3× National Hackathon Winner | Top Voice", "#d29922"),
        ("Core Stack", "Python, SQL, PyTorch, Spark, AWS, Docker", "#58a6ff"),
        ("Location", "Tempe, Arizona, USA 🌵", "#e5e5e5"),
        ("Availability", "Open to Full-Time Roles (May 2026)", "#7ee787")
    ]

    for i, (label, val, val_color) in enumerate(info_items):
        y = 68 + i * 24
        svg.append(f'<text x="20" y="{y}" class="mono" font-size="12">')
        label_padded = f"{label:<13}"
        svg.append(f'<tspan fill="#8b949e" font-weight="600">{label_padded}</tspan>')
        svg.append(f'<tspan fill="{val_color}">{saxutils.escape(val)}</tspan>')
        svg.append('</text>')

    # Color palette pills at bottom of info
    pills = ["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff", "#bc8cff", "#c5ff4a", "#f0883e", "#e5e5e5"]
    svg.append('<g transform="translate(20, 260)">')
    for p_idx, p_col in enumerate(pills):
        svg.append(f'<rect x="{p_idx * 28}" y="0" width="22" height="8" rx="2" fill="{p_col}"/>')
    svg.append('</g>')
    svg.append('</g>')

    # 4. Languages Widget (x: 20, y: 390, w: 480, h: 170)
    svg.append('<!-- Languages Stats Widget -->')
    svg.append('<g transform="translate(20, 390)">')
    svg.append(f'<rect width="480" height="170" rx="8" fill="#0b0e14" stroke="{border_color}" stroke-width="1"/>')
    svg.append(f'<text x="20" y="28" class="mono bold" font-size="13" fill="{accent_color}">⚡ Top Languages &amp; Competencies</text>')
    svg.append(f'<line x1="20" y1="38" x2="460" y2="38" stroke="{border_color}" stroke-width="1"/>')

    langs = [
        ("Python / PyTorch / Pandas", 45, "#3572A5"),
        ("SQL & Database Engineering", 25, "#e38c00"),
        ("TypeScript / JavaScript / React", 15, "#f1e05a"),
        ("R / C++ / Cloud Infra", 15, "#199f4b")
    ]

    # Multi-color progress bar
    total_bar_w = 440
    curr_x = 20
    svg.append(f'<rect x="20" y="52" width="{total_bar_w}" height="10" rx="5" fill="#21262d"/>')
    svg.append('<g>')
    for l_name, pct, l_col in langs:
        segment_w = total_bar_w * (pct / 100)
        svg.append(f'<rect x="{curr_x}" y="52" width="{segment_w}" height="10" fill="{l_col}"/>')
        curr_x += segment_w
    svg.append('</g>')

    # Language legend list (2x2 grid)
    for idx, (l_name, pct, l_col) in enumerate(langs):
        col_x = 20 if idx % 2 == 0 else 250
        row_y = 90 + (idx // 2) * 32
        svg.append(f'<circle cx="{col_x + 5}" cy="{row_y - 4}" r="5" fill="{l_col}"/>')
        svg.append(f'<text x="{col_x + 18}" y="{row_y}" class="mono" font-size="11">')
        svg.append(f'<tspan fill="#e5e5e5" font-weight="600">{l_name}</tspan> ')
        svg.append(f'<tspan fill="#8b949e">({pct}%)</tspan>')
        svg.append('</text>')

    svg.append('</g>')

    # 5. Tech Stack Widget (x: 515, y: 390, w: 265, h: 170)
    svg.append('<!-- Tech Stack Widget -->')
    svg.append('<g transform="translate(515, 390)">')
    svg.append(f'<rect width="265" height="170" rx="8" fill="#0b0e14" stroke="{border_color}" stroke-width="1"/>')
    svg.append(f'<text x="16" y="28" class="mono bold" font-size="13" fill="{accent_color}">🛠️ Tech Ecosystem</text>')
    svg.append(f'<line x1="16" y1="38" x2="249" y2="38" stroke="{border_color}" stroke-width="1"/>')

    tech_badges = [
        ("Python", "#3776AB"),
        ("SQL", "#4479A1"),
        ("TypeScript", "#3178C6"),
        ("React", "#61DAFB"),
        ("Docker", "#2496ED"),
        ("AWS", "#FF9900"),
        ("PyTorch", "#EE4C2C"),
        ("Spark", "#E25A1C")
    ]

    for idx, (t_name, t_col) in enumerate(tech_badges):
        bx = 16 + (idx % 2) * 120
        by = 52 + (idx // 2) * 26
        svg.append(f'<rect x="{bx}" y="{by}" width="112" height="20" rx="4" fill="#161b22" stroke="{border_color}" stroke-width="1"/>')
        svg.append(f'<circle cx="{bx + 10}" cy="{by + 10}" r="3.5" fill="{t_col}"/>')
        svg.append(f'<text x="{bx + 20}" y="{by + 14}" class="mono bold" font-size="10" fill="#e5e5e5">{t_name}</text>')

    svg.append('</g>')

    # 6. Footer Widget (x: 20, y: 575, w: 760, h: 42)
    svg.append('<!-- Footer Widget -->')
    svg.append('<g transform="translate(20, 575)">')
    svg.append(f'<rect width="760" height="42" rx="8" fill="#161b22" stroke="{border_color}" stroke-width="1"/>')
    svg.append(f'<text x="20" y="26" class="mono" font-size="11">')
    svg.append(f'<tspan fill="{accent_color}">⚡ status:</tspan> <tspan fill="#3fb950">building next-gen data &amp; AI systems</tspan>')
    svg.append(f'</text>')
    svg.append(f'<text x="740" y="26" text-anchor="end" class="mono dim" font-size="11">')
    svg.append(f'<tspan fill="#8b949e">portfolio: </tspan><tspan fill="#58a6ff">urvanshshah.netlify.app</tspan>')
    svg.append(f'</text>')
    svg.append('</g>')

    svg.append('</svg>')

    with open('gitascii.svg', 'w', encoding='utf-8') as f:
        f.write('\n'.join(svg))
    print('Generated gitascii.svg successfully!')

if __name__ == '__main__':
    generate_svg()
