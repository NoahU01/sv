# -*- coding: utf-8 -*-
import json, os
from string import Template

WORKDIR = os.path.dirname(os.path.abspath(__file__))
SITEDIR = os.path.abspath(os.path.join(WORKDIR, "..", ".."))
os.makedirs(SITEDIR, exist_ok=True)

with open(os.path.join(WORKDIR, "assets_b64.json")) as f:
    B64 = json.load(f)

FONT_HEAD_URI = "data:font/ttf;base64," + B64['font_head']
FONT_BODY_URI = "data:font/ttf;base64," + B64['font_body']
LOGO_COLOR_URI = "data:image/png;base64," + B64['logo_color']
LOGO_WHITE_URI = "data:image/png;base64," + B64['logo_white']
ROCKET_URI = "data:image/png;base64," + B64['rocket']

C = {
    "rot": "#EE0000", "rot_dunkel": "#B30000",
    "dunkelgrau2": "#444444", "dunkelgrau1": "#666666",
    "grau6": "#999999", "grau5": "#BBBBBB", "grau4": "#CCCCCC",
    "grau3": "#D9D9D9", "grau2": "#E3E3E3", "grau1": "#E9E9E9",
    "hellgrau": "#F0F0F0", "violet": "#9B348E", "blau": "#2C57D2",
    "hellblau": "#00ACD3", "dunkelgruen": "#009864", "gelb": "#FFC900",
    "orange": "#FF8F00", "weiss": "#FFFFFF", "schwarz": "#000000",
}

ICON_ELEARNING = '<svg viewBox="0 0 250 250" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="10"><path d="M27.5,12.51h195s15,0,15,15v150s0,15-15,15H27.5s-15,0-15-15V27.51s0-15,15-15"/><path d="M162.5,237.51h-75l7.5-45h60l7.5,45Z"/><path d="M65,237.51h120"/><path d="M192.5,80.01v22.5"/><path d="M162.5,93.35v39.16c-10.22,9.41-23.54,14.74-37.43,15-13.93-.28-27.28-5.61-37.57-15v-39.16"/><path d="M57.5,80.01l67.5,30,67.5-30-67.5-30-67.5,30Z"/></g></svg>'

ICON_GRADUATE = '<svg viewBox="0 0 250 250" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="10"><path d="M177.5,65c0,28.99-23.51,52.5-52.5,52.5s-52.5-23.51-52.5-52.5V12.5h105v52.5Z"/><path d="M27.5,237.5c0-53.85,43.65-97.5,97.5-97.5s97.5,43.65,97.5,97.5"/><path d="M12.5,12.5h225"/><path d="M72.5,57.5h105"/><path d="M27.5,12.5v75"/><path d="M75.13,153.71l49.87,38.79,49.87-38.79"/></g></svg>'

ICON_CONVERSATION = '<svg viewBox="0 0 250 250" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="10"><path d="M222.5,192.5h-105l-60,45v-45h-30c-8.28,0-15-6.72-15-15h0V27.5c0-8.28,6.72-15,15-15h195c8.28,0,15,6.72,15,15v150c0,8.28-6.72,15-15,15Z"/><path d="M148.96,72.5c0,12.43,10.07,22.5,22.5,22.5s22.5-10.07,22.5-22.5-10.07-22.5-22.5-22.5-22.5,10.07-22.5,22.5Z"/><path d="M210.43,125c-12.43-21.52-39.96-28.89-61.48-16.45-6.83,3.95-12.51,9.62-16.45,16.45"/><path d="M61.25,76.25c0,14.5,11.75,26.25,26.25,26.25s26.25-11.75,26.25-26.25h0c0-14.5-11.75-26.25-26.25-26.25s-26.25,11.75-26.25,26.25h0Z"/><path d="M42.5,155c0-24.85,20.15-45,45-45s45,20.15,45,45"/></g></svg>'

print("common part loaded")

with open(os.path.join(WORKDIR, "style.css.tpl"), encoding="utf-8") as f:
    css_tpl = f.read()

css_map = dict(C)
css_map.update({
    "font_head_uri": FONT_HEAD_URI,
    "font_body_uri": FONT_BODY_URI,
})
BASE_CSS = Template(css_tpl).substitute(**css_map)
print("BASE_CSS chars:", len(BASE_CSS))

