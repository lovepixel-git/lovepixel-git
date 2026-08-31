#!/usr/bin/env python3
"""Builds the animated SVG assets for the profile README.

Tweak the palette below, run `python3 assets/build.py`, commit the output.
Everything is self-hosted and self-contained: no external fonts, no badge
services, no CDN. SMIL animation so it plays inside GitHub's <img> proxy.
"""
import os

# ---- Lovepixel palette -------------------------------------------------
PINK, PURPLE, BLUE = "#FF6FB5", "#B57BFF", "#6FA8FF"
INK   = "#8A7FA8"   # muted text, readable on light AND dark GitHub
GOLD  = "#FFCF6F"
FONT  = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
OUT   = os.path.dirname(os.path.abspath(__file__))


def flow(gid, dur="7s"):
    """A gradient that loops forever without a seam."""
    return (
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0" spreadMethod="repeat">'
        f'<stop offset="0" stop-color="{PINK}"/><stop offset="0.25" stop-color="{PURPLE}"/>'
        f'<stop offset="0.5" stop-color="{BLUE}"/><stop offset="0.75" stop-color="{PURPLE}"/>'
        f'<stop offset="1" stop-color="{PINK}"/>'
        f'<animateTransform attributeName="gradientTransform" type="translate"'
        f' from="0 0" to="1 0" dur="{dur}" repeatCount="indefinite"/></linearGradient>'
    )


def svg(w, h, body, defs="", label=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" '
        f'height="{h}" role="img" aria-label="{label}" fill="none">'
        f'<defs>{defs}</defs>{body}</svg>\n'
    )


def write(name, content):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(content)
    print(f"  {name}  {len(content):>6} bytes")


# ---- 1. header ---------------------------------------------------------
sparks = ""
for i, (cx, cy, r, dur, col) in enumerate([
    (72, 58, 3.5, "3.1s", PINK), (146, 168, 2.5, "4.3s", PURPLE),
    (44, 132, 2.0, "2.6s", BLUE), (828, 62, 3.0, "3.7s", PURPLE),
    (762, 172, 2.5, "2.9s", PINK), (866, 138, 2.0, "4.9s", BLUE),
]):
    sparks += (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}">'
               f'<animate attributeName="opacity" values="0.15;0.95;0.15" '
               f'dur="{dur}" repeatCount="indefinite" begin="{i*0.4}s"/></circle>')

write("welcome-header.svg", svg(900, 216, f'''
<g font-family="{FONT}">
  <text x="450" y="50" text-anchor="middle" font-size="15" letter-spacing="6.5"
        fill="{INK}" opacity="0.9">HI, I&apos;M CHRISTIAN</text>
  <text x="450" y="124" text-anchor="middle" font-size="58" font-weight="800"
        fill="url(#hg)" textLength="800" lengthAdjust="spacingAndGlyphs"
        >welcome to my github portfolio</text>
  <text x="450" y="162" text-anchor="middle" font-size="16.5" fill="{INK}"
        >AI Solutions Architect &#183; AI made with Love.</text>
</g>
<rect x="330" y="188" width="240" height="6" rx="3" fill="url(#hg)">
  <animate attributeName="width" values="240;360;240" dur="6s" repeatCount="indefinite"/>
  <animate attributeName="x" values="330;270;330" dur="6s" repeatCount="indefinite"/>
</rect>{sparks}''', flow("hg"), "welcome to my github portfolio"))


# ---- 2. "i love code" mark --------------------------------------------
write("code.svg", svg(64, 32, f'''
<rect x="1.6" y="1.6" width="60.8" height="28.8" rx="9" fill="none"
      stroke="url(#cg)" stroke-width="2.4"/>
<circle cx="11" cy="10" r="1.8" fill="{PINK}"/>
<circle cx="17.5" cy="10" r="1.8" fill="{PURPLE}"/>
<circle cx="24" cy="10" r="1.8" fill="{BLUE}"/>
<rect x="10" y="18.5" height="3.4" rx="1.7" fill="url(#cg)" width="4">
  <animate attributeName="width" values="2;30;2" dur="2.6s" repeatCount="indefinite"/>
</rect>
<rect y="17.4" width="2.6" height="5.6" rx="1.3" fill="{PURPLE}" x="14">
  <animate attributeName="x" values="13;41;13" dur="2.6s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="1;1;0;1" dur="0.9s" repeatCount="indefinite"/>
</rect>''', flow("cg", "5s"), "i love code"))


# ---- 3. pixel unicorn (Lovepixel, literally) ---------------------------
# Shape is described as spans, not ASCII, and the outline is computed from the
# silhouette so it stays clean whenever the spans are edited.
HEAD = {4: (9, 12), 5: (8, 13), 6: (7, 14), 7: (7, 15), 8: (6, 17), 9: (6, 18),
        10: (6, 18), 11: (6, 17), 12: (6, 14), 13: (6, 13), 14: (7, 12),
        15: (8, 12), 16: (8, 11), 17: (9, 11)}
EAR   = {2: (8, 8), 3: (8, 9)}
HORN  = {0: (13, 13), 1: (12, 13), 2: (12, 12), 3: (11, 12)}
MANE  = {5: [8], 6: [7, 8], 7: [6, 7, 8], 8: [5, 6, 7], 9: [4, 5, 6, 7],
         10: [4, 5, 6, 7], 11: [3, 4, 5, 6], 12: [3, 4, 5, 6], 13: [4, 5, 6],
         14: [4, 5, 6, 7], 15: [5, 6], 16: [6]}
