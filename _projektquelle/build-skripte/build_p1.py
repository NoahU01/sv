# -*- coding: utf-8 -*-
import json, os

WORKDIR = "/sessions/ecstatic-nice-gauss/mnt/outputs/_work"
SITEDIR = os.path.join(WORKDIR, "site")
os.makedirs(SITEDIR, exist_ok=True)

with open(os.path.join(WORKDIR, "assets_b64.json")) as f:
    B64 = json.load(f)

FONT_HEAD_URI = f"data:font/ttf;base64,{B64['font_head']}"
FONT_BODY_URI = f"data:font/ttf;base64,{B64['font_body']}"
LOGO_COLOR_URI = f"data:image/png;base64,{B64['logo_color']}"
LOGO_WHITE_URI = f"data:image/png;base64,{B64['logo_white']}"
ROCKET_URI = f"data:image/png;base64,{B64['rocket']}"

# ---- Brand colors (from Farben.pptx, Sparkasse_colors theme) ----
C = {
    "rot": "#EE0000",
    "rot_dunkel": "#B30000",
    "dunkelgrau2": "#444444",
    "dunkelgrau1": "#666666",
    "grau6": "#999999",
    "grau5": "#BBBBBB",
    "grau4": "#CCCCCC",
    "grau3": "#D9D9D9",
    "grau2": "#E3E3E3",
    "grau1": "#E9E9E9",
    "hellgrau": "#F0F0F0",
    "violet": "#9B348E",
    "blau": "#2C57D2",
    "hellblau": "#00ACD3",
    "dunkelgruen": "#009864",
    "gelb": "#FFC900",
    "orange": "#FF8F00",
    "weiss": "#FFFFFF",
    "schwarz": "#000000",
}

# Inline SVG icons (recolored via currentColor), sourced from Streamline Ultimate set supplied by client
ICON_ELEARNING = '''<svg viewBox="0 0 250 250" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="10"><path d="M27.5,12.51h195s15,0,15,15v150s0,15-15,15H27.5s-15,0-15-15V27.51s0-15,15-15"/><path d="M162.5,237.51h-75l7.5-45h60l7.5,45Z"/><path d="M65,237.51h120"/><path d="M192.5,80.01v22.5"/><path d="M162.5,93.35v39.16c-10.22,9.41-23.54,14.74-37.43,15-13.93-.28-27.28-5.61-37.57-15v-39.16"/><path d="M57.5,80.01l67.5,30,67.5-30-67.5-30-67.5,30Z"/></g></svg>'''

ICON_GRADUATE = '''<svg viewBox="0 0 250 250" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="10"><path d="M177.5,65c0,28.99-23.51,52.5-52.5,52.5s-52.5-23.51-52.5-52.5V12.5h105v52.5Z"/><path d="M27.5,237.5c0-53.85,43.65-97.5,97.5-97.5s97.5,43.65,97.5,97.5"/><path d="M12.5,12.5h225"/><path d="M72.5,57.5h105"/><path d="M27.5,12.5v75"/><path d="M75.13,153.71l49.87,38.79,49.87-38.79"/></g></svg>'''

ICON_CONVERSATION = '''<svg viewBox="0 0 250 250" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="10"><path d="M222.5,192.5h-105l-60,45v-45h-30c-8.28,0-15-6.72-15-15h0V27.5c0-8.28,6.72-15,15-15h195c8.28,0,15,6.72,15,15v150c0,8.28-6.72,15-15,15Z"/><path d="M148.96,72.5c0,12.43,10.07,22.5,22.5,22.5s22.5-10.07,22.5-22.5-10.07-22.5-22.5-22.5-22.5,10.07-22.5,22.5Z"/><path d="M210.43,125c-12.43-21.52-39.96-28.89-61.48-16.45-6.83,3.95-12.51,9.62-16.45,16.45"/><path d="M61.25,76.25c0,14.5,11.75,26.25,26.25,26.25s26.25-11.75,26.25-26.25h0c0-14.5-11.75-26.25-26.25-26.25s-26.25,11.75-26.25,26.25h0Z"/><path d="M42.5,155c0-24.85,20.15-45,45-45s45,20.15,45,45"/></g></svg>'''

