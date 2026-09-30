# -*- coding: utf-8 -*-
"""Seiten unter „/ Entwicklung /“ → Kategorie „Strategie“.

- entwicklung-strategie-zielbild.html   Platzhalter
- entwicklung-meilensteine-fein.html    Liniennetz
- entwicklung-meilensteine-dunkel.html  Graph, dunkel
- entwicklung-meilensteine-hell.html    Graph, hell

Die Meilenstein-Logik ist aus sofort sichtbar übertragen (Branch daniel:
strategieGraph.js, meilenstein-kopf.njk, metro-plan.njk, graph-abschnitte.njk,
layouts/konzept.njk, strategie.js). Daten: entwicklung_strategie.json.

HARTE REGEL: Diese Seiten existieren nur auf dem Branch daniel. Auf jedem
anderen Branch baut dieses Skript nichts, und .githooks/pre-commit verweigert
Commits mit entwicklung-*.html.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from html import escape
from build_common import *
import entwicklung_graph

if not DEV_MENU:
    print("Entwicklungsseiten übersprungen: nicht auf Branch daniel.")
    sys.exit(0)

e = lambda t: escape(str(t), quote=True)

SEITE_SZ = "entwicklung-strategie-zielbild.html"
KONZEPTE = [
    ("fein", "entwicklung-meilensteine-fein.html"),
    ("dunkel", "entwicklung-meilensteine-dunkel.html"),
    ("hell", "entwicklung-meilensteine-hell.html"),
]

with open(os.path.join(WORKDIR, "entwicklung_meilensteine.css"), encoding="utf-8") as f:
    MS_CSS = f.read()
with open(os.path.join(WORKDIR, "entwicklung_meilensteine.js"), encoding="utf-8") as f:
    MS_JS = f.read()

g = entwicklung_graph.berechne()


# ---- Gemeinsamer Kopf (meilenstein-kopf.njk) -------------------------------
def kopf(konzept):
    ansichten = "".join(
        '<a class="mk__ansicht{0}" href="{1}"{2}>{3}</a>'.format(
            " is-aktiv" if k == konzept else "", href, ' aria-current="page"' if k == konzept else "", k)
        for k, href in KONZEPTE)
    if konzept == "fein":
        info = '''
            <p>Jeder Strang ist eine <b>Linie</b>, die von links nach rechts läuft.
              Jeder <b>Halt</b> darauf ist ein Schritt.</p>
            <p>Ein Abschnitt ist <b>dick</b>, wenn der Halt an seinem Ende erledigt ist oder
              gerade ansteht — sonst dünn. So zeigt die Linie selbst, wie weit der Strang
              gekommen ist.</p>
            <p>Die <b>nummerierten Stationen</b> sind Ergebnisstufen mit festem Termin. Dort muss jede Linie
              angekommen sein, bevor es weitergeht.</p>
            <p>Gestrichelte <b>Umstiege</b> zeigen, wo ein Strang auf einen anderen wartet.</p>
            <p>Ein Klick auf einen Halt zeigt die <b>Route dorthin</b>: alles, was nicht zu
              diesem Ziel führt, tritt zurück. Ein Klick daneben hebt das wieder auf.</p>'''
        eintraege = '''
        <span class="mk__eintrag"><i class="me__muster me__muster--fertig"></i>erledigt</span>
        <span class="mk__eintrag"><i class="me__muster me__muster--jetzt"></i>jetzt machbar</span>
        <span class="mk__eintrag"><i class="me__muster me__muster--wartet"></i>wartet noch</span>
        <span class="mk__eintrag"><i class="me__muster me__muster--dick"></i>Abschnitt erledigt oder dran</span>
        <span class="mk__eintrag"><i class="me__muster me__muster--duenn"></i>noch offen</span>
        <span class="mk__eintrag"><i class="me__muster me__muster--bogen"></i>Umstieg</span>'''
    else:
        info = '''
            <p>Von links nach rechts. Jeder <b>Pfeil</b> heißt „muss vorher fertig sein".</p>
            <p>Die drei <b>Bahnen</b> untereinander sind die Stränge. Links stehen ihre
              Themen und wer verantwortlich ist.</p>
            <p>Nach jedem Abschnitt steht eine <b>Ergebnisstufe</b> mit festem Termin. Dort muss jede der drei
              Bahnen angekommen sein, bevor der nächste Abschnitt beginnt.</p>
            <p>Ein Klick auf eine Karte zeigt ihre <b>Kette</b> nach vorn und nach hinten und
              öffnet die Details. Ein Klick daneben hebt das wieder auf.</p>'''
        eintraege = '''
        <span class="mk__eintrag"><i class="g2__zeichen g2__zeichen--fertig"></i>erledigt</span>
        <span class="mk__eintrag"><i class="g2__zeichen g2__zeichen--jetzt"></i>jetzt machbar</span>
        <span class="mk__eintrag"><i class="g2__zeichen g2__zeichen--wartet"></i>kommt später</span>
        <span class="mk__eintrag mk__eintrag--pfeil">muss vorher fertig sein</span>
        <span class="mk__eintrag mk__eintrag--quer">wartet auf andere Bahn</span>'''
    return '''
<header class="mk">
  <div class="mk__text">
    <h1 class="mk__titel">Meilensteine zur Transformation der SV Akademie</h1>
    <p class="mk__lead">
      Drei Stränge laufen parallel auf das Zielbild zu. Dazwischen liegen fünf
      Ergebnisstufen mit festen Terminen — jede ist erst erreicht, wenn alle drei
      Stränge ihren Teil erledigt haben.
    </p>
  </div>
  <div class="mk__boxen">
  <div class="mk__box mk__box--schalter">
    <span class="mk__box-titel">Darstellung</span>
    <nav class="mk__ansichten" aria-label="Darstellung wechseln">''' + ansichten + '''</nav>
  </div>
  <div class="mk__box mk__legende">
    <div class="mk__legende-kopf">
      <span class="mk__box-titel">Legende</span>
      <details class="mk__info">
        <summary aria-label="Wie ist das Bild zu lesen?"><span aria-hidden="true">i</span></summary>
        <div class="mk__info-panel">
          <h2>Wie das Bild zu lesen ist</h2>''' + info + '''
        </div>
      </details>
    </div>
    <div class="mk__eintraege">''' + eintraege + '''
    </div>
  </div>
  </div>
</header>'''


def _themen(strang):
    return "<span>%s</span>" % e(strang["frage"]) if strang["frage"] else ""


def _verantwortung(strang):
    v = strang.get("verantwortung")
    return '<em class="k-verantwortung">%s</em>' % e(v) if v else ""


def _ergebnis(m, klasse):
    # Ein Ergebnis kann ein Satz oder eine Liste von Punkten sein
    x = m["ergebnis"]
    if isinstance(x, list):
        return '<ul class="%s k-ergebnisliste">%s</ul>' % (klasse, "".join("<li>%s</li>" % e(p) for p in x))
    return '<span class="%s">%s</span>' % (klasse, e(x))


def _liste(ids):
    return e(" ".join(ids))


# ---- Liniennetz (metro-plan.njk) -------------------------------------------
def metro_plan():
    m = g["metro"]
    rail = "".join(
        '<div class="me__rail-bahn" style="top: {0}px; --f: {1}"><b>{2}</b>{3}{4}<i>{5}%</i></div>'.format(
            l["y"], l["farbe"], e(l["label"]), _themen(l), _verantwortung(l), l["fortschritt"]) for l in m["linien"])
    svg = ['<svg class="me__svg" width="{0}" height="{1}" aria-hidden="true"><defs>'
           '<marker id="mpfeil" viewBox="0 0 8 8" refX="6" refY="4" markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
           '<path d="M 0 0 L 8 4 L 0 8 z" class="me__quer-spitze" /></marker></defs>'.format(m["breite"], m["hoehe"])]
    for s in m["stationen"]:
        svg.append('<line class="me__stationslinie" x1="{0}" y1="96" x2="{0}" y2="{1}" />'.format(s["x"], m["hoehe"] - 30))
    # Umstiege zuerst – sie liegen unter den Linien
    for q in m["quer"]:
        svg.append('<path class="me__quer" data-von="{0}" data-nach="{1}" d="{2}" marker-end="url(#mpfeil)"><title>{3}</title></path>'.format(
            q["von"], q["nach"], q["pfad"], e(q["text"])))
    # Jede Linie zieht einen Saum in Hintergrundfarbe mit: dadurch bekommen
    # kreuzende Umstiege einen sauberen Abstand statt sich zu berühren.
    for l in m["linien"]:
        for a in l["abschnitte"]:
            svg.append('<path class="me__saum {0}" d="{1}" />'.format("me__saum--dick" if a["dick"] else "me__saum--duenn", a["pfad"]))
    for l in m["linien"]:
        for a in l["abschnitte"]:
            svg.append('<path class="me__linie {0}"{1} d="{2}" style="--f: {3}" />'.format(
                "me__linie--gegangen" if a["dick"] else "me__linie--offen",
                ' data-bis="%s"' % a["bis"] if a["bis"] else "", a["pfad"], l["farbe"]))
    svg.append("</svg>")
    stationen = "".join(
        '<div class="me__station{0}" style="left: {1}px"><span class="me__station-nr">{2}</span>'
        '<span class="me__station-titel">{3}</span>{4}'
        '<span class="me__station-balken"><i style="width: {5}%"></i></span></div>'.format(
            " is-erreicht" if s["erreicht"] else "", s["x"], s["nr"], e(s["titel"]), _ergebnis(s, "me__station-text"), s["fortschritt"])
        for s in m["stationen"])
    halte = "".join(
        '<button class="me__halt me__halt--{0}{1}" type="button" data-schritt="{2}" data-halt="{2}" data-knoten="{2}"'
        ' data-braucht="{3}" data-nachfolger="{4}" data-vorher="{5}" style="left: {6}px; top: {7}px; --f: {8}">'
        '<span class="me__halt-punkt"></span><span class="me__halt-label">{9}</span>{10}</button>'.format(
            s["status"], " is-machbar" if s["dran"] else "", s["id"], _liste(s["braucht"]), _liste(s["nachfolger"]),
            _liste(s["metroVorher"]), s["mx"], s["my"], s["farbe"], e(s["titel"]),
            '<span class="me__halt-wer">%s</span>' % e(s["wer"]) if s["wer"] else "")
        for s in g["schritte"])
    return '''
<div class="me me--v2">
''' + kopf("fein") + '''
  <div class="me__buehne">
    <aside class="me__rail" style="height: {0}px" aria-hidden="true">{1}</aside>
    <div class="me__scroll">
      <div class="me__plan" style="width: {2}px; height: {0}px">
        {3}
        {4}
        {5}
      </div>
    </div>
  </div>
  <div class="me__route" data-route-leiste hidden>
    <span class="me__route-text" data-route-text></span>
    <button class="me__route-zu" type="button" data-metro-reset>Ganzes Netz zeigen</button>
  </div>
</div>'''.format(m["hoehe"], rail, m["breite"], "".join(svg), stationen, halte)


# ---- Graph in Abschnitten (graph-abschnitte.njk) ---------------------------
def graph_abschnitte(konzept, variante):
    G = g["graph2"]
    band = G["bandLuft"]
    rail = "".join(
        '<div class="g2__rail-bahn" style="top: {0}px; height: {1}px; --f: {2}"><b>{3}</b>{4}{5}<i>{6}%</i></div>'.format(
            sp["y"] - band, sp["hoehe"] + band * 2, sp["farbe"], e(sp["label"]), _themen(sp), _verantwortung(sp), sp["fortschritt"])
        for sp in G["spuren"])
    stationen = "".join(
        '<div class="g2__station{0}" style="left: {1}px"><span class="g2__station-nr">{2}</span>'
        '<span class="g2__station-titel">{3}</span>{4}'
        '<span class="g2__station-balken"><i style="width: {5}%"></i></span>'
        '<span class="g2__station-quote">{5}% · {6} Schritte</span></div>'.format(
            " is-erreicht" if st["erreicht"] else "", st["x"], st["nr"], e(st["titel"]), _ergebnis(st, "g2__station-text"),
            st["fortschritt"], st["anzahl"]) for st in G["stationen"])
    tore = "".join('<div class="g2__tor{0}" style="left: {1}px"></div>'.format(
        " is-erreicht" if st["erreicht"] else "", st["x"]) for st in G["stationen"])
    # Das Band greift oben und unten über die Karten hinaus
    bahnen = "".join('<div class="g2__bahn" style="top: {0}px; height: {1}px; --f: {2}"></div>'.format(
        sp["y"] - band, sp["hoehe"] + band * 2, sp["farbe"]) for sp in G["spuren"])
    kanten = "".join('<path class="g2__kante{0}" data-von="{1}" data-nach="{2}" d="{3}" marker-end="url(#g2pfeil)" />'.format(
        " is-quer" if k["quer"] else "", k["von"], k["nach"], k["pfad"]) for k in G["kanten"])
    karten = "".join(
        '<button class="g2__karte g2__karte--{0}{1}" type="button" data-knoten="{2}" data-schritt="{2}"'
        ' data-braucht="{3}" data-nachfolger="{4}" style="left: {5}px; top: {6}px; width: {7}px; height: {8}px; --f: {9}">'
        '<span class="g2__karte-kopf"><i class="g2__zeichen" aria-hidden="true"></i>'
        '<span class="g2__karte-titel">{10}</span>{11}</span><span class="g2__karte-satz">{12}</span></button>'.format(
            s["status"], " is-machbar" if s["dran"] else "", s["id"], _liste(s["braucht"]), _liste(s["nachfolger"]),
            s["g2x"], s["g2y"], G["knotenBreite"], G["knotenHoehe"], s["farbe"], e(s["titel"]),
            '<span class="g2__wer" title="%s">%s</span>' % (e(s["werName"]), e(s["wer"])) if s["wer"] else "",
            e(s["ergebnis"])) for s in g["schritte"])
    return '''
<div class="g2 g2--{0}" data-g2>
''' .format(variante) + kopf(konzept) + '''
  <div class="g2__buehne">
    <aside class="g2__rail" aria-hidden="true">{0}</aside>
    <div class="g2__scroll">
    <div class="g2__inhalt" style="width: {1}px">
      <div class="g2__stationsreihe">{2}</div>
      <div class="g2__flaeche" style="height: {3}px">
        {4}
        {5}
        <svg class="g2__kanten" width="{1}" height="{3}" aria-hidden="true"><defs>
          <marker id="g2pfeil" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto-start-reverse">
            <path d="M 0 0 L 8 4 L 0 8 z" class="g2__spitze" /></marker></defs>{6}</svg>
        {7}
      </div>
    </div>
    </div>
  </div>
</div>'''.format(rail, G["breite"], stationen, G["hoehe"], tore, bahnen, kanten, karten)


# ---- Hülle mit Kopfleiste und Detailfenster (layouts/konzept.njk) -----------
def konzept_huelle(konzept, inhalt):
    details = []
    for s in g["schritte"]:
        teile = ['<article class="k-detail" data-detail="{0}" hidden><div class="k-detail__kopf">'
                 '<span class="k-detail__strang" style="--f: {1}">{2}</span>{3}</div>'
                 '<h2 class="k-detail__titel">{4}</h2>'
                 '{6}{5}'.format(
                     s["id"], s["farbe"], e(s["strangLabel"]),
                     '<span class="k-detail__wer" title="%s">%s</span>' % (e(s["werName"]), e(s["wer"])) if s["wer"] else "",
                     e(s["titel"]),
                     '<div class="k-detail__block"><h3>Aufwand</h3><p>%s</p></div>' % e(s["aufwandLabel"]) if s["aufwandLabel"] else "",
                     '<p class="k-detail__verantwortung">%s</p>' % e(s["verantwortung"]) if s["verantwortung"] else "")]
        if s["details"]:
            teile.append('<div class="k-detail__block"><h3>Inhalte</h3><ul>%s</ul></div>' % "".join("<li>%s</li>" % e(d) for d in s["details"]))
        teile.append('<div class="k-detail__block"><h3>Ergebnis</h3><p>%s</p></div>' % e(s["ergebnis"]))
        if s["offen"]:
            teile.append('<div class="k-detail__block"><h3>Offen</h3><ul class="k-detail__offen">%s</ul></div>' % "".join("<li>%s</li>" % e(o) for o in s["offen"]))
        teile.append("</article>")
        details.append("".join(teile))
    return '''
<div class="k k--{0}">
  <header class="k-bar">
    <a class="k-bar__zurueck" href="{1}">Strategie und Zielbild</a>
    <span class="k-bar__meta">{2}% · {3}/{4}</span>
  </header>
  {5}
  <div class="k-pop" data-pop hidden role="dialog" aria-label="Schrittdetails">
    <button class="k-pop__zu" type="button" data-pop-zu aria-label="Schließen">&times;</button>
    {6}
  </div>
</div>'''.format(konzept, SEITE_SZ, g["fortschritt"], len(g["erledigt"]), g["anzahl"], inhalt, "".join(details))


def schreibe(dateiname, html):
    with open(os.path.join(SITEDIR, dateiname), "w", encoding="utf-8") as f:
        f.write(html)
    print(dateiname, "written:", len(html), "chars")


for konzept, dateiname in KONZEPTE:
    inhalt = metro_plan() if konzept == "fein" else graph_abschnitte(konzept, "a" if konzept == "dunkel" else "c")
    schreibe(dateiname, page_shell(
        "Meilensteine – " + konzept + " — SV Akademie (Entwicklung)",
        "Meilensteine zur Transformation der SV Akademie – Arbeitsstand, nicht öffentlich.",
        "", konzept_huelle(konzept, inhalt),
        extra_head="<style>" + MS_CSS + "</style>", extra_js=MS_JS))


# ---- Strategie und Zielbild: Platzhalter -----------------------------------
SZ_BODY = '''
<section class="section">
  <div class="wrap" style="max-width:760px;">
    <h1 style="color:var(--dunkelgrau2);">Strategie und Zielbild</h1>
    <p class="lead" style="color:var(--dunkelgrau1);">Platzhalter – hier entsteht die Beschreibung von Strategie und Zielbild der SV Akademie.</p>
    <p style="margin-top:28px;">Wie sich der Weg dorthin verzweigt, zeigen die
      <a href="''' + KONZEPTE[0][1] + '''" style="color:var(--rot); text-decoration:underline;">Meilensteine</a>.</p>
  </div>
</section>
'''
schreibe(SEITE_SZ, page_shell(
    "Strategie und Zielbild — SV Akademie (Entwicklung)",
    "Strategie und Zielbild – Arbeitsstand, nicht öffentlich.",
    "", SZ_BODY))