# Hauptnavigation – zur Startseite führt das Logo, ein eigener Punkt „Start“ entfällt
PAGES = [
    ("ueber-uns.html", "Über uns"),
    ("quickcheck.html", "Quick-Check"),
    ("portal.html", "KI-Lernassistent"),
    ("community.html", "Community-Austausch"),
]

# ---- Menüpunkt „/ Entwicklung /“ ----
# Existiert NUR auf dem Branch `daniel`, niemals auf main:
# 1. Build: Das Menü wird nur eingebaut, wenn der ausgecheckte Branch `daniel` ist.
# 2. Laufzeit: Selbst dann erscheint es nur lokal und auf der Vercel-Vorschau
#    des Branches (svakademie-git-daniel-…), sonst entfernt das Inline-Skript es.
# 3. Ein Git-Hook (.githooks/pre-commit) verweigert Commits auf main mit dem Menü.
import subprocess
def _git_branch():
    try:
        return subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                                       cwd=WORKDIR, stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return ""
DEV_MENU = _git_branch() == "daniel"
# Nur neue Unterseiten, die Daniel entwickelt und die noch nicht auf main sind –
# keine Seiten, die schon in der Hauptnavigation stehen.
# (href, tag, titel, unterzeile[, [(href, tag, titel, unterzeile), …] für ein Flyout])
DEV_UNTERSEITEN = []
# Weitere Kategorien unter „Unterseiten“: (Überschrift, [(href, tag, titel, unterzeile), …])
# Ein Eintrag kann Unterpunkte tragen: (href, tag, titel, unterzeile, gruppe, [Unterpunkte])
# → Flyout, beliebig tief. Die SV-Akademie-Seiten liegen 1:1 aus dem empiria-Repo
# (Branch Daniel, site/projekte/) in entwicklung-empiria/.
_EMP = "entwicklung-empiria/projekte/"
DEV_KATEGORIEN = [
    ("Strategie", [
        (_EMP + "sv-akademie.html", "SV", "SV Akademie", "Steuerungsseite · drei Module", "Die Module", [
            (_EMP + "sv-selbstverstaendnis.html", "1", "Selbstverständnis", "Wofür stehen wir?"),
            (_EMP + "sv-vision.html", "2", "Vision", "Wie wollen wir wahrgenommen werden?"),
            (_EMP + "sv-strategie.html", "3", "Strategie", "Wie kommen wir dorthin?", "Darunter", [
                (_EMP + "sv-strategie-ist.html", "IS", "Ist-Situation", "SWOT-Logik und was einfließt"),
                (_EMP + "sv-strategie-stossrichtungen.html", "ST", "Stoßrichtungen", "Herkunft, Auswahl, Nachweis"),
                (_EMP + "sv-meilensteine.html", "MS", "Meilensteinplan", "Drei Stränge · fein, hell, dunkel"),
                (_EMP + "sv-abstimmung-hal.html", "AG", "Agenda Vision & Strategie", "Workshop mit dem Hauptabteilungsleiter"),
            ]),
            (_EMP + "sv-projektplanung.html", "PP", "Projektplanung", "Termine, Agenden und der Meilensteinplan"),
        ]),
        ("entwicklung-meilensteine-fein.html", "MS", "Meilensteine", "Transformation der SV Akademie · fein, dunkel, hell"),
    ]),
]
DEV_ARCHIV = []  # (href, tag, titel, unterzeile)

def _dev_link(href, tag, title, sub, extra=""):
    return ('<a href="{0}" class="dev-dd-link{4}"><span class="dev-dd-tag">{1}</span>'
            '<span class="dev-dd-txt"><b>{2}</b><small>{3}</small></span></a>').format(href, tag, title, sub, extra)

def _dev_eintrag(e):
    # Eintrag mit Unterpunkten wird zum Flyout – rekursiv, also beliebig tief
    if len(e) > 4:
        href, tag, title, sub, gruppe, kinder = e
        return ('<div class="dev-dd-sub">' + _dev_link(href, tag, title, sub, " dev-dd-link--parent")
                + '<div class="dev-dd-flyout"><div class="dev-dd-flyout-panel"><p class="dev-dd-group">' + gruppe + '</p>'
                + "".join(_dev_eintrag(k) for k in kinder) + '</div></div></div>')
    return _dev_link(*e)