print("Part 1 loaded OK. Logo/Font/Rocket URIs prepared.")

BASE_CSS = f"""
@font-face {{
  font-family: 'Sparkasse Head';
  src: url('{FONT_HEAD_URI}') format('truetype');
  font-weight: 400 800;
  font-style: normal;
  font-display: swap;
}}
@font-face {{
  font-family: 'Sparkasse Lt';
  src: url('{FONT_BODY_URI}') format('truetype');
  font-weight: 300 500;
  font-style: normal;
  font-display: swap;
}}

:root {{
  --rot: {C['rot']};
  --rot-dunkel: {C['rot_dunkel']};
  --dunkelgrau2: {C['dunkelgrau2']};
  --dunkelgrau1: {C['dunkelgrau1']};
  --grau6: {C['grau6']};
  --grau5: {C['grau5']};
  --grau4: {C['grau4']};
  --grau3: {C['grau3']};
  --grau2: {C['grau2']};
  --grau1: {C['grau1']};
  --hellgrau: {C['hellgrau']};
  --violet: {C['violet']};
  --blau: {C['blau']};
  --hellblau: {C['hellblau']};
  --dunkelgruen: {C['dunkelgruen']};
  --gelb: {C['gelb']};
  --orange: {C['orange']};
  --weiss: {C['weiss']};
  --schwarz: {C['schwarz']};
  --font-head: 'Sparkasse Head', 'Arial Narrow', Arial, sans-serif;
  --font-body: 'Sparkasse Lt', Arial, Helvetica, sans-serif;
  --maxw: 1180px;
  --radius: 14px;
  --shadow: 0 10px 30px rgba(0,0,0,0.08);
  --shadow-lg: 0 20px 50px rgba(0,0,0,0.14);
}}

* {{ box-sizing: border-box; }}
html {{ scroll-behavior: smooth; }}
body {{
  margin: 0;
  font-family: var(--font-body);
  color: var(--dunkelgrau2);
  background: var(--weiss);
  -webkit-font-smoothing: antialiased;
  line-height: 1.6;
  font-size: 17px;
}}
h1,h2,h3,h4 {{
  font-family: var(--font-head);
  font-weight: 800;
  color: var(--dunkelgrau2);
  line-height: 1.15;
  margin: 0 0 .5em 0;
}}
h1 {{ font-size: clamp(2rem, 4.2vw, 3.4rem); letter-spacing: -0.01em; }}
h2 {{ font-size: clamp(1.6rem, 3vw, 2.4rem); }}
h3 {{ font-size: 1.25rem; }}
p {{ margin: 0 0 1em 0; }}
a {{ color: var(--rot); text-decoration: none; }}
.eyebrow {{
  display: inline-flex; align-items: center; gap: 8px;
  font-family: var(--font-head); font-weight: 700;
  font-size: .78rem; letter-spacing: .12em; text-transform: uppercase;
  color: var(--rot); margin-bottom: 14px;
}}
.eyebrow::before {{ content:""; width: 22px; height: 3px; background: var(--rot); border-radius: 2px; display:inline-block; }}
.wrap {{ max-width: var(--maxw); margin: 0 auto; padding: 0 28px; }}
.section {{ padding: 88px 0; position: relative; }}
.section-tight {{ padding: 56px 0; }}
.center {{ text-align: center; }}
.muted {{ color: var(--dunkelgrau1); }}
.small {{ font-size: .9rem; }}
img {{ max-width: 100%; display:block; }}

/* Buttons */
.btn {{
  display: inline-flex; align-items:center; justify-content:center; gap:10px;
  font-family: var(--font-head); font-weight: 700; font-size: .98rem;
  padding: 15px 30px; border-radius: 999px; border: 2px solid transparent;
  cursor: pointer; transition: all .18s ease; white-space: nowrap;
}}
.btn-primary {{ background: var(--rot); color: #fff; box-shadow: 0 8px 20px rgba(238,0,0,.28); }}
.btn-primary:hover {{ background: var(--rot-dunkel); transform: translateY(-2px); box-shadow: 0 12px 26px rgba(238,0,0,.35); }}
.btn-ghost {{ background: transparent; border-color: rgba(255,255,255,.7); color: #fff; }}
.btn-ghost:hover {{ background: rgba(255,255,255,.15); transform: translateY(-2px); }}
.btn-outline {{ background: #fff; border-color: var(--grau4); color: var(--dunkelgrau2); }}
.btn-outline:hover {{ border-color: var(--rot); color: var(--rot); transform: translateY(-2px); }}
.btn-sm {{ padding: 10px 20px; font-size: .85rem; }}
.btn-block {{ width: 100%; }}
.btn[disabled] {{ opacity:.45; cursor:not-allowed; transform:none !important; }}

/* Header / Nav */
.site-header {{
  position: sticky; top: 0; z-index: 500;
  background: rgba(255,255,255,.92); backdrop-filter: blur(10px);
  border-bottom: 1px solid var(--grau2);
}}
.site-header .wrap {{ display:flex; align-items:center; justify-content:space-between; height: 84px; }}
.brand {{ display:flex; align-items:center; gap:12px; }}
.brand img {{ height: 40px; width:auto; }}
.nav {{ display:flex; align-items:center; gap: 30px; }}
.nav a {{ color: var(--dunkelgrau2); font-weight:600; font-size:.95rem; padding: 6px 2px; border-bottom: 2px solid transparent; }}
.nav a:hover, .nav a.active {{ color: var(--rot); border-color: var(--rot); }}
.nav-cta {{ display:flex; align-items:center; gap:14px; }}
.burger {{ display:none; background:none; border:none; cursor:pointer; padding:8px; }}
.burger span {{ display:block; width:26px; height:3px; background:var(--dunkelgrau2); margin:5px 0; border-radius:2px; }}

@media (max-width: 900px) {{
  .nav {{ position:fixed; inset: 84px 0 0 0; background:#fff; flex-direction:column; align-items:flex-start;
    padding: 28px; gap:20px; transform: translateX(100%); transition: transform .25s ease; overflow:auto; }}
  .nav.open {{ transform: translateX(0); }}
  .burger {{ display:block; }}
  .nav-cta .btn-outline {{ display:none; }}
}}

/* Footer */
.site-footer {{ background: var(--dunkelgrau2); color: #fff; padding: 56px 0 28px; }}
.site-footer a {{ color: #fff; opacity:.85; }}
.site-footer a:hover {{ opacity:1; text-decoration:underline; }}
.footer-grid {{ display:grid; grid-template-columns: 1.4fr 1fr 1fr 1fr; gap: 40px; margin-bottom:40px; }}
.footer-grid h4 {{ color:#fff; font-size:.95rem; text-transform:uppercase; letter-spacing:.06em; margin-bottom:14px; }}
.footer-grid ul {{ list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:10px; font-size:.92rem; }}
.footer-bottom {{ border-top:1px solid rgba(255,255,255,.15); padding-top:22px; display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; font-size:.85rem; opacity:.75; }}
@media (max-width:800px) {{ .footer-grid {{ grid-template-columns: 1fr 1fr; }} }}

/* Cards */
.card {{ background:#fff; border:1px solid var(--grau2); border-radius: var(--radius); padding: 32px; transition: all .2s ease; }}
.card:hover {{ box-shadow: var(--shadow); transform: translateY(-4px); border-color: var(--grau3); }}
.grid {{ display:grid; gap: 26px; }}
.grid-3 {{ grid-template-columns: repeat(3, 1fr); }}
.grid-2 {{ grid-template-columns: repeat(2, 1fr); }}
.grid-4 {{ grid-template-columns: repeat(4, 1fr); }}
@media (max-width: 900px) {{ .grid-3, .grid-4 {{ grid-template-columns: 1fr 1fr; }} }}
@media (max-width: 620px) {{ .grid-3, .grid-4, .grid-2 {{ grid-template-columns: 1fr; }} }}

/* Icon badge (gradient ring like Selbstbild) */
.icon-badge {{
  width:74px; height:74px; border-radius:50%; display:flex; align-items:center; justify-content:center;
  background: #fff; border: 2.5px solid; border-image: linear-gradient(135deg, var(--rot), var(--violet)) 1;
  margin-bottom: 20px; color: var(--dunkelgrau2);
}}
.icon-badge svg {{ width: 34px; height:34px; }}

/* Pillar/problem numbering */
.num-badge {{
  width:40px;height:40px;border-radius:50%;background:var(--rot);color:#fff;
  display:flex;align-items:center;justify-content:center;font-family:var(--font-head);font-weight:800;
  flex-shrink:0;
}}

BASE_CSS += f"""
/* Hero */
.hero {{
  position: relative; background: linear-gradient(160deg, var(--rot) 0%, var(--rot-dunkel) 100%);
  color:#fff; overflow:hidden; padding-top: 70px;
}}
.hero .wrap {{ position:relative; z-index:2; display:grid; grid-template-columns: 1.15fr .85fr; gap: 40px; align-items:center; padding-bottom: 140px; padding-top: 40px; }}
.hero h1 {{ color:#fff; }}
.hero p.lead {{ font-size:1.15rem; opacity:.95; max-width: 540px; }}
.hero-ctas {{ display:flex; gap:16px; flex-wrap:wrap; margin-top: 30px; }}
.hero-visual {{ display:flex; justify-content:center; align-items:center; }}
.hero-visual img {{ max-width: 320px; filter: drop-shadow(0 30px 40px rgba(0,0,0,.35)); animation: float 5s ease-in-out infinite; }}
@keyframes float {{ 0%,100% {{ transform: translateY(0);}} 50% {{ transform: translateY(-16px);}} }}
.cloud-divider {{ position:absolute; left:0; right:0; bottom:-1px; line-height:0; z-index:1; }}
.cloud-divider svg {{ width:100%; height: auto; display:block; }}
.hero-stats {{ position:relative; z-index:2; display:flex; gap: 46px; flex-wrap:wrap; margin-top: 14px; }}
.hero-stat b {{ font-family: var(--font-head); font-size:1.6rem; display:block; }}
.hero-stat span {{ font-size:.85rem; opacity:.85; }}
@media (max-width: 900px) {{ .hero .wrap {{ grid-template-columns: 1fr; text-align:center; }} .hero-ctas, .hero-stats {{ justify-content:center; }} .hero-visual img {{ max-width:220px; }} }}

/* Problem list */
.problem-row {{ display:flex; gap:20px; align-items:flex-start; padding: 22px 0; border-bottom: 1px solid var(--grau2); }}
.problem-row:last-child {{ border-bottom:none; }}
.problem-icon {{ font-size:1.6rem; flex-shrink:0; }}

/* Timeline (Zusammenarbeit) */
.timeline {{ display:grid; grid-template-columns: repeat(4,1fr); gap: 22px; counter-reset: step; margin-top: 50px; }}
.timeline-step {{ position:relative; background:#fff; border:1px solid var(--grau2); border-radius: var(--radius); padding: 30px 24px; }}
.timeline-step::before {{ counter-increment: step; content: counter(step); position:absolute; top:-18px; left:24px;
  width:36px;height:36px;border-radius:50%; background:var(--rot); color:#fff; display:flex;align-items:center;justify-content:center;
  font-family:var(--font-head); font-weight:800; box-shadow:0 6px 14px rgba(238,0,0,.35); }}
.timeline-step h3 {{ margin-top: 10px; }}
@media (max-width: 900px) {{ .timeline {{ grid-template-columns: 1fr 1fr; }} }}
@media (max-width: 600px) {{ .timeline {{ grid-template-columns: 1fr; }} }}

/* Lead magnet cards */
.lead-card {{ display:flex; flex-direction:column; height:100%; }}
.lead-card .tag {{ align-self:flex-start; background: var(--grau1); color:var(--dunkelgrau1); font-size:.72rem; font-weight:700;
  text-transform:uppercase; letter-spacing:.06em; padding: 5px 12px; border-radius: 999px; margin-bottom:16px; }}
.lead-card .tag.new {{ background: #FCE8E8; color: var(--rot); }}
.lead-card p {{ flex-grow:1; }}

/* Accordion (FAQ) */
.accordion-item {{ border-bottom: 1px solid var(--grau2); }}
.accordion-item:first-child {{ border-top: 1px solid var(--grau2); }}
.accordion-trigger {{
  width:100%; text-align:left; background:none; border:none; cursor:pointer;
  display:flex; justify-content:space-between; align-items:center; gap:20px;
  padding: 22px 4px; font-family: var(--font-head); font-weight:700; font-size:1.05rem; color: var(--dunkelgrau2);
}}
.accordion-trigger:hover {{ color: var(--rot); }}
.accordion-plus {{ flex-shrink:0; width:28px;height:28px;border-radius:50%;border:2px solid var(--rot); color:var(--rot);
  display:flex;align-items:center;justify-content:center; font-size:1.1rem; transition: transform .2s ease; }}
.accordion-item.open .accordion-plus {{ transform: rotate(135deg); background:var(--rot); color:#fff; }}
.accordion-panel {{ max-height:0; overflow:hidden; transition: max-height .3s ease; }}
.accordion-panel-inner {{ padding: 0 4px 24px 4px; color: var(--dunkelgrau1); }}

/* Modal / Pop-up */
.modal-overlay {{
  position:fixed; inset:0; background: rgba(20,20,20,.55); display:flex; align-items:center; justify-content:center;
  z-index:1000; opacity:0; pointer-events:none; transition: opacity .2s ease; padding: 20px;
}}
.modal-overlay.active {{ opacity:1; pointer-events:auto; }}
.modal-box {{
  background:#fff; border-radius: 18px; max-width: 480px; width:100%; padding: 40px; position:relative;
  transform: translateY(16px) scale(.98); transition: transform .25s ease; box-shadow: var(--shadow-lg); text-align:center;
}}
.modal-overlay.active .modal-box {{ transform: translateY(0) scale(1); }}
.modal-close {{ position:absolute; top:16px; right:16px; background:var(--grau1); border:none; width:34px;height:34px;
  border-radius:50%; cursor:pointer; font-size:1.1rem; color:var(--dunkelgrau1); }}
.modal-icon {{ width:64px;height:64px;border-radius:50%; background: #E9F8F1; color: var(--dunkelgruen); display:flex;
  align-items:center;justify-content:center; margin: 0 auto 20px; font-size:1.8rem; }}

/* Forms */
.form-field {{ margin-bottom: 20px; text-align:left; }}
.form-field label {{ display:block; font-weight:700; font-size:.85rem; margin-bottom:7px; color: var(--dunkelgrau2); }}
.form-field input, .form-field select, .form-field textarea {{
  width:100%; padding: 13px 16px; border-radius: 10px; border: 1.5px solid var(--grau3); font-family: var(--font-body);
  font-size: 1rem; background:#fff; color: var(--dunkelgrau2); transition: border-color .15s ease;
}}
.form-field input:focus, .form-field select:focus, .form-field textarea:focus {{ outline:none; border-color: var(--rot); }}
.form-row {{ display:grid; grid-template-columns:1fr 1fr; gap:18px; }}
@media (max-width:600px) {{ .form-row {{ grid-template-columns:1fr; }} }}
.form-check {{ display:flex; align-items:flex-start; gap:10px; font-size:.85rem; color: var(--dunkelgrau1); }}

/* Choice cards (Quick-Check) */
.choice-card {{ border:2px solid var(--grau3); border-radius: var(--radius); padding:26px; cursor:pointer; text-align:left; background:#fff; transition: all .18s ease; }}
.choice-card:hover {{ border-color: var(--grau5); }}
.choice-card.selected {{ border-color: var(--rot); box-shadow: 0 0 0 4px rgba(238,0,0,.08); }}
.choice-card .radio-dot {{ width:22px;height:22px;border-radius:50%;border:2px solid var(--grau4); margin-bottom:14px; position:relative; }}
.choice-card.selected .radio-dot {{ border-color: var(--rot); }}
.choice-card.selected .radio-dot::after {{ content:""; position:absolute; inset:3px; border-radius:50%; background:var(--rot); }}

/* Slot buttons */
.slot-btn {{ border:1.5px solid var(--grau3); background:#fff; border-radius:10px; padding:12px 10px; cursor:pointer; font-weight:700; font-size:.85rem; text-align:center; }}
.slot-btn:hover {{ border-color: var(--grau5); }}
.slot-btn.selected {{ background: var(--rot); border-color:var(--rot); color:#fff; }}
.slot-grid {{ display:grid; grid-template-columns: repeat(3,1fr); gap:10px; }}

/* Pills / badges */
.pill {{ display:inline-block; padding:5px 14px; border-radius:999px; font-size:.75rem; font-weight:700; letter-spacing:.03em; }}
.pill-red {{ background:#FCE8E8; color:var(--rot); }}
.pill-green {{ background:#E1F5EC; color:var(--dunkelgruen); }}
.pill-grau {{ background:var(--grau1); color:var(--dunkelgrau1); }}

/* Section backgrounds */
.bg-grau {{ background: var(--hellgrau); }}
.bg-dunkel {{ background: var(--dunkelgrau2); color:#fff; }}
.bg-dunkel h2, .bg-dunkel h3 {{ color:#fff; }}

/* Sticky mini CTA bar (mobile) */
.mobile-cta-bar {{ display:none; }}
@media (max-width:700px) {{
  .mobile-cta-bar {{ display:flex; position:fixed; bottom:0; left:0; right:0; background:#fff; border-top:1px solid var(--grau2);
    padding:12px 16px; z-index:400; box-shadow: 0 -6px 20px rgba(0,0,0,.08); }}
}}

/* Utility reveal animation */
.reveal {{ opacity:0; transform: translateY(24px); transition: opacity .6s ease, transform .6s ease; }}
.reveal.visible {{ opacity:1; transform:none; }}

/* Simple page hero (subpages) */
.page-hero {{ background: linear-gradient(160deg, var(--dunkelgrau2), #2a2a2a); color:#fff; padding: 130px 0 70px; }}
.page-hero h1 {{ color:#fff; }}
.breadcrumb {{ font-size:.85rem; opacity:.75; margin-bottom:18px; }}
.breadcrumb a {{ color:#fff; }}

/* Login mock (Portal) */
.login-card {{ background:#fff; border-radius:20px; box-shadow: var(--shadow-lg); padding:44px; max-width:420px; margin: -90px auto 0; position:relative; z-index:5; }}
.dash-mock {{ background:#fff; border-radius:16px; border:1px solid var(--grau2); overflow:hidden; box-shadow: var(--shadow); }}
.dash-topbar {{ background: var(--dunkelgrau2); color:#fff; padding:14px 22px; display:flex; align-items:center; justify-content:space-between; font-size:.85rem; }}
.dash-body {{ display:grid; grid-template-columns: 220px 1fr; min-height: 380px; }}
.dash-side {{ background: var(--hellgrau); padding: 22px 16px; border-right:1px solid var(--grau2); }}
.dash-side a {{ display:block; padding:10px 12px; border-radius:8px; color:var(--dunkelgrau2); font-weight:600; font-size:.9rem; margin-bottom:4px; }}
.dash-side a.active {{ background:#fff; color:var(--rot); box-shadow:0 2px 6px rgba(0,0,0,.06); }}
.dash-main {{ padding: 26px; }}
.progress-bar {{ height:8px; background:var(--grau2); border-radius:99px; overflow:hidden; margin-top:8px; }}
.progress-bar > span {{ display:block; height:100%; background: linear-gradient(90deg, var(--rot), var(--violet)); border-radius:99px; }}

/* Table (Community past sessions) */
.simple-table {{ width:100%; border-collapse:collapse; }}
.simple-table th {{ text-align:left; font-family: var(--font-head); font-size:.78rem; text-transform:uppercase; letter-spacing:.05em;
  color:var(--dunkelgrau1); padding: 10px 14px; border-bottom:2px solid var(--grau3); }}
.simple-table td {{ padding: 14px 14px; border-bottom:1px solid var(--grau2); font-size:.92rem; }}
"""
print("CSS length:", len(BASE_CSS))