MUZZLE = {9: [16, 17, 18], 10: [16, 17, 18], 11: [15, 16, 17]}
OUTLINE, BODY, EYE, NOSE = "#6D4FD6", "#FDF2FF", "#3B2B4A", "#FF8FC0"
BANDS = [PINK, PURPLE, BLUE]

cells = {}
for r, (a, b) in list(HEAD.items()) + list(EAR.items()):
    for c in range(a, b + 1):
        cells[(r, c)] = BODY
for r, cs in MUZZLE.items():
    for c in cs:
        cells[(r, c)] = "#FFD9EC"
for r, (a, b) in HORN.items():
    for c in range(a, b + 1):
        cells[(r, c)] = GOLD if r > 1 else "#FFE9B8"
for r, cs in MANE.items():
    for c in cs:
        cells[(r, c)] = BANDS[((r + c) // 2) % 3]
cells[(8, 13)] = EYE
cells[(10, 17)] = NOSE

for (r, c) in list(cells):                      # 4-way silhouette outline
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        if (r + dr, c + dc) not in cells:
            cells.setdefault((r + dr, c + dc), OUTLINE)
for k, v in list(cells.items()):
    if v is None:
        cells[k] = OUTLINE

r0 = min(r for r, _ in cells); c0 = min(c for _, c in cells)
W = max(c for _, c in cells) - c0 + 1
H = max(r for r, _ in cells) - r0 + 1
px = "".join(f'<rect x="{c-c0}" y="{r-r0}" width="1" height="1" fill="{v}"/>'
             for (r, c), v in sorted(cells.items()))
star = (f'<g fill="#FFF3C4" transform="translate({13-c0+0.5} {0-r0})">'
        '<path d="M0,-1.15 L0.3,-0.3 L1.15,0 L0.3,0.3 L0,1.15 L-0.3,0.3 '
        'L-1.15,0 L-0.3,-0.3 Z">'
        '<animateTransform attributeName="transform" type="scale" '
        'values="0.15;1.2;0.15" dur="2.4s" repeatCount="indefinite"/>'
        '<animate attributeName="opacity" values="0;1;0" dur="2.4s" '
        'repeatCount="indefinite"/></path></g>')
write("unicorn.svg", svg(W, H, (
    f'<g shape-rendering="crispEdges">{px}'
    '<animateTransform attributeName="transform" type="translate" '
    'values="0 0.5; 0 -0.4; 0 0.5" dur="3.4s" repeatCount="indefinite"/></g>'
    f'{star}'), "", "and unicorns"))


# ---- 4. divider --------------------------------------------------------
write("divider.svg", svg(900, 12, f'''
<rect x="0" y="4.5" width="900" height="3" rx="1.5" fill="url(#dg)" opacity="0.45"/>
<circle cy="6" r="4.5" fill="url(#dg)" cx="40">
  <animate attributeName="cx" values="40;860;40" dur="11s" repeatCount="indefinite"/>
</circle>''', flow("dg", "9s"), ""))


# ---- 5. live status ----------------------------------------------------
write("status.svg", svg(660, 32, f'''
<circle cx="14" cy="16" r="5" fill="{PINK}">
  <animate attributeName="opacity" values="1;0.35;1" dur="1.8s" repeatCount="indefinite"/>
</circle>
<circle cx="14" cy="16" r="5" fill="none" stroke="{PINK}" stroke-width="1.5">
  <animate attributeName="r" values="5;13" dur="1.8s" repeatCount="indefinite"/>
  <animate attributeName="opacity" values="0.7;0" dur="1.8s" repeatCount="indefinite"/>
</circle>
<text x="32" y="21" font-family="{FONT}" font-size="15" fill="{INK}"
      >56 agents running unattended &#183; 14 MCP servers &#183; 1 TB of video indexed</text>''',
    "", "currently running"))


# ---- 6. badge row (the Lovepixel answer to 88x31 GeoCities buttons) ----
LABELS = ["MADE WITH LOVE", "100% AGENTIC", "NO DEMOS",
          "POWERED BY MATCHA", "BEST VIEWED IN ANY BROWSER"]
x, gap, parts = 0, 10, ""
for i, label in enumerate(LABELS):
    w = round(len(label) * 6.55 + 26)
    parts += (
        f'<g><rect x="{x}" y="1.2" width="{w}" height="29.6" rx="14.8" fill="none" '
        f'stroke="url(#bg)" stroke-width="1.8" opacity="0.85"/>'
        f'<text x="{x + w/2:.1f}" y="20.2" text-anchor="middle" font-family="{FONT}" '
        f'font-size="9.5" font-weight="700" letter-spacing="1.15" fill="{INK}">{label}</text>'
        f'<animate attributeName="opacity" values="0.55;1;0.55" dur="4s" '
        f'begin="{i*0.55}s" repeatCount="indefinite"/></g>')
    x += w + gap
write("badges.svg", svg(x - gap, 32, parts, flow("bg", "8s"), "badges"))


# ---- 7. footer ---------------------------------------------------------
write("footer.svg", svg(900, 74, f'''
<g transform="translate(450 30)">
  <path d="M0,7 C-11,-4 -8,-15 0,-9 C8,-15 11,-4 0,7 Z" fill="url(#fg)">
    <animateTransform attributeName="transform" type="scale"
      values="1;1.18;1;1.08;1" dur="1.9s" repeatCount="indefinite"/>
  </path>
</g>
<text x="450" y="62" text-anchor="middle" font-family="{FONT}" font-size="19"
      font-weight="700" fill="url(#fg)">AI made with Love.</text>''',
    flow("fg", "6s"), "AI made with Love"))

print("done.")