def dev_dropdown_html(extra_class=""):
    if not DEV_MENU:
        return ""
    items = []
    for entry in DEV_UNTERSEITEN:
        href, tag, title, sub = entry[:4]
        children = entry[4] if len(entry) > 4 else []
        if children:
            fly = "".join(_dev_link(*c) for c in children)
            items.append('<div class="dev-dd-sub">' + _dev_link(href, tag, title, sub, " dev-dd-link--parent")
                         + '<div class="dev-dd-flyout"><div class="dev-dd-flyout-panel"><p class="dev-dd-group">Die Varianten</p>'
                         + fly + '</div></div></div>')
        else:
            items.append(_dev_link(href, tag, title, sub))
    archiv = "".join(_dev_link(*a) for a in DEV_ARCHIV) or '<p class="dev-dd-empty">Noch keine archivierten Stände.</p>'
    return ('<div class="dev-dd' + extra_class + '" data-dev-dd>'
            '<button class="dev-dd-toggle" type="button" aria-expanded="false"><span class="dev-dd-long">/ Entwicklung /</span>'
            '<span class="dev-dd-short" aria-hidden="true">/ Entw. /</span>'
            '<svg class="dev-dd-chev" viewBox="0 0 12 12" aria-hidden="true"><path d="M2.5 4.5 6 8l3.5-3.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg></button>'
            '<div class="dev-dd-panel">'
            '<p class="dev-dd-note"><b>Nur in der Entwicklungsumgebung sichtbar</b>Dieser Menüpunkt ist in der Live-Version nicht enthalten.</p>'
            '<p class="dev-dd-group">Unterseiten</p>' + ("".join(items) or '<p class="dev-dd-empty">Noch keine neuen Unterseiten.</p>') +
            "".join('<p class="dev-dd-group dev-dd-group--sub">' + name + '</p>' + "".join(_dev_eintrag(l) for l in links)
                    for name, links in DEV_KATEGORIEN) +
            '<p class="dev-dd-group dev-dd-group--sub">Archiv</p>' + archiv +
            '</div></div>'
            "<script>(function(){var h=location.hostname,d=document.currentScript.previousElementSibling;"
            "if(!(location.protocol==='file:'||h==='localhost'||h==='127.0.0.1'||/^svakademie-git-daniel-/.test(h)))d.remove();})();</script>")

def nav_html(active):
    links = []
    for href, label in PAGES:
        cls = "active" if href == active else ""
        links.append('<a href="{0}" class="{1}">{2}</a>'.format(href, cls, label))
    kontakt_href = "index.html#kontakt" if active != "index.html" else "#kontakt"
    nav_inner = "\n      ".join(links)
    return '''
  <header class="site-header">
    <div class="wrap">
      <a href="index.html" class="brand">
        <img src="''' + LOGO_COLOR_URI + '''" alt="SV Akademie Logo" />
      </a>
      <nav class="nav" id="mainNav">
        ''' + nav_inner + '''
        ''' + dev_dropdown_html() + '''
        <a href="''' + kontakt_href + '''" class="nav-kontakt-btn">Kontakt</a>
      </nav>
      <div class="nav-cta">
        <a href="portal.html" class="btn btn-primary btn-sm">KI-Lernassistent entdecken</a>
        <button class="burger" id="burgerBtn" aria-label="Menü öffnen"><span></span><span></span><span></span></button>
      </div>
    </div>
  </header>
'''

def minimal_header_html():
    return '''
  <header class="site-header">
    <div class="wrap" style="justify-content:center; position:relative;">
      <a href="index.html" class="brand">
        <img src="''' + LOGO_COLOR_URI + '''" alt="SV Akademie Logo" />
      </a>
      ''' + dev_dropdown_html(" dev-dd--corner") + '''
    </div>
  </header>
'''

