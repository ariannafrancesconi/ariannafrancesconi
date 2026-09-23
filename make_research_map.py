"""Animated research map: four overlapping challenges of Resilient AI,
projects sitting in their intersections, a travelling spark linking them.

Run:  python3 make_research_map.py   (writes assets/research-map-{dark,light}.svg)
Edit PROJECTS to rename, move or add a node.
"""
from html import escape

W, H = 1200, 660
CX, CY, D, R = 600, 325, 112, 150      # Venn centre, offset of each circle, radius

THEMES = {
    "dark": dict(bg="#0D1117", text="#E6EDF3", muted="#8B949E", node="#0D1117",
                 core="#FFFFFF", fillop=0.10),
    "light": dict(bg="#FFFFFF", text="#1F2328", muted="#57606A", node="#FFFFFF",
                  core="#0A2540", fillop=0.09),
}

# challenge circles: (name, line2, colour, centre, label position)
CIRCLES = [
    ("IMBALANCE", "the rare class matters most", "#14B8A6", (CX, CY - D), (CX, CY - D - R - 26)),
    ("BIAS & FAIRNESS", "disease, or the patient?", "#F43F5E", (CX + D, CY), (CX + D + R + 88, CY - 6)),
    ("DOMAIN SHIFT", "new cohort, device, language", "#F59E0B", (CX, CY + D), (CX, CY + D + R + 26)),
    ("MISSING MODALITIES", "no patient has everything", "#8B5CF6", (CX - D, CY), (CX - D - R - 98, CY - 6)),
]

# projects: (label, sub, x, y, colour) — placed in the region they belong to
PROJECTS = [
    ("IMBALMED", "multimodal ensemble", 506, 232, "#14B8A6"),
    ("Keystrokes", "cross-dataset", 600, 140, "#14B8A6"),
    ("Confounder audit", "voice + tapping", 694, 232, "#F43F5E"),
    ("FairPDA", "fair adaptation", 694, 418, "#F59E0B"),
    ("HYCA", "unpaired fusion", 506, 418, "#8B5CF6"),
    ("Clinical LLMs", "notes + labs", 405, 325, "#8B5CF6"),
]
PATH_ORDER = [0, 1, 2, 3, 4, 5]
HALO = "#000"   # set per theme in build()


def t(x, y, s, size, fill, weight=400, anchor="middle", ls=0, mono=False):
    """Text with a background-coloured halo drawn underneath, so labels stay legible over lines."""
    fam = "mono" if mono else "sans"
    extra = f' letter-spacing="{ls}"' if ls else ""
    base = (f'class="{fam}" x="{x}" y="{y}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}"{extra}')
    return (f'<text {base} fill="{HALO}" stroke="{HALO}" stroke-width="5" stroke-linejoin="round">{escape(s)}</text>'
            f'<text {base} fill="{fill}">{escape(s)}</text>')


