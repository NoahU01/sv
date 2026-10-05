# -*- coding: utf-8 -*-
"""Projekt-Repository SV Akademie: baut entwicklung-empiria/ aus den Originalen.

Quelle: _projektquelle/entwicklung-empiria-quelle/ – die Seiten 1:1 aus dem
empiria-Repo (NoahU01/empiria, Branch Daniel, site/). Layout, Logo, Kopf und
Fuß bleiben empiria. Angepasst wird nur, was sonst in die empiria-Homepage
führen würde – das Projekt-Repository steht für sich:

- absolute Pfade (/styles.css, /assets/…) werden relativ
- Logo und „Zur Startseite“ führen zur Projektübersicht (projekte/sv-akademie.html)
- Hauptnavigation (Problem, Lösung, Leistungen) und „Kontakt“ entfallen
- Menü „/ Entwicklung /“ zeigt nur das Projekt und die SV-Homepage
  (gleicher Inhalt wie auf den SV-Seiten, aus build_common.DEV_KATEGORIEN)
- „Zur Webseite gehen“ führt auf die SV-Homepage in diesem Branch
- Impressum/Datenschutz ohne empiria-Tracking (Google Analytics, Cookiebot)

Neuen Stand aus empiria holen: Dateien in die Quelle legen, dieses Skript
laufen lassen. Nur auf dem Branch daniel.
"""
import sys, os, re, glob
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_common import WORKDIR, SITEDIR, DEV_MENU, dev_panel_inhalt

if not DEV_MENU:
    print("entwicklung-empiria übersprungen: nicht auf Branch daniel.")
    sys.exit(0)

QUELLE = os.path.abspath(os.path.join(WORKDIR, "..", "entwicklung-empiria-quelle"))
ZIEL = os.path.join(SITEDIR, "entwicklung-empiria")

# Flyouts des empiria-Menüs öffnen nach rechts; das Menü steht jetzt am
# rechten Rand, deshalb nach links.
CSS_PROJEKT = ('<style>/* Projekt-Repository SV */'
               '.dev-dd--desktop .dev-dd-flyout{left:auto;right:100%;padding-left:0;padding-right:10px}'
               '.dev-dd-empty{margin:0 8px 4px;padding:6px 0;font-size:13px;color:var(--grey-50,#8a8a8a)}'
               '</style>')


def _div_ende(s, start):
    """Position direkt hinter dem </div>, das das <div> bei start schließt."""
    tiefe, i = 0, start
    for m in re.finditer(r'<div\b|</div>', s[start:]):
        tiefe += 1 if m.group(0) == "<div" else -1
        if tiefe == 0:
            return start + m.end()
    raise ValueError("kein schließendes </div>")


def panel_ersetzen(s, praefix):
    pos = 0
    while True:
        i = s.find('<div class="dev-dd-panel">', pos)
        if i < 0:
            return s
        j = _div_ende(s, i)
        neu = '<div class="dev-dd-panel">' + dev_panel_inhalt(praefix) + '</div>'
        s = s[:i] + neu + s[j:]
        pos = i + len(neu)


def bauen(rel):
    s = open(os.path.join(QUELLE, rel), encoding="utf-8").read()
    tiefe = rel.count("/")                      # projekte/x.html → 1
    zur_wurzel = "../" * tiefe                  # bis entwicklung-empiria/
    zum_repo = "../" * (tiefe + 1)              # bis zur SV-Homepage

    # 1. absolute Pfade relativ
    s = re.sub(r'((?:href|src|action|poster|data-[a-z-]+)=")/(?!/)', r'\1' + zur_wurzel, s)

    # 2. Logo → Projektübersicht
    uebersicht = ("" if tiefe else "projekte/") + "sv-akademie.html"
    s = re.sub(r'<a class="brand" href="[^"]*" aria-label="[^"]*">',
               '<a class="brand" href="%s" aria-label="Projekt SV Akademie">' % uebersicht, s)
    s = re.sub(r'<a href="[^"]*" class="brand" aria-label="[^"]*">',
               '<a href="%s" class="brand" aria-label="Projekt SV Akademie">' % uebersicht, s)

    # 2b. „Zur Startseite“ (Impressum, Datenschutz) → Projektübersicht
    s = re.sub(r'(<a class="btn[^"]*nav-back" href=")[^"]*(">)Zur Startseite(</a>)',
               r'\g<1>' + uebersicht + r'\g<2>Zur Projektübersicht\g<3>', s)

    # 3. Hauptnavigation und Kontakt raus
    s = re.sub(r'\s*<nav class="nav-links"[^>]*>.*?</nav>', '', s, count=1, flags=re.S)
    s = re.sub(r'\s*<a class="btn btn--dark[^"]*"[^>]*href="[^"]*#kontakt">.*?</a>', '', s, flags=re.S)

    # 4. Mobiles Menü: nur das Menü „/ Entwicklung /“ bleibt
    m = re.search(r'(<nav class="mobile-menu"[^>]*>)(.*?)(<!-- ENTWICKLUNG:START)', s, re.S)
    if m:
        s = s[:m.start(2)] + "\n" + s[m.end(2):]

    # 5. Menü „/ Entwicklung /“: nur Projekt und SV-Homepage
    s = panel_ersetzen(s, zum_repo)
    if 'dev-dd--desktop' in s and "Projekt-Repository SV" not in s:
        s = s.replace("</head>", CSS_PROJEKT + "\n</head>", 1)

    # 6. Absprung zur Webseite → SV-Homepage in diesem Branch
    s = s.replace('href="https://svakademie.vercel.app/"', 'href="%sindex.html"' % zum_repo)

    # 7. Kein empiria-Tracking
    s = re.sub(r'\s*<script async src="https://www\.googletagmanager\.com/[^"]*"[^>]*></script>\s*<script[^>]*>.*?</script>',
               '', s, flags=re.S)
    s = re.sub(r'\s*<script id="Cookiebot"[^>]*></script>', '', s)
    s = re.sub(r'\s*<script src="[^"]*tracking\.js"[^>]*></script>', '', s)

    ziel = os.path.join(ZIEL, rel)
    os.makedirs(os.path.dirname(ziel), exist_ok=True)
    with open(ziel, "w", encoding="utf-8") as f:
        f.write(s)
    return rel


seiten = sorted(os.path.relpath(p, QUELLE) for p in glob.glob(os.path.join(QUELLE, "**", "*.html"), recursive=True))
for rel in seiten:
    bauen(rel)
print("entwicklung-empiria:", len(seiten), "Seiten gebaut")
