@font-face {
  font-family: 'Sparkasse Head';
  src: url('${font_head_uri}') format('truetype');
  font-weight: 400 800;
  font-style: normal;
  font-display: swap;
}
@font-face {
  font-family: 'Sparkasse Lt';
  src: url('${font_body_uri}') format('truetype');
  font-weight: 300 500;
  font-style: normal;
  font-display: swap;
}

:root {
  --rot: ${rot};
  --rot-dunkel: ${rot_dunkel};
  --dunkelgrau2: ${dunkelgrau2};
  --dunkelgrau1: ${dunkelgrau1};
  --grau6: ${grau6};
  --grau5: ${grau5};
  --grau4: ${grau4};
  --grau3: ${grau3};
  --grau2: ${grau2};
  --grau1: ${grau1};
  --hellgrau: ${hellgrau};
  --violet: ${violet};
  --blau: ${blau};
  --hellblau: ${hellblau};
  --dunkelgruen: ${dunkelgruen};
  --gelb: ${gelb};
  --orange: ${orange};
  --weiss: ${weiss};
  --schwarz: ${schwarz};
  --font-head: 'Sparkasse Head', 'Arial Narrow', Arial, sans-serif;
  --font-body: 'Sparkasse Lt', Arial, Helvetica, sans-serif;
  --maxw: 1180px;
  --radius: 14px;
  --shadow: 0 10px 30px rgba(0,0,0,0.08);
  --shadow-lg: 0 20px 50px rgba(0,0,0,0.14);
}

* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: var(--font-body);
  color: var(--dunkelgrau2);
  background: var(--weiss);
  -webkit-font-smoothing: antialiased;
  line-height: 1.6;
  font-size: 17px;
}
h1,h2,h3,h4 {
  font-family: var(--font-head);
  font-weight: 800;
  color: var(--dunkelgrau2);
  line-height: 1.15;
  margin: 0 0 .5em 0;
}
h1 { font-size: clamp(2rem, 4.2vw, 3.4rem); letter-spacing: -0.01em; }
h2 { font-size: clamp(1.6rem, 3vw, 2.4rem); }
h3 { font-size: 1.25rem; }
p { margin: 0 0 1em 0; }
a { color: var(--rot); text-decoration: none; }
.eyebrow {
  display: inline-flex; align-items: center; gap: 8px;
  font-family: var(--font-head); font-weight: 700;
  font-size: .78rem; letter-spacing: .12em; text-transform: uppercase;
  color: var(--rot); margin-bottom: 14px;
}
.eyebrow::before { content:""; width: 22px; height: 3px; background: var(--rot); border-radius: 2px; display:inline-block; }
.eyebrow-white { color: #fff; }
.eyebrow-white::before { background: #fff; }
.wrap { max-width: var(--maxw); margin: 0 auto; padding: 0 28px; }
.section { padding: 88px 0; position: relative; }
.section-tight { padding: 56px 0; }
.center { text-align: center; }
.muted { color: var(--dunkelgrau1); }
.small { font-size: .9rem; }
img { max-width: 100%; display:block; }

.btn {
  display: inline-flex; align-items:center; justify-content:center; gap:10px;
  font-family: var(--font-head); font-weight: 700; font-size: .98rem; line-height:1;
  padding: 15px 30px; border-radius: 999px; border: 2px solid transparent;
  cursor: pointer; transition: all .18s ease; white-space: nowrap;
}
.btn-primary { background: var(--rot); color: #fff; box-shadow: 0 8px 20px rgba(238,0,0,.28); }
.btn-primary:hover { background: var(--rot-dunkel); box-shadow: 0 12px 26px rgba(238,0,0,.35); }
.btn-ghost { background: transparent; border-color: rgba(255,255,255,.7); color: #fff; }
.btn-ghost:hover { background: rgba(255,255,255,.15); }
.btn-outline { background: #fff; border-color: var(--grau4); color: var(--dunkelgrau2); }
.btn-outline:hover { border-color: var(--rot); color: var(--rot); }
.btn-sm { padding: 10px 20px; font-size: .85rem; }
.btn-block { width: 100%; }
.btn[disabled] { opacity:.45; cursor:not-allowed; transform:none !important; }

.site-header {
  position: sticky; top: 0; z-index: 500;
  background: rgba(255,255,255,.92);
  border-bottom: 1px solid var(--grau2);
}
/* Der Weichzeichner sitzt auf einer eigenen Ebene: direkt am Header würde
   backdrop-filter den Header zum Bezugsrahmen des fixierten Handy-Menüs machen
   (Menü nur 56 px hoch, Seite auf dem Handy doppelt so breit). */
.site-header::before { content:""; position:absolute; inset:0; z-index:-1; backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px); }
.site-header .wrap { display:flex; align-items:center; justify-content:space-between; min-height: 96px; padding-top:8px; padding-bottom:8px; }
.brand { display:flex; align-items:center; gap:12px; flex-shrink:0; margin-right:32px; }
.brand img { height: 76px; width:auto; }
/* Logo links, Menüpunkte rechtsbündig bis an den CTA-Button */
.nav { display:flex; align-items:center; gap: 26px; margin-left:auto; }
.nav a { color: var(--dunkelgrau2); font-weight:600; font-size:.95rem; padding: 6px 2px; border-bottom: 2px solid transparent; white-space:nowrap; }
.nav a:hover, .nav a.active { color: var(--rot); border-color: var(--rot); }
.nav a.nav-kontakt-btn {
  flex-shrink:0; margin-left:6px; min-width:118px; text-align:center; text-decoration:none;
  display: inline-flex; align-items:center; justify-content:center; gap:10px;
  font-family: var(--font-head); font-weight: 700; font-size: .85rem; line-height:1;
  padding: 10px 20px; border-radius: 999px; border: 2px solid var(--grau4);
  background:#fff; color:var(--dunkelgrau2); box-shadow:none;
  cursor:pointer; transition: all .18s ease; white-space:nowrap;
}
.nav a.nav-kontakt-btn:hover { border-color:var(--rot); color:var(--rot); }
.nav-cta { display:flex; align-items:center; gap:14px; flex-shrink:0; margin-left:26px; }
.burger { display:none; background:none; border:none; cursor:pointer; padding:8px; }
.burger span { display:block; width:26px; height:3px; background:var(--dunkelgrau2); margin:5px 0; border-radius:2px; }

/* Burger-Menü unter 1280 px: darüber passt die volle Leiste samt „/ Entwicklung /“ */
@media (max-width: 1279px) {
  .nav { position:fixed; inset: 84px 0 0 0; background:#fff; flex-direction:column; align-items:flex-start;
    padding: 28px; gap:20px; transform: translateX(100%); transition: transform .25s ease; overflow:auto; }
  .nav.open { transform: translateX(0); }
  .burger { display:block; }
  .nav-cta .btn-outline { display:none; }
}
/* Logo, Button und Burger passen auf dem Handy nicht nebeneinander; der Button steht im Menü und im Aufmacher */
@media (max-width: 480px) { .nav-cta .btn-primary { display:none; } }

/* ---- Menüpunkt „/ Entwicklung /“ – nur in der Entwicklungsumgebung (Aufbau wie empiria) ---- */
.dev-dd { position:relative; display:inline-flex; align-items:center; }
.dev-dd-toggle { display:inline-flex; align-items:center; gap:.35rem; font-family:inherit; font-size:.95rem; font-weight:400; line-height:1.4; color:var(--grau6); background:none; border:0; padding:6px 0; cursor:pointer; white-space:nowrap; transition:color .18s ease; }
.dev-dd-toggle:hover, .dev-dd.is-open .dev-dd-toggle { color:var(--dunkelgrau2); }
.dev-dd-short { display:none; }
.dev-dd-chev { width:12px; height:12px; transition:transform .2s ease; }
.dev-dd.is-open .dev-dd-chev { transform:rotate(180deg); }
.dev-dd-panel { position:absolute; top:calc(100% + 18px); right:-14px; width:390px; padding:12px; background:#fff; border:1px solid var(--hellgrau); border-radius:18px; box-shadow:0 20px 50px rgba(0,0,0,.14); opacity:0; visibility:hidden; transform:translateY(6px); transition:opacity .16s ease, transform .16s ease, visibility .16s ease; z-index:600; text-align:left; }
.dev-dd-panel::before { content:""; position:absolute; left:0; right:0; top:-20px; height:20px; }
.dev-dd.is-open .dev-dd-panel { opacity:1; visibility:visible; transform:none; }
.dev-dd-note { margin:0 0 14px; padding:11px 13px; background:#fff400; color:#1a1817; border-radius:10px; font-size:12px; line-height:1.45; }
.dev-dd-note b { display:block; font-size:13px; font-weight:600; margin-bottom:2px; }
.dev-dd-group { margin:4px 8px 8px; font-size:11px; letter-spacing:.08em; text-transform:uppercase; color:var(--grau6); font-weight:600; }
.dev-dd-group--sub { margin-top:14px; padding-top:12px; border-top:1px solid var(--hellgrau); }
.dev-dd a.dev-dd-link, .nav .dev-dd a.dev-dd-link { display:flex; align-items:center; gap:12px; padding:9px 8px; border-radius:10px; border-bottom:0; color:var(--dunkelgrau2); font-weight:400; font-size:inherit; white-space:normal; text-decoration:none; }
.dev-dd a.dev-dd-link:hover, .dev-dd a.dev-dd-link.is-current, .nav .dev-dd a.dev-dd-link:hover { background:var(--hellgrau); color:var(--dunkelgrau2); }
.dev-dd-tag { flex:0 0 32px; height:32px; display:flex; align-items:center; justify-content:center; border-radius:8px; background:var(--dunkelgrau2); color:#fff; font-weight:600; font-size:12px; }
.dev-dd-txt { display:flex; flex-direction:column; line-height:1.3; min-width:0; }
.dev-dd-txt b { font-weight:500; font-size:14px; }
.dev-dd-txt small { font-size:12px; color:var(--grau6); margin-top:1px; }
.dev-dd-empty { margin:0 8px 4px; padding:6px 0; font-size:13px; color:var(--grau6); }
.dev-dd-sub { position:relative; }
.dev-dd a.dev-dd-link--parent::after { content:""; width:6px; height:6px; margin-left:auto; flex:0 0 auto; border-right:1.5px solid currentColor; border-bottom:1.5px solid currentColor; transform:rotate(-45deg); opacity:.45; }
.dev-dd-sub:hover > a.dev-dd-link--parent, .dev-dd-sub:focus-within > a.dev-dd-link--parent { background:var(--hellgrau); }
.dev-dd-flyout { position:absolute; right:100%; top:-10px; padding-right:10px; opacity:0; visibility:hidden; transition:opacity .16s ease, visibility .16s ease; z-index:601; }
.dev-dd-sub:hover > .dev-dd-flyout, .dev-dd-sub:focus-within > .dev-dd-flyout { opacity:1; visibility:visible; }
.dev-dd-flyout-panel { width:262px; padding:10px; background:#fff; border:1px solid var(--hellgrau); border-radius:14px; box-shadow:0 20px 50px rgba(0,0,0,.14); }
.dev-dd-flyout-panel .dev-dd-group { margin:2px 8px 6px; }
.dev-dd--corner { position:absolute; right:24px; top:0; bottom:0; }
.dev-dd--corner .dev-dd-panel { top:calc(100% - 4px); }
/* Auf dem Desktop immer die Kurzform – die Langform passt nicht neben Logo und Menüpunkte */
@media (min-width: 1280px) {
  .nav .dev-dd-long { display:none; }
  .nav .dev-dd-short { display:inline; }
}
@media (min-width: 1280px) and (max-width: 1400px) {
  .nav { gap:20px; }
  .nav-cta { margin-left:20px; }
}
@media (max-width: 1279px) {
  .nav .dev-dd { display:block; width:100%; }
  .nav .dev-dd-toggle { display:flex; width:100%; justify-content:space-between; font-size:.95rem; }
  .nav .dev-dd-flyout { position:static; opacity:1; visibility:visible; padding:0; }
  .nav .dev-dd-flyout-panel { width:auto; padding:0 0 0 12px; margin:2px 0 6px 20px; background:none; border:0; border-left:2px solid var(--hellgrau); border-radius:0; box-shadow:none; }
  .nav .dev-dd a.dev-dd-link--parent::after { display:none; }
  .nav .dev-dd-panel { position:static; width:auto; display:none; opacity:1; visibility:visible; transform:none; box-shadow:none; border:0; border-left:2px solid var(--hellgrau); border-radius:0; margin:10px 0 6px; padding:0 0 0 12px; }
  .nav .dev-dd-panel::before { display:none; }
  .nav .dev-dd.is-open .dev-dd-panel { display:block; }
}
@media (max-width: 900px) {
  .dev-dd--corner { right:16px; }
  .dev-dd--corner .dev-dd-flyout { position:static; opacity:1; visibility:visible; padding:0; }
  .dev-dd--corner .dev-dd-flyout-panel { width:auto; padding:0 0 0 12px; margin:2px 0 6px 20px; background:none; border:0; border-left:2px solid var(--hellgrau); border-radius:0; box-shadow:none; }
  .dev-dd--corner a.dev-dd-link--parent::after { display:none; }
  .dev-dd--corner .dev-dd-panel { position:fixed; top:96px; left:16px; right:16px; width:auto; max-height:calc(100vh - 112px); overflow:auto; }
}

.site-footer { background: var(--dunkelgrau2); color: #fff; padding: 56px 0 28px; }
.site-footer a { color: #fff; opacity:.85; }
.site-footer a:hover { opacity:1; text-decoration:underline; }
.footer-grid { display:grid; grid-template-columns: 1.4fr 1fr 1fr 1fr; gap: 40px; margin-bottom:40px; }
.footer-grid h4 { color:#fff; font-size:.95rem; text-transform:uppercase; letter-spacing:.06em; margin-bottom:14px; }
.footer-grid ul { list-style:none; padding:0; margin:0; display:flex; flex-direction:column; gap:10px; font-size:.92rem; }
.footer-bottom { border-top:1px solid rgba(255,255,255,.15); padding-top:22px; display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; font-size:.85rem; opacity:.75; }
@media (max-width:800px) { .footer-grid { grid-template-columns: 1fr 1fr; } }

.card { background:#fff; border:1px solid var(--grau2); border-radius: var(--radius); padding: 32px; transition: all .2s ease; }
.card:hover { box-shadow: var(--shadow); transform: translateY(-4px); border-color: var(--grau3); }
.grid { display:grid; gap: 26px; }
.grid-3 { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.grid-2 { grid-template-columns: repeat(2, 1fr); }
.grid-4 { grid-template-columns: repeat(4, minmax(0, 1fr)); }
@media (max-width: 900px) { .grid-3, .grid-4 { grid-template-columns: 1fr 1fr; } }
@media (max-width: 620px) { .grid-3, .grid-4, .grid-2 { grid-template-columns: 1fr; } }

.icon-badge {
  width:74px; height:74px; border-radius:50%; display:flex; align-items:center; justify-content:center;
  background: #fff; border: 2.5px solid; border-image: linear-gradient(135deg, var(--rot), var(--violet)) 1;
  margin-bottom: 20px; color: var(--dunkelgrau2);
}
.icon-badge svg { width: 34px; height:34px; }

.num-badge {
  width:40px;height:40px;border-radius:50%;background:var(--rot);color:#fff;
  display:flex;align-items:center;justify-content:center;font-family:var(--font-head);font-weight:800;
  flex-shrink:0;
}

.hero {
  position: relative; background: linear-gradient(135deg, var(--rot) 0%, #6a1f66 100%);
  color:#fff; overflow:hidden; padding-top: 70px;
}
.hero .wrap { position:relative; z-index:2; display:grid; grid-template-columns: 1.15fr .85fr; gap: 40px; align-items:center; padding-bottom: 90px; padding-top: 40px; }
.hero h1 { color:#fff; }
.hero p.lead { font-size:1.15rem; opacity:.95; max-width: 540px; }
.hero-ctas { display:flex; gap:16px; flex-wrap:wrap; margin-top: 30px; }
.hero-visual { display:flex; justify-content:center; align-items:center; }
.hero-visual img { max-width: 250px; filter: drop-shadow(0 30px 40px rgba(0,0,0,.35)); animation: float 5s ease-in-out infinite; }
@keyframes float { 0%,100% { transform: translateY(0);} 50% { transform: translateY(-16px);} }
.cloud-divider { position:absolute; left:0; right:0; bottom:-1px; line-height:0; z-index:1; }
.cloud-divider svg { width:100%; height: auto; display:block; }
.hero-stats { position:relative; z-index:2; display:flex; gap: 46px; flex-wrap:wrap; margin-top: 14px; }
.hero-stat b { font-family: var(--font-head); font-size:1.6rem; display:block; }
.hero-stat span { font-size:.85rem; opacity:.85; }
@media (max-width: 900px) { .hero .wrap { grid-template-columns: 1fr; text-align:center; } .hero-ctas, .hero-stats { justify-content:center; } .hero-visual img { max-width:220px; } }

.trust-bar { background: var(--hellgrau); padding: 38px 0; border-bottom: 1px solid var(--grau2); }
.trust-bar .wrap { display:flex; justify-content:center; flex-wrap:wrap; }
.trust-stat { flex:1; min-width:220px; text-align:center; padding: 0 30px; position:relative; }
.trust-stat:not(:last-child)::after { content:""; position:absolute; right:0; top:50%; transform:translateY(-50%); width:1px; height:46px; background:var(--grau3); }
.trust-stat b { display:block; font-family:var(--font-head); font-weight:800; font-size:2.2rem; color:var(--rot); line-height:1; margin-bottom:8px; }
.trust-stat span { font-size:.88rem; color:var(--dunkelgrau1); line-height:1.35; display:block; max-width:230px; margin:0 auto; }
@media (max-width:700px) {
  .trust-stat:not(:last-child)::after { display:none; }
  .trust-bar .wrap { flex-direction:column; gap:26px; }
}

.problem-row { display:flex; gap:20px; align-items:flex-start; padding: 22px 0; border-bottom: 1px solid var(--grau2); }
.problem-row:last-child { border-bottom:none; }
.problem-icon { font-size:1.6rem; flex-shrink:0; }

.timeline { display:grid; grid-template-columns: repeat(var(--tl-cols, 3),1fr); gap: 22px; counter-reset: step; margin-top: 50px; }
.timeline-step { position:relative; background:#fff; border:1px solid var(--grau2); border-radius: var(--radius); padding: 30px 24px; }
.timeline-step::before { counter-increment: step; content: counter(step); position:absolute; top:-18px; left:24px;
  width:36px;height:36px;border-radius:50%; background:var(--rot); color:#fff; display:flex;align-items:center;justify-content:center;
  font-family:var(--font-head); font-weight:800; box-shadow:0 6px 14px rgba(238,0,0,.35); }
.timeline-step h3 { margin-top: 10px; }
@media (max-width: 900px) { .timeline { grid-template-columns: 1fr 1fr; } }
@media (max-width: 600px) { .timeline { grid-template-columns: 1fr; } }

.lead-card { display:flex; flex-direction:column; height:100%; }
.lead-card .tag { align-self:flex-start; background: var(--grau1); color:var(--dunkelgrau1); font-size:.72rem; font-weight:700;
  text-transform:uppercase; letter-spacing:.06em; padding: 5px 12px; border-radius: 999px; margin-bottom:16px; }
.lead-card .tag.new { background: #FCE8E8; color: var(--rot); }
.step-tag { display:inline-flex; align-items:center; gap:8px; font-family:var(--font-head); font-weight:700; font-size:.72rem;
  text-transform:uppercase; letter-spacing:.06em; color:var(--dunkelgrau1); margin-bottom:16px; }
.step-tag .step-num { width:22px;height:22px;border-radius:50%; background:var(--rot); color:#fff; display:flex;
  align-items:center;justify-content:center; font-size:.72rem; flex-shrink:0; }
.icon-line { width:56px;height:56px; color:var(--rot); margin-bottom:18px; }
.icon-line svg { width:100%; height:100%; }
.lead-card p { flex-grow:1; }
.lead-card .btn { margin-top: 26px; }
.problem-card { display:flex; flex-direction:column; height:100%; }
.problem-card h3 { min-height: 46px; }
.problem-card p { flex-grow:1; }
.card-more-link { display:inline-flex; align-items:center; gap:6px; background:none; border:none; padding:0; margin-top:18px;
  font-family:var(--font-head); font-weight:700; font-size:.85rem; color:var(--rot); cursor:pointer; align-self:flex-start; }
.card-more-link:hover { color:var(--rot-dunkel); gap:9px; }

.detail-list { display:flex; flex-direction:column; }
.detail-row { position:relative; padding: 22px 0 22px 22px; border-bottom:1px solid var(--grau3); border-left:3px solid transparent;
  transition: border-color .25s ease, padding-left .25s ease; }
.detail-row:first-child { }
.detail-row:hover { border-left-color: var(--rot); padding-left:30px; }
.detail-row h3 { display:flex; align-items:center; justify-content:flex-start; gap:14px; margin-bottom:0; font-size:1.1rem; }
.detail-row h3 .detail-arrow { color:var(--rot); opacity:0; transform:translateX(-6px); transition: all .25s ease; flex-shrink:0; }
.detail-row:hover h3 .detail-arrow { opacity:1; transform:translateX(0); }
.detail-icon-badge { display:inline-flex; align-items:center; justify-content:center; width:34px; height:34px; border-radius:50%; border:2px solid var(--rot); color:var(--rot); flex-shrink:0; }
.detail-icon-badge svg { width:17px; height:17px; }
.detail-reveal { max-height:0; opacity:0; overflow:hidden; transition: max-height .35s ease, opacity .3s ease, margin-top .35s ease; margin-top:0; }
.detail-row:hover .detail-reveal { max-height:180px; opacity:1; margin-top:12px; }
.detail-reveal .card-more-link { margin-top:10px; }

.accordion-item { border-bottom: 1px solid var(--grau2); }
.accordion-item:first-child { border-top: 1px solid var(--grau2); }
.accordion-trigger {
  width:100%; text-align:left; background:none; border:none; cursor:pointer;
  display:flex; justify-content:space-between; align-items:center; gap:20px;
  padding: 22px 4px; font-family: var(--font-head); font-weight:700; font-size:1.05rem; color: var(--dunkelgrau2);
}
.accordion-trigger:hover { color: var(--rot); }
.accordion-plus { flex-shrink:0; width:28px;height:28px;border-radius:50%;border:2px solid var(--rot); color:var(--rot);
  display:flex;align-items:center;justify-content:center; font-size:1.1rem; transition: transform .2s ease; }
.accordion-item.open .accordion-plus { transform: rotate(135deg); background:var(--rot); color:#fff; }
.accordion-panel { max-height:0; overflow:hidden; transition: max-height .3s ease; }
.accordion-panel-inner { padding: 0 4px 24px 4px; color: var(--dunkelgrau1); }

.modal-overlay {
  position:fixed; inset:0; background: rgba(20,20,20,.55); display:flex; align-items:center; justify-content:center;
  z-index:1000; opacity:0; pointer-events:none; transition: opacity .2s ease; padding: 20px;
}
.modal-overlay.active { opacity:1; pointer-events:auto; }
.modal-box {
  background:#fff; border-radius: 18px; max-width: 480px; width:100%; padding: 40px; position:relative;
  transform: translateY(16px) scale(.98); transition: transform .25s ease; box-shadow: var(--shadow-lg); text-align:center;
}
.modal-overlay.active .modal-box { transform: translateY(0) scale(1); }
.modal-close { position:absolute; top:16px; right:16px; background:var(--grau1); border:none; width:34px;height:34px;
  border-radius:50%; cursor:pointer; font-size:1.1rem; color:var(--dunkelgrau1); }
.modal-icon { width:64px;height:64px;border-radius:50%; background: #E9F8F1; color: var(--dunkelgruen); display:flex;
  align-items:center;justify-content:center; margin: 0 auto 20px; font-size:1.8rem; }

.form-field { margin-bottom: 20px; text-align:left; }
.form-field label { display:block; font-weight:700; font-size:.85rem; margin-bottom:7px; color: var(--dunkelgrau2); }
.form-field input, .form-field select, .form-field textarea {
  width:100%; padding: 13px 16px; border-radius: 10px; border: 1.5px solid var(--grau3); font-family: var(--font-body);
  font-size: 1rem; background:#fff; color: var(--dunkelgrau2); transition: border-color .15s ease;
}
.form-field input:focus, .form-field select:focus, .form-field textarea:focus { outline:none; border-color: var(--rot); }
.form-row { display:grid; grid-template-columns:1fr 1fr; gap:18px; }
@media (max-width:600px) { .form-row { grid-template-columns:1fr; } }
.form-check { display:flex; align-items:flex-start; gap:10px; font-size:.85rem; color: var(--dunkelgrau1); }

.choice-card { display:block; border:2px solid var(--grau3); border-radius: var(--radius); padding:26px; cursor:pointer; text-align:left; background:#fff; transition: all .18s ease; text-decoration:none; color:inherit; }
.choice-card:hover { border-color: var(--rot); box-shadow: var(--shadow); transform: translateY(-2px); }
.choice-card.selected { border-color: var(--rot); box-shadow: 0 0 0 4px rgba(238,0,0,.08); }
.choice-card .radio-dot { width:22px;height:22px;border-radius:50%;border:2px solid var(--grau4); margin-bottom:14px; position:relative; }
.choice-card.selected .radio-dot { border-color: var(--rot); }
.choice-card.selected .radio-dot::after { content:""; position:absolute; inset:3px; border-radius:50%; background:var(--rot); }

.slot-btn { border:1.5px solid var(--grau3); background:#fff; border-radius:10px; padding:12px 10px; cursor:pointer; font-weight:700; font-size:.85rem; text-align:center; }
.slot-btn:hover { border-color: var(--grau5); }
.slot-btn.selected { background: var(--rot); border-color:var(--rot); color:#fff; }
.slot-grid { display:grid; grid-template-columns: repeat(3,1fr); gap:10px; }

.pill { display:inline-block; padding:5px 14px; border-radius:999px; font-size:.75rem; font-weight:700; letter-spacing:.03em; }
.pill-red { background:#FCE8E8; color:var(--rot); }
.pill-green { background:#E1F5EC; color:var(--dunkelgruen); }
.pill-grau { background:var(--grau1); color:var(--dunkelgrau1); }

.bg-grau { background: var(--hellgrau); }
.bg-dunkel { background: var(--dunkelgrau2); color:#fff; }
#kontakt.section { padding: 140px 0; }
@media (max-width:700px) { #kontakt.section { padding: 90px 0; } }
.bg-dunkel h2, .bg-dunkel h3 { color:#fff; }

/* Quick-Check Wizard */
.wizard-progress { display:flex; align-items:center; justify-content:center; gap:6px; margin-bottom:38px; flex-wrap:wrap; }
.wizard-progress-step { display:flex; align-items:center; gap:8px; font-size:.8rem; font-weight:700; color:var(--grau5); }
.wizard-progress-step .num { width:26px;height:26px;border-radius:50%; border:2px solid var(--grau4); display:flex;align-items:center;justify-content:center;
  font-size:.76rem; color:var(--grau5); flex-shrink:0; background:#fff; transition: all .2s ease; }
.wizard-progress-step.active { color:var(--dunkelgrau2); }
.wizard-progress-step.active .num { border-color:var(--rot); background:var(--rot); color:#fff; }
.wizard-progress-step.done .num { border-color:var(--rot); background:#fff; color:var(--rot); }
.wizard-progress-step.done .num::after { content:"\2713"; }
.wizard-progress-line { width:26px; height:2px; background:var(--grau3); flex-shrink:0; }
.wizard-progress-label { display:none; }
@media (min-width:640px) { .wizard-progress-label { display:inline; } }

.wizard-panel { display:none; }
.wizard-panel.active { display:block; }
.wizard-situation-content { display:none; }
.wizard-situation-content.active { display:block; }

.wizard-nav { display:flex; justify-content:space-between; align-items:center; margin-top:36px; gap:14px; flex-wrap:wrap; }
.wizard-lock-note { display:flex; align-items:center; gap:10px; background:var(--hellgrau); border-radius:var(--radius); padding:16px 20px; font-size:.88rem; color:var(--dunkelgrau1); margin-top:24px; }

.sparring-box { background:var(--hellgrau); border-radius:var(--radius); padding:28px; margin-top:10px; }
.sparring-box h3 { margin-bottom:6px; }

/* KI-Lernassistent - KI-Chat-Vorschau */
.ai-chat-widget { background:#fff; border-radius:22px; box-shadow: var(--shadow-lg); overflow:hidden; max-width:720px; margin:0 auto; border:1px solid var(--grau2); }
.ai-chat-topbar { background: var(--dunkelgrau2); color:#fff; padding:16px 24px; display:flex; align-items:center; gap:12px; }
.ai-chat-topbar .dot { width:10px; height:10px; border-radius:50%; background:#4ADE80; flex-shrink:0; }
.ai-chat-body { padding:30px 26px; min-height:200px; display:flex; flex-direction:column; gap:14px; max-height:420px; overflow-y:auto; }
.ai-chat-bubble { max-width:82%; padding:13px 18px; border-radius:16px; font-size:.92rem; line-height:1.5; }
.ai-chat-bubble.user { align-self:flex-end; background:var(--rot); color:#fff; border-bottom-right-radius:4px; }
.ai-chat-bubble.assistant { align-self:flex-start; background:var(--hellgrau); color:var(--dunkelgrau2); border-bottom-left-radius:4px; }
.ai-chat-empty { text-align:center; color:var(--dunkelgrau1); padding:10px 4px; margin:auto; }
.ai-chat-empty p { font-size:.92rem; }
.ai-chat-inputrow { display:flex; gap:10px; padding:16px 20px; border-top:1px solid var(--grau2); background:#fff; }
.ai-chat-inputrow input { flex:1; border:1.5px solid var(--grau3); border-radius:999px; padding:13px 20px; font-family:var(--font-body); font-size:.95rem; color:var(--dunkelgrau2); }
.ai-chat-inputrow input:focus { outline:none; border-color:var(--rot); }
.ai-chat-send { width:46px; height:46px; border-radius:50%; background:var(--rot); color:#fff; border:none; display:flex;
  align-items:center; justify-content:center; cursor:pointer; flex-shrink:0; font-size:1.1rem; transition: background .15s ease; }
.ai-chat-send:hover { background:var(--rot-dunkel); }

.suggestion-chips { display:flex; flex-wrap:wrap; gap:10px; margin-top:6px; justify-content:center; }
.suggestion-chip { background:#fff; border:1.5px solid var(--grau3); border-radius:999px; padding:10px 18px; font-size:.83rem;
  cursor:pointer; color:var(--dunkelgrau2); transition:all .15s ease; font-family:var(--font-body); }
.suggestion-chip:hover { border-color:var(--rot); color:var(--rot); }
.ai-typing { display:inline-flex; gap:4px; align-items:center; }
.ai-typing span { width:6px; height:6px; border-radius:50%; background:var(--grau5); display:inline-block; animation: aiTypingBounce 1.1s infinite ease-in-out; }
.ai-typing span:nth-child(2) { animation-delay:.15s; }
.ai-typing span:nth-child(3) { animation-delay:.3s; }
@keyframes aiTypingBounce { 0%, 60%, 100% { transform: translateY(0); opacity:.5; } 30% { transform: translateY(-4px); opacity:1; } }

.mobile-cta-bar { display:none; }
@media (max-width:700px) {
  .mobile-cta-bar { display:flex; position:fixed; bottom:0; left:0; right:0; background:#fff; border-top:1px solid var(--grau2);
    padding:12px 16px; z-index:400; box-shadow: 0 -6px 20px rgba(0,0,0,.08); gap:10px; }
}

.reveal { opacity:0; transform: translateY(24px); transition: opacity .6s ease, transform .6s ease; }
.reveal.visible { opacity:1; transform:none; }

.page-hero { background: linear-gradient(135deg, var(--rot) 0%, #6a1f66 100%); color:#fff; padding: 130px 0 70px; }
.page-hero h1 { color:#fff; }
.breadcrumb { font-size:.85rem; opacity:.75; margin-bottom:18px; }
.breadcrumb a { color:#fff; }

.login-card { background:#fff; border-radius:20px; box-shadow: var(--shadow-lg); padding:44px; max-width:420px; margin: -90px auto 0; position:relative; z-index:5; }
.dash-mock { background:#fff; border-radius:16px; border:1px solid var(--grau2); overflow:hidden; box-shadow: var(--shadow); }
.dash-topbar { background: var(--dunkelgrau2); color:#fff; padding:14px 22px; display:flex; align-items:center; justify-content:space-between; font-size:.85rem; }
.dash-body { display:grid; grid-template-columns: 220px 1fr; min-height: 380px; }
.dash-side { background: var(--hellgrau); padding: 22px 16px; border-right:1px solid var(--grau2); }
.dash-side a { display:block; padding:10px 12px; border-radius:8px; color:var(--dunkelgrau2); font-weight:600; font-size:.9rem; margin-bottom:4px; }
.dash-side a.active { background:#fff; color:var(--rot); box-shadow:0 2px 6px rgba(0,0,0,.06); }
.dash-main { padding: 26px; }
.progress-bar { height:8px; background:var(--grau2); border-radius:99px; overflow:hidden; margin-top:8px; }
.progress-bar > span { display:block; height:100%; background: linear-gradient(90deg, var(--rot), var(--violet)); border-radius:99px; }

.simple-table { width:100%; border-collapse:collapse; }
.simple-table th { text-align:left; font-family: var(--font-head); font-size:.78rem; text-transform:uppercase; letter-spacing:.05em;
  color:var(--dunkelgrau1); padding: 10px 14px; border-bottom:2px solid var(--grau3); }
.simple-table td { padding: 14px 14px; border-bottom:1px solid var(--grau2); font-size:.92rem; }
@media (max-width:480px) { .simple-table th, .simple-table td { padding-left:8px; padding-right:8px; } }

.badge-check { color: var(--dunkelgruen); font-weight:700; }

/* Cycle diagram (Kreislauf) - CSS Grid based, self-sizing, no manual height guessing */
.cycle-diagram { position:relative; max-width:640px; margin:36px auto 0; padding: 30px 10px; }
.cycle-ring { position:absolute; inset:0; z-index:0; pointer-events:none; }
.cycle-grid {
  position:relative; z-index:1;
  display:grid; grid-template-columns: 1fr 1fr; grid-template-areas: "a b" "c c";
  column-gap: 24px; row-gap: 34px; align-items:start;
}
.cycle-node { text-align:center; }
.cycle-node-a { grid-area:a; }
.cycle-node-b { grid-area:b; }
.cycle-node-c { grid-area:c; max-width:260px; margin:0 auto; }
.cycle-icon { width:44px;height:44px; margin:0 auto 12px; color:var(--rot); }
.cycle-icon svg { width:100%; height:100%; }
.cycle-node p { font-size:.86rem; color:var(--dunkelgrau1); margin:0; line-height:1.5; }
@media (max-width: 640px) {
  .cycle-ring { display:none; }
  .cycle-grid { grid-template-columns: 1fr; grid-template-areas: "a" "b" "c"; row-gap:26px; }
  .cycle-node-c { max-width:100%; }
}

/* Illustration tiles (Zusammenarbeit-Karten) - fixed height so card content never shifts */
.illus-box { width:100%; height:190px; margin:0 auto 14px; display:flex; align-items:center; justify-content:center; overflow:hidden; }
.illus-box svg { height:100%; width:auto; max-width:100%; display:block; transform: rotate(-2.5deg); }
.lead-card:nth-child(2) .illus-box svg { transform: rotate(2deg); }
.lead-card:nth-child(3) .illus-box svg { transform: rotate(-1.5deg); }
.two-col { display:grid; grid-template-columns: 1fr 1fr; gap:60px; align-items:center; }
@media (max-width:900px) { .two-col { grid-template-columns:1fr; gap:30px; } }
.divider { height:1px; background:var(--grau2); margin: 40px 0; border:none; }
.kicker-card { background:#fff; border:1px solid var(--grau2); border-radius:var(--radius); padding:24px; }

/* Cycle diagram v2: single static SVG image (no CSS layout, cannot ever shift/overlap) */
.cycle-static { max-width:560px; margin:36px auto 0; display:block; }
.cycle-connector { width:2px; height:70px; margin:0 auto; border-left:3px dashed var(--hellgrau); }

/* Circle icon badge variant (Handlungsfelder / Unsere 3 Teams) */
.icon-badge-circle { width:74px; height:74px; border-radius:50%; display:flex; align-items:center; justify-content:center;
  background:#fff; border:2.5px solid var(--rot); margin-bottom:20px; color:var(--rot); }
.icon-badge-circle svg { width:32px; height:32px; }

/* Leader profile card in page-hero */
.leader-card { display:flex; flex-direction:column; align-items:center; text-align:center; }
.leader-photo { width:150px; height:150px; border-radius:50%; overflow:hidden; border:4px solid rgba(255,255,255,.85);
  box-shadow:0 10px 30px rgba(0,0,0,.25); margin-bottom:18px; background:#fff; flex-shrink:0; }
.leader-photo img, .leader-photo svg { width:100%; height:100%; object-fit:cover; display:block; }
.leader-name { font-family:var(--font-head); font-weight:700; font-size:1.05rem; color:#fff; margin-bottom:2px; }
.leader-role { font-size:.85rem; color:#fff; opacity:.8; margin-bottom:16px; }
.leader-quote { font-size:.92rem; color:#fff; opacity:.95; font-style:italic; max-width:280px; line-height:1.55; }

/* Team-Karten mit Mouse-Over (Unsere 3 Teams) */
.team-card { position:relative; overflow:hidden; }
.team-hover-overlay {
  position:absolute; inset:0; background:var(--rot); color:#fff; border-radius:var(--radius);
  display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center;
  padding:28px; transform:translateY(100%); transition:transform .35s ease; z-index:2;
}
.team-card:hover .team-hover-overlay { transform:translateY(0); }
.team-hover-photo { width:76px; height:76px; border-radius:50%; overflow:hidden; border:3px solid rgba(255,255,255,.9);
  margin-bottom:14px; background:#fff; flex-shrink:0; }
.team-hover-photo img, .team-hover-photo svg { width:100%; height:100%; object-fit:cover; display:block; }
.team-hover-name { font-family:var(--font-head); font-weight:700; font-size:1.02rem; margin-bottom:2px; }
.team-hover-role { font-size:.8rem; opacity:.9; margin-bottom:14px; }
.team-hover-text { font-size:.86rem; opacity:.96; margin-bottom:18px; line-height:1.45; max-width:220px; }
.team-hover-overlay .btn-primary { background:#fff; color:var(--rot); box-shadow:none; }
.team-hover-overlay .btn-primary:hover { background:rgba(255,255,255,.88); color:var(--rot-dunkel); }

/* Clickable image that opens an enlarged pop-up */
.img-clickable { cursor:pointer; transition: transform .2s ease, box-shadow .2s ease; }
.img-clickable:hover { transform: translateY(-2px); box-shadow: var(--shadow-lg); }
.img-modal-box { max-width:920px; width:100%; padding:16px; text-align:left; }
.img-modal-box img { width:100%; border-radius:10px; display:block; }

/* PDF preview card */
.pdf-preview-card { display:flex; gap:26px; align-items:center; background:#fff; border:1px solid var(--grau2); border-radius:var(--radius); padding:26px; cursor:pointer; transition: all .2s ease; }
.pdf-preview-card:hover { box-shadow: var(--shadow); border-color: var(--grau3); }
.pdf-preview-thumb { width:110px; height:150px; flex-shrink:0; border-radius:8px; overflow:hidden; border:1px solid var(--grau2); box-shadow:0 6px 16px rgba(0,0,0,.1); background:var(--hellgrau); display:flex; align-items:center; justify-content:center; }
.pdf-preview-thumb img { width:100%; height:100%; object-fit:contain; object-position:center; }
@media (max-width:560px) { .pdf-preview-card { flex-direction:column; text-align:center; } }
.pdf-modal-box { max-width:520px; width:100%; max-height:88vh; display:flex; flex-direction:column; padding:0; overflow:hidden; }
.pdf-modal-scroll { overflow-y:auto; padding:20px; background:var(--hellgrau); }
.pdf-modal-scroll img { width:100%; border-radius:8px; box-shadow:0 8px 24px rgba(0,0,0,.15); }
.pdf-modal-footer { padding:16px 20px; border-top:1px solid var(--grau2); text-align:center; background:#fff; }

/* Team grid (42 Dummy-Profile) */
.team-grid { display:grid; grid-template-columns: repeat(7, 1fr); gap: 22px 14px; margin-top:40px; }
.team-member { text-align:center; }
.team-avatar { width:64px; height:64px; border-radius:50%; margin:0 auto 10px; background:var(--grau1); display:flex; align-items:center; justify-content:center; overflow:hidden; border:2px solid var(--grau2); }
.team-avatar svg { width:60%; height:60%; color:var(--grau5); }
.team-member .t-name { font-family:var(--font-head); font-weight:700; font-size:.78rem; color:var(--dunkelgrau2); line-height:1.3; margin-bottom:2px; }
.team-member .t-role { font-size:.68rem; color:var(--dunkelgrau1); line-height:1.3; }
@media (max-width:900px) { .team-grid { grid-template-columns: repeat(4, 1fr); } }
@media (max-width:560px) { .team-grid { grid-template-columns: repeat(3, 1fr); gap:18px 8px; } }