def footer_html(schlank=False):
    if schlank:
        # Nur die Zeile zur Sparkassen-Finanzgruppe – für die Strategieseiten unter „/ Entwicklung /“
        return '''
  <footer class="site-footer site-footer--schlank">
    <div class="wrap"><span>&copy; 2026 SV Akademie &mdash; Teil der Sparkassen-Finanzgruppe.</span></div>
  </footer>
'''
    return '''
  <footer class="site-footer" id="impressum">
    <div class="wrap">
      <div class="footer-grid">
        <div>
          <div style="height:70px; width:100px; overflow:hidden; display:flex; align-items:center; justify-content:center; margin-bottom:6px;">
            <img src="''' + LOGO_WHITE_URI + '''" alt="SV Akademie" style="height:91px; width:auto; display:block; flex-shrink:0;" />
          </div>
          <p class="small" style="opacity:.75; max-width:320px;">Wir sind Dein Ansprechpartner für Bildung und Weiterentwicklung. Die SV Akademie begleitet Führungskräfte, Mitarbeitende und Vertriebspartner der SV in ihrer beruflichen und persönlichen Entwicklung.</p>
        </div>
        <div>
          <h4>Angebote</h4>
          <ul>
            <li><a href="quickcheck.html">Quick-Check Bedarfsklärung</a></li>
            <li><a href="portal.html">KI-Lernassistent</a></li>
            <li><a href="community.html">Community-Austausch</a></li>
            <li><a href="ueber-uns.html">Über uns</a></li>
          </ul>
        </div>
        <div>
          <h4>Service</h4>
          <ul>
            <li><a href="index.html#faq">FAQ</a></li>
            <li><a href="index.html#kontakt">Kontakt</a></li>
          </ul>
        </div>
        <div>
          <h4>Rechtliches</h4>
          <ul>
            <li><a href="#" onclick="openLegalModal('impressum'); return false;">Impressum</a></li>
            <li><a href="#" onclick="openLegalModal('datenschutz'); return false;">Datenschutz</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>&copy; 2026 SV Akademie &mdash; Teil der Sparkassen-Finanzgruppe. Strategie-Mock-up, nicht produktiv im Einsatz.</span>
        <span>Konzept &amp; Entwicklung: Strategieprojekt SV Akademie 4.0</span>
      </div>
    </div>
  </footer>

  <div class="modal-overlay" id="legalModal">
    <div class="modal-box" style="max-width:600px; text-align:left;">
      <button class="modal-close" onclick="closeModal('legalModal')">&times;</button>
      <div id="legalModalContent"></div>
    </div>
  </div>
'''

CLOUD_DIVIDER_TO_WHITE = '''<div class="cloud-divider"><svg viewBox="0 0 1440 120" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg"><path fill="#ffffff" d="M0,80 C120,110 240,40 360,55 C480,70 540,110 660,100 C780,90 840,30 960,35 C1080,40 1140,95 1260,90 C1350,86 1410,60 1440,50 L1440,120 L0,120 Z"/></svg></div>'''


with open(os.path.join(WORKDIR, "shared.js.tpl"), encoding="utf-8") as f:
    SHARED_JS = f.read()

LEITFADEN_PDF_URI = "data:application/pdf;base64," + B64['leitfaden_pdf']

def page_shell(title, description, active, body_html, extra_head="", extra_js="", header_override=None, footer_schlank=False):
    header = header_override if header_override is not None else nav_html(active)
    return '''<!DOCTYPE html>
<html lang="de">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>''' + title + '''</title>
<meta name="description" content="''' + description + '''" />
<meta name="robots" content="noindex, nofollow" />
<style>''' + BASE_CSS + '''</style>
''' + extra_head + '''
</head>
<body>
''' + header + '''
''' + body_html + '''
''' + footer_html(footer_schlank) + '''
<script>
''' + SHARED_JS + '''
''' + extra_js + '''
</script>
</body>
</html>'''

print("Shell + JS ready. LEITFADEN_PDF_URI length:", len(LEITFADEN_PDF_URI))

SELBSTBILD_PDF_URI = "data:application/pdf;base64," + B64['selbstbild_pdf']
SELBSTBILD_PREVIEW_URI = "data:image/png;base64," + B64['selbstbild_preview_png']
EINBETTUNG_DIAGRAM_URI = "data:image/png;base64," + B64['einbettung_diagram_png']
print("ueber-uns assets ready")

ONEPAGER_BUDGET_PDF_URI = "data:application/pdf;base64," + B64['onepager_budget_pdf']
ONEPAGER_KLAERUNG_PDF_URI = "data:application/pdf;base64," + B64['onepager_klaerung_pdf']
ONEPAGER_AUFBAU_PDF_URI = "data:application/pdf;base64," + B64['onepager_aufbau_pdf']

ONEPAGER_BUDGET_PREVIEW_URI = "data:image/png;base64," + B64['onepager_budget_preview_png']
ONEPAGER_KLAERUNG_PREVIEW_URI = "data:image/png;base64," + B64['onepager_klaerung_preview_png']
ONEPAGER_AUFBAU_PREVIEW_URI = "data:image/png;base64," + B64['onepager_aufbau_preview_png']
print("quick-check onepager assets ready")