def build(name):
    global HALO
    th = THEMES[name]
    HALO = th["bg"]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="rt rd">',
         '<title id="rt">Where my work sits in Resilient AI</title>',
         '<desc id="rd">Four overlapping challenges of resilient clinical AI: imbalance, bias and fairness, domain shift, missing modalities. '
         'Projects sit in their intersections, linked by a travelling spark to the core, where the ADELAI clinical study meets all four at once.</desc>',
         '<defs><style>.sans{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}'
         '.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}</style>',
         f'<radialGradient id="coreglow"><stop offset="0" stop-color="{th["core"]}" stop-opacity="0.35"/>'
         f'<stop offset="1" stop-color="{th["core"]}" stop-opacity="0"/></radialGradient>',
         '<linearGradient id="spark" x1="0" x2="1"><stop offset="0" stop-color="#14B8A6"/><stop offset="0.33" stop-color="#F43F5E"/>'
         '<stop offset="0.66" stop-color="#F59E0B"/><stop offset="1" stop-color="#8B5CF6"/></linearGradient>',
         '</defs>',
         f'<rect width="{W}" height="{H}" rx="18" fill="{th["bg"]}"/>']

    for i, (nm, sub, col, (x, y), _) in enumerate(CIRCLES):
        b = f"{i * 1.3:.1f}s"
        o.append(f'<circle cx="{x}" cy="{y}" r="{R}" fill="{col}" fill-opacity="{th["fillop"]}">'
                 f'<animate attributeName="r" values="{R};{R + 7};{R}" dur="7s" begin="{b}" repeatCount="indefinite"/></circle>')
        o.append(f'<circle cx="{x}" cy="{y}" r="{R}" fill="none" stroke="{col}" stroke-opacity="0.75" stroke-width="1.6" stroke-dasharray="2 7">'
                 f'<animate attributeName="r" values="{R};{R + 7};{R}" dur="7s" begin="{b}" repeatCount="indefinite"/>'
                 f'<animate attributeName="stroke-dashoffset" values="0;{-90 if i % 2 else 90}" dur="6s" repeatCount="indefinite"/></circle>')

    for nm, sub, col, _, (lx, ly) in CIRCLES:
        o.append(t(lx, ly, nm, 13, col, 800, ls=1.6))
        o.append(t(lx, ly + 17, sub, 11.5, th["muted"]))

    for i, (_, _, x, y, col) in enumerate(PROJECTS):
        o.append(f'<line x1="{x}" y1="{y}" x2="{CX}" y2="{CY}" stroke="{col}" stroke-opacity="0.3" stroke-width="1.2" stroke-dasharray="3 6">'
                 f'<animate attributeName="stroke-dashoffset" values="18;0" dur="1.6s" begin="{i * 0.2:.1f}s" repeatCount="indefinite"/></line>')

    pts = [(PROJECTS[i][2], PROJECTS[i][3]) for i in PATH_ORDER] + [(CX, CY)]
    d = "M" + " L".join(f"{x} {y}" for x, y in pts)
    o.append(f'<path id="thread" d="{d}" fill="none" stroke="url(#spark)" stroke-opacity="0.55" stroke-width="2" stroke-linejoin="round"/>')
    for r_, op in ((12, 0.25), (6, 1)):
        o.append(f'<circle r="{r_}" fill="#FFFFFF" fill-opacity="{op}" stroke="#0A2540" stroke-opacity="{0.4 if name == "light" and r_ == 6 else 0}">'
                 '<animateMotion dur="9s" repeatCount="indefinite"><mpath href="#thread"/></animateMotion>'
                 '<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.9;1" dur="9s" repeatCount="indefinite"/></circle>')

    for i, (lab, sub, x, y, col) in enumerate(PROJECTS):
        b = f"{i * 0.5:.1f}s"
        o.append(f'<circle cx="{x}" cy="{y}" r="9" fill="none" stroke="{col}" stroke-width="2">'
                 f'<animate attributeName="r" values="9;19" dur="2.8s" begin="{b}" repeatCount="indefinite"/>'
                 f'<animate attributeName="stroke-opacity" values="0.8;0" dur="2.8s" begin="{b}" repeatCount="indefinite"/></circle>')
        o.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{th["node"]}" stroke="{col}" stroke-width="3"/>')
        o.append(t(x, y - 17, lab, 13.5, th["text"], 700))
        o.append(t(x, y + 26, sub, 11, th["muted"], mono=True))

    o.append(f'<circle cx="{CX}" cy="{CY}" r="62" fill="url(#coreglow)"/>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="36" fill="none" stroke="url(#spark)" stroke-width="2.5">'
             f'<animate attributeName="r" values="34;46;34" dur="4s" repeatCount="indefinite"/>'
             f'<animate attributeName="stroke-opacity" values="1;0.3;1" dur="4s" repeatCount="indefinite"/></circle>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="30" fill="{th["node"]}" stroke="url(#spark)" stroke-width="2.5"/>')
    o.append(t(CX, CY - 1, "ADELAI", 13, th["text"], 800, ls=0.6))
    o.append(t(CX, CY + 13, "the clinic", 9.5, th["muted"], mono=True))

    o.append(t(46, 70, "RESILIENT AI", 13, th["muted"], 700, "start", ls=2.4))
    for k, line in enumerate(["Models that degrade", "gracefully when real", "clinical data break", "their assumptions."]):
        o.append(t(46, 98 + 25 * k, line, 20, th["text"], 700, "start"))
    o.append(t(W - 46, H - 52, "each dot is a project · the spark follows my PhD", 11.5, th["muted"], 400, "end", mono=True))
    o.append(t(W - 46, H - 34, "the centre: all four at once, in a real clinic", 11.5, th["muted"], 400, "end", mono=True))
    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    for n in THEMES:
        with open(f"assets/research-map-{n}.svg", "w") as f:
            f.write(build(n))
