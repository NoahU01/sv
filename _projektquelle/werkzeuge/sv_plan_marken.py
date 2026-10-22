#!/usr/bin/env python3
"""Setzt die eigenen Marken in den Meilensteinplan der SV Akademie.

Der Plan selbst wird aus dem SV-Repo gebaut (entwicklung_strategie.json ->
entwicklung_seiten.py). Dessen Datenmodell kennt nur Status, Abhaengigkeit
und Text - zwei Dinge fehlen uns:

  * ein Hinweis, dass hinter einem Schritt eine eigene Seite liegt,
  * eine Markierung kritischer Schritte.

Beides wird hier nachtraeglich eingesetzt, in alle drei Ansichten. Das
Skript ist wiederholbar: was schon steht, wird nicht doppelt gesetzt. Nach
jedem Neubau des Plans einmal laufen lassen.

    python3 _projektquelle/werkzeuge/sv_plan_marken.py          # setzen
    python3 _projektquelle/werkzeuge/sv_plan_marken.py --probe  # nur zeigen

Umgezogen aus dem empiria-Repo (22.10.2026): Die Marken gehen in die
Originale (_projektquelle/entwicklung-empiria-quelle/projekte/), danach
python3 _projektquelle/build-skripte/entwicklung_empiria.py laufen lassen.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # SV-Repo
SEITEN = ["_projektquelle/entwicklung-empiria-quelle/projekte/sv-meilensteine.html",
          "_projektquelle/entwicklung-empiria-quelle/projekte/sv-meilensteine-fein.html",
          "_projektquelle/entwicklung-empiria-quelle/projekte/sv-meilensteine-dunkel.html"]

# ---------------------------------------------------------------------------
# Die Marken. Schluessel ist die Schritt-ID aus entwicklung_strategie.json.
# ---------------------------------------------------------------------------
MARKEN = {
    "sa-1-hal": {
        "seite": "/projekte/sv-abstimmung-hal.html",
        "linktext": "Agenda zum Workshop ansehen",
    },
    "t1-1-copilot": {
        "kritisch": {
            "grund": "Wie lange die Pilotierung l\u00e4uft, ist offen.",
            "blockiert": "Davon h\u00e4ngt ab, wann die Entwicklung des KI-Assistenten Lea "
                         "starten kann \u2013 und mit ihr die Kette bis zur Webseite.",
        },
    },
}

ZEICHEN_MEHR = ('<span class="k-mehr" aria-hidden="true" title="Es gibt eine eigene Seite dazu">'
                '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" '
                'stroke-linecap="round" stroke-linejoin="round"><path d="M7 5l6 7-6 7"/>'
                '<path d="M14 5l6 7-6 7"/></svg></span>')
ZEICHEN_KRITISCH = '<span class="k-kritisch" title="Kritischer Punkt">!</span>'

CSS = '''
/* MARKEN-ANFANG (werkzeuge/sv_plan_marken.py - nicht von Hand aendern) */
/* --- Eigene Marken im Plan --------------------------------------------
   Die Karten tragen ihre Formsprache schon: linker Balken die Bahn, Ring
   den Status, gestrichelt heisst wartet. Fuer "kritisch" bleibt nur ein
   freier Kanal - eine Farbe, die keine Bahn benutzt. Ember steht im CD und
   ist hier unbelegt, deshalb liest sich der Ring eindeutig als Warnung und
   nicht als vierter Strang. */
.k-mehr { position: absolute; top: 9px; right: 10px; width: 15px; height: 15px;
          color: var(--f, #0B9FBD); opacity: .85; }
.k-mehr svg { width: 100%; height: 100%; display: block; }
.me__halt .k-mehr { top: -22px; right: auto; left: 50%; transform: translateX(-50%); }

.k-kritisch { position: absolute; top: 7px; right: 8px; width: 17px; height: 17px;
              display: grid; place-items: center; border-radius: 50%;
              background: #F0603A; color: #fff; font-size: 11px; font-weight: 800;
              font-style: normal; line-height: 1; }
.k-mehr + .k-kritisch, .k-kritisch + .k-mehr { right: 29px; }
/* Der Ring liegt im box-shadow, damit er dem Rahmen nicht in die Quere
   kommt - der traegt Bahn und Status. */
.g2 .g2__karte.ist-kritisch { box-shadow: 0 0 0 2px #F0603A; }
.me__halt .k-kritisch { top: -24px; right: auto; left: 50%; transform: translateX(-50%); }
.me .me__halt.ist-kritisch .me__halt-punkt { box-shadow: 0 0 0 4px #F0603A; }
.mk__eintrag--kritisch::before { content: ""; flex: none; width: .7rem; height: .7rem;
                                 border-radius: 50%; background: #F0603A; }
.k-detail__block--kritisch h3 { color: #F0603A; }
.k-detail__block--mehr { margin-top: 2px; }
/* Das Detailfenster ist in jeder Ansicht dunkel - auch in der hellen. Ein
   dunkler Link waere darin unsichtbar, deshalb steht er in empiria-Gelb. */
.k-mehr-link { display: inline-flex; align-items: center; gap: 8px; font-weight: 600;
               color: #fff400; text-decoration: underline; text-underline-offset: 3px; }
.k-mehr-link:hover { color: #ffffff; }
/* MARKEN-ENDE */
'''.strip()

LEGENDE = '<span class="mk__eintrag mk__eintrag--kritisch">kritisch &middot; Dauer oder Abh&auml;ngigkeit offen</span>'


def _karte(t, schritt_id):
    """Findet die Karte (Graph) oder den Halt (Liniennetz) eines Schritts."""
    for muster in (r'(<button class="[^"]*g2__karte[^>]*data-knoten="%s"[^>]*>)(.*?)(</button>)' % schritt_id,
                   r'(<button class="[^"]*me__halt[^>]*data-halt="%s"[^>]*>)(.*?)(</button>)' % schritt_id):
        m = re.search(muster, t, re.S)
        if m:
            return m
    return None


def setze(t, schritt_id, marke):
    befund = []
    m = _karte(t, schritt_id)
    if not m:
        return t, ["%s: keine Karte gefunden" % schritt_id]
    auf, innen, zu = m.group(1), m.group(2), m.group(3)

    if "seite" in marke and 'class="k-mehr"' not in innen:
        innen += ZEICHEN_MEHR
        befund.append("%s: Hinweis auf die eigene Seite" % schritt_id)
    if "kritisch" in marke:
        if 'class="k-kritisch"' not in innen:
            innen += ZEICHEN_KRITISCH
            befund.append("%s: als kritisch markiert" % schritt_id)
        if "ist-kritisch" not in auf:
            auf = auf.replace('class="', 'class="ist-kritisch ', 1)
    t = t[:m.start()] + auf + innen + zu + t[m.end():]

    # Detailfenster: Begruendung und Weg zur Unterseite
    d = re.search(r'(<article class="k-detail" data-detail="%s".*?)(</article>)' % schritt_id, t, re.S)
    if d:
        block = ""
        if "kritisch" in marke and "k-detail__block--kritisch" not in d.group(1):
            k = marke["kritisch"]
            block += ('<div class="k-detail__block k-detail__block--kritisch"><h3>Kritischer Punkt</h3>'
                      '<p>%s</p><p>%s</p></div>' % (k["grund"], k["blockiert"]))
            befund.append("%s: Begruendung im Detailfenster" % schritt_id)
        if "seite" in marke and "k-mehr-link" not in d.group(1):
            block += ('<div class="k-detail__block k-detail__block--mehr">'
                      '<a class="k-mehr-link" href="%s">%s &#8594;</a></div>'
                      % (marke["seite"], marke["linktext"]))
            befund.append("%s: Link im Detailfenster" % schritt_id)
        if block:
            t = t[:d.start()] + d.group(1) + block + d.group(2) + t[d.end():]
    return t, befund


def main(probe=False):
    gesamt = []
    for rel in SEITEN:
        p = os.path.join(ROOT, rel)
        t0 = open(p, encoding="utf-8").read()
        t = t0
        for schritt_id, marke in MARKEN.items():
            t, befund = setze(t, schritt_id, marke)
            gesamt += ["  %s  %s" % (os.path.basename(rel), b) for b in befund]
        # Stylesheet: alten Block entfernen, aktuellen setzen - sonst stehen
        # nach dem zweiten Lauf zwei Fassungen derselben Regeln da.
        hatte_css = CSS in t
        t = re.sub(r"/\* MARKEN-ANFANG.*?/\* MARKEN-ENDE \*/\n\n", "", t, flags=re.S)
        t = re.sub(r"/\* --- Hinweis auf eine eigene Seite.*?\.k--dunkel \.k-mehr-link \{ color: #ffffff; \}\n\n", "", t, flags=re.S)
        if CSS not in t:
            t = t.replace(".k-verantwortung { display: block;", CSS + "\n\n.k-verantwortung { display: block;", 1)
            if not hatte_css:
                gesamt.append("  %s  Stylesheet gesetzt" % os.path.basename(rel))
        if "mk__eintrag--kritisch" not in t.split("<style")[-1] or LEGENDE not in t:
            t, n = re.subn(r'(</div>\s*</div>\s*</details>|)(\s*)(</div>\s*</header>)', r'\1\2\3', t, count=0)
            m = re.search(r'(<span class="mk__eintrag mk__eintrag--quer">[^<]*</span>|'
                          r'<span class="mk__eintrag"><i class="me__muster me__muster--bogen"></i>[^<]*</span>)', t)
            if m and LEGENDE not in t:
                t = t[:m.end()] + LEGENDE + t[m.end():]
                gesamt.append("  %s  Legende ergaenzt" % os.path.basename(rel))
        if t != t0 and not probe:
            open(p, "w", encoding="utf-8").write(t)
    print("\n".join(gesamt) if gesamt else "Nichts zu tun - alle Marken sitzen.")
    if probe:
        print("\n[Probe] nichts geschrieben.")


if __name__ == "__main__":
    main(probe="--probe" in sys.argv)
