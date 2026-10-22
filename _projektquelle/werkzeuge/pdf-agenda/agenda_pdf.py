#!/usr/bin/env python3
"""Baut zwei PDFs der Workshop-Agenda - zum Moderieren und zum Mitnehmen.

    moderation  4 Seiten, 11 pt, Notizspalte rechts. Zum Ausdrucken und
                Danebenlegen. Kein Block bricht ueber eine Seitengrenze.
    kompakt     2 Seiten, eng gesetzt, ohne Notizspalte. Fuer die Tasche.

Die Seiten sind feste Kaesten von 210x297 mm, keine Fliesspaginierung.
Nur so laesst sich "Seite X von Y" verlaesslich setzen - Chrome kennt die
CSS-Zaehler fuer Druckseiten nicht.

Aufruf:  python3 _projektquelle/werkzeuge/pdf-agenda/agenda_pdf.py [zielordner]

Umgezogen aus dem empiria-Repo (22.10.2026). Das Vorschaubild kommt aus
dem PDF-Werkzeug von empiria (werkzeuge/pdf-vorlage) - dafuer muss das
empiria-Repo daneben liegen (~/Projekte/empiria) oder EMPIRIA_REPO gesetzt sein.
"""
import os, pathlib, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from agenda_lesen import bloecke, kopf, BEGINN

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent          # SV-Repo
SITE = ROOT / "entwicklung-empiria"       # gebaute Projektseiten
EMPIRIA = pathlib.Path(os.environ.get("EMPIRIA_REPO", pathlib.Path.home() / "Projekte" / "empiria"))
BUILD = HERE / "_build"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

TITEL = "Workshop Vision &amp; Strategie"
DATUM = "06. Oktober 2026"

# Welche Bloecke auf welche Seite. Geprueft wird das ueber die Messung in
# messen.py - bleibt unten Platz, passt mehr drauf.
VERTEILUNG = {"moderation": [[1, 2], [3, 4], [5]],
              "kompakt": [[1, 2], [3, 4, 5]]}

# Die kompakte Fassung geht an die Teilnehmer, auch an den
# Hauptabteilungsleiter. Wie wir vorgehen, gehoert dort in einen Satz -
# die Einzelschritte sind Regie fuer uns und haben auf seinem Tisch
# nichts zu suchen. Leitfragen und Abschluss bleiben unveraendert, sie
# sind Gespraechsgegenstand, keine Taktik.
OHNE_REGIE = {"Ergebnis", "Vorgehen", "Die Story"}
TEILNEHMERSATZ = {
    "01": "Wir steigen direkt ein, knüpfen an das Statement von M.\u00a0S. aus "
          "dem letzten Termin an und legen Ziel und Ablauf der zwei Stunden "
          "offen – einschließlich der Punkte, die heute bewusst offenbleiben.",
    "02": "Wir greifen die Aussagen aus dem letzten Termin auf und hören, was "
          "für M.\u00a0S. heute die beste Akademie der Versicherungsbranche "
          "ausmacht.",
    "03": "Wir führen beide Bilder zusammen: zuerst die Kriterien, an denen "
          "sich die beste Akademie der Branche messen lässt, dann die Vision, "
          "wie die SV Akademie künftig arbeitet, was sie anbietet und wie sie "
          "auftritt.",
    "04": "Wir stellen die entwickelten Stoßrichtungen vor und prüfen sie "
          "gemeinsam auf der Ebene der Richtungen – die Ausarbeitung folgt "
          "im Anschluss.",
    "05": "Wir sprechen darüber, wie M.\u00a0S. die Akademie künftig "
          "begleitet.",
}

CSS = r"""
@page { size: A4; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
:root { --ink:#1a1817; --g70:#58564f; --g50:#8a8783; --g25:#d8d4cf;
        --bg:#f4f3f1; --hl:#fff400;
        --serif:"Lora",Georgia,serif; --sans:"Poppins",sans-serif; }
body { font-family: var(--sans); font-weight: 300; color: var(--ink);
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
b, strong { font-weight: 600; }

.page { width: 210mm; height: 297mm; position: relative; overflow: hidden;
        padding: 16mm 15mm 16mm 18mm; page-break-after: always; }
.page:last-child { page-break-after: auto; }

/* Das Logo steht auf jeder Seite an derselben Stelle: rechtsbuendig mit
   dem Satzspiegel, Oberkante auf Hoehe der Ueberschrift. */
.logo { position: absolute; top: 18mm; right: 15mm; height: 5.5mm; }
.fuss { position: absolute; left: 18mm; right: 15mm; bottom: 11mm;
        display: flex; justify-content: space-between; align-items: baseline;
        font-size: 7.6pt; color: var(--g50); }

/* Corporate Design: Das Gelb liegt hinter dem Wort, das Wort steht im
   700er-Schnitt, die Ecken sind gerundet. Die Zeilenhoehe traegt den
   Kasten - sonst schneidet er die Unterlaengen der Zeile darueber ab. */
h1 { font-family: var(--serif); font-weight: 600; font-size: 26pt;
     line-height: 1.42; letter-spacing: -.01em; max-width: 150mm; }
/* Das Polster des gelben Kastens wird durch einen gleich grossen
   negativen Aussenabstand ausgeglichen. Sonst rueckt das hervorgehobene
   Wort nach rechts und flucht nicht mehr mit der Zeile darueber - der
   Kasten darf links ueberstehen, der Text nicht. Genau so loest es die
   Website in styles.css. */
.hl { display: inline; color: var(--ink); font-weight: 700;
      background: var(--hl); border-radius: .14em;
      padding: .06em .12em; margin-inline: -.12em;
      -webkit-box-decoration-break: clone; box-decoration-break: clone; }
.unterzeile { margin-top: 5mm; font-size: 10pt; color: var(--g70); }
.unterzeile b { font-weight: 600; color: var(--ink); }

.tag { font-size: 7.6pt; font-weight: 600; letter-spacing: .13em;
       text-transform: uppercase; color: var(--g50); margin-bottom: 3mm; }
h2 { font-family: var(--serif); font-weight: 600; font-size: 14pt;
     line-height: 1.25; margin-bottom: 5mm; }

/* ---- Seite 1: Ziel des Termins ---------------------------------------- */
.ziele { display: grid; grid-template-columns: repeat(3, 1fr); gap: 5mm;
         margin-bottom: 7mm; }
.ziel { border-top: 1.2pt solid var(--ink); padding-top: 3mm; }
.ziel .nr { font-family: var(--serif); font-weight: 700; font-size: 9pt;
            color: var(--g50); }
.ziel b { display: block; font-size: 10pt; line-height: 1.3; margin: 1.2mm 0 2mm; }
.ziel p { font-size: 8.8pt; line-height: 1.55; color: var(--g70); }

.zitat { background: var(--bg); border-radius: 3mm; padding: 6mm;
         margin-bottom: 6mm; }
.zitat p { font-family: var(--serif); font-weight: 500; font-size: 11.5pt;
           line-height: 1.5; }
.zitat span { display: block; margin-top: 3mm; font-size: 7.6pt;
              font-weight: 600; letter-spacing: .12em; text-transform: uppercase;
              color: var(--g50); }
.nichtziel { margin-bottom: 8mm; }
.nichtziel span { display: block; font-size: 7.6pt; font-weight: 600;
                  letter-spacing: .12em; text-transform: uppercase;
                  color: var(--g50); margin-bottom: 2mm; }
.nichtziel p { font-size: 9.2pt; line-height: 1.6; color: var(--g70); }

/* ---- Ablauf auf einen Blick ------------------------------------------- */
.uz { display: grid; grid-template-columns: 22mm 8mm 1fr 16mm;
      gap: 3mm; align-items: baseline;
      padding: 3mm 0; border-bottom: .4pt solid var(--g25); }
.uebersicht .uz:first-child { border-top: .4pt solid var(--g25); }
.uz .zeit { font-size: 9.4pt; font-weight: 500; }
.uz .nr { font-family: var(--serif); font-weight: 700; font-size: 9pt;
          color: var(--g50); }
.uz .was { font-size: 10pt; }
.uz .dau { font-size: 8.8pt; color: var(--g50); text-align: right; }
.uz--kern { position: relative; }
.uz--kern::before { content: ""; position: absolute; left: -4mm; top: 2mm;
                    bottom: 2mm; width: 1.6mm; background: var(--hl); }
.uz--kern .was { font-weight: 500; }
.summe { display: flex; justify-content: space-between; margin-top: 3.5mm;
         font-size: 8.8pt; color: var(--g50); }

/* ---- Die Bloecke ------------------------------------------------------ */
/* Einspaltig ueber die volle Breite: Bei 150 mm und 10,5 pt stehen rund
   75 Zeichen in der Zeile - die Breite, die sich am schnellsten liest. */
.block { display: grid; grid-template-columns: 20mm 1fr; gap: 6mm; }
/* Die Linie trennt zwei Bloecke, sie schliesst keinen ab. Deshalb traegt
   sie der folgende Block - :last-of-type greift hier nicht, weil die
   Fusszeile als weiteres div dazwischenzaehlt. */
.block + .block { border-top: .4pt solid var(--g25);
                  padding-top: 5mm; margin-top: 5mm; }
/* Die Minuten gross, die Uhrzeit mit Abstand darunter - ohne Striche. */
.zeitspur .min { font-family: var(--serif); font-weight: 700; font-size: 22pt;
                 line-height: 1; }
.zeitspur .min small { font-family: var(--sans); font-weight: 500;
                       font-size: 8.4pt; display: block; margin-top: 1mm;
                       letter-spacing: .04em; color: var(--g70); }
.zeitspur .uhr { display: block; margin-top: 5mm; font-size: 8.6pt;
                 color: var(--g50); line-height: 1.5; }
.bkopf { display: flex; align-items: baseline; gap: 3.5mm; margin-bottom: 3mm; }
.bkopf .nr { font-family: var(--serif); font-weight: 700; font-size: 10.5pt;
             color: var(--g50); }
.bkopf h3 { font-family: var(--serif); font-weight: 600; font-size: 14pt;
            line-height: 1.3; }


.aufmacher { font-size: 10.5pt; line-height: 1.58; color: var(--ink);
             margin-bottom: 3mm; }
.eng .aufmacher { font-size: 9.8pt; line-height: 1.55; margin-bottom: 2.6mm; }
.feld { margin-bottom: 3mm; }
.feld:last-child { margin-bottom: 0; }
.feld > dt { font-size: 7.6pt; font-weight: 600; letter-spacing: .12em;
             text-transform: uppercase; color: var(--g50); margin-bottom: 1.6mm; }
.feld p, .feld li { font-size: 10.5pt; line-height: 1.58; color: var(--g70); }
.feld ul { list-style: none; }
.feld li { position: relative; padding-left: 4.5mm; margin-bottom: 1.2mm; }
.feld li::before { content: ""; position: absolute; left: 0; top: 2.1mm;
                   width: 1.5mm; height: 1.5mm; background: var(--g50); }
.feld--fragen li::before { background: var(--ink); }
.feld--fragen li { font-style: italic; }
/* Die Kette traegt nur die Ziffer - ein gefuellter Kreis je Schritt macht
   die Seite unruhig, ohne mehr zu sagen. */
.kette { list-style: none; counter-reset: k; }
.kette li { position: relative; padding-left: 6mm; margin-bottom: 2.4mm;
            counter-increment: k; }
/* Die Ziffer muss die Punkt-Regel der Listen oben zuruecknehmen - sonst
   steht sie in einem 1,5-mm-Kaestchen und wird abgeschnitten. */
.kette li::before { content: counter(k) "."; position: absolute; left: 0; top: 0;
                    width: auto; height: auto; background: none;
                    font-family: var(--serif); font-weight: 700;
                    font-size: 10.5pt; line-height: 1.58; color: var(--g50); }
.kette li.reserve::before { color: var(--g25); }
.kette b { display: block; font-size: 10.5pt; color: var(--ink); }
/* Vier Rollen, vier Felder: Der graue Grund grenzt sie voneinander ab. */
.rollen { display: grid; grid-template-columns: 1fr 1fr; gap: 3mm; }
.rolle { background: var(--bg); border-radius: 2.5mm; padding: 3.5mm 4mm; }
.rolle b { display: block; font-size: 10pt; margin-bottom: 1mm; }
.rolle span { display: block; font-size: 9pt; line-height: 1.5; color: var(--g70); }

/* ---- Die kompakte Fassung zieht alles enger --------------------------- */
.eng { padding: 14mm 14mm 14mm; }
.eng .logo { top: 15.5mm; right: 14mm; height: 5mm; }
.eng .fuss { left: 14mm; right: 14mm; bottom: 9mm; }
.eng .block { grid-template-columns: 16mm 1fr; gap: 4.5mm; }
.eng .block + .block { padding-top: 5mm; margin-top: 5mm; }
.eng .zeitspur .min { font-size: 19pt; }
.eng .zeitspur .min small { font-size: 7.8pt; margin-top: .8mm; }
.eng .zeitspur .uhr { font-size: 8.2pt; margin-top: 4mm; line-height: 1.5; }
.eng .bkopf { margin-bottom: 3mm; gap: 3.2mm; }
.eng .bkopf h3 { font-size: 12.5pt; }
.eng .feld { margin-bottom: 2.6mm; }
.eng .feld > dt { font-size: 7.2pt; margin-bottom: 1.2mm; }
.eng .feld p, .eng .feld li { font-size: 9.2pt; line-height: 1.5; }
.eng .feld li { margin-bottom: .9mm; padding-left: 4.2mm; }
.eng .feld li::before { top: 1.9mm; width: 1.4mm; height: 1.4mm; }
.eng .kette li { padding-left: 4.4mm; margin-bottom: .9mm; }
.eng .kette li::before { font-size: 8pt; }
.eng .kette b { font-size: 8pt; }
.eng .rollen { gap: 2.4mm; }
.eng .rolle { padding: 2.8mm 3.2mm; border-radius: 2mm; }
.eng .rolle b { font-size: 9pt; margin-bottom: .6mm; }
.eng .rolle span { font-size: 8.2pt; line-height: 1.45; }
.eng h1 { font-size: 18pt; }
.eng .unterzeile { font-size: 9pt; margin-top: 3.5mm; }
.eng .ziel b { font-size: 9pt; }
.eng .ziel p { font-size: 8pt; line-height: 1.45; }
.eng .uz { padding: 1.8mm 0; }
.eng .uz .was { font-size: 8.6pt; }
.eng .uz .zeit { font-size: 8.2pt; }
.eng .uz .dau { font-size: 7.8pt; }
.eng .summe { font-size: 7.8pt; }
"""


def feld_html(f):
    art, inhalt, lab = f["art"], f["inhalt"], f["label"]
    kl = " feld--fragen" if lab.lower().startswith("leitfrage") else ""
    if art == "text":
        k = '<div class="warnung">' if False else ""
        return f'<div class="feld{kl}"><dt>{lab}</dt><p>{inhalt}</p></div>'
    if art == "warnung":
        return ""   # interne Arbeitsanweisung, nicht fuer den Ausdruck
    if art == "liste":
        li = "".join(f"<li>{x}</li>" for x in inhalt)
        return f'<div class="feld{kl}"><dt>{lab}</dt><ul>{li}</ul></div>'
    if art == "kette":
        li = "".join(
            f'<li class="reserve"><b>{t}</b>{r}</li>' if res
            else f"<li><b>{t}</b>{r}</li>" for t, r, res in inhalt)
        return f'<div class="feld"><dt>{lab}</dt><ol class="kette">{li}</ol></div>'
    if art == "rollen":
        r = "".join(f'<div class="rolle"><b>{b}</b><span>{s}</span></div>'
                    for b, s in inhalt)
        return f'<div class="feld"><dt>{lab}</dt><div class="rollen">{r}</div></div>'
    return ""


def block_html(b, teilnehmer=False):
    if teilnehmer:
        felder = (f'<p class="aufmacher">{TEILNEHMERSATZ[b["nr"]]}</p>'
                  + "".join(feld_html(f) for f in b["felder"]
                            if f["label"] not in OHNE_REGIE))
    else:
        felder = "".join(feld_html(f) for f in b["felder"])
    kern = " block--kern" if b["kern"] else ""
    return f'''<div class="block{kern}">
      <div class="zeitspur">
        <span class="min">{b["min"]}<small>Min</small></span>
        <span class="uhr">{b["von"]}<br>bis {b["bis"]}</span>
      </div>
      <div class="inhalt"><div class="bkopf"><span class="nr">{b["nr"]}</span>
        <h3>{b["titel"]}</h3></div>{felder}</div></div>'''


def uebersicht_html(bl):
    z = ['<div class="uebersicht">']
    for b in bl:
        k = " uz--kern" if b["kern"] else ""
        z.append(f'<div class="uz{k}"><span class="zeit">{b["von"]}–{b["bis"]}</span>'
                 f'<span class="nr">{b["nr"]}</span>'
                 f'<span class="was">{b["titel"]}</span>'
                 f'<span class="dau">{b["min"]} Min</span></div>')
    z.append('</div><div class="summe"><span>Fünf Blöcke</span>'
             f'<span>{sum(b["min"] for b in bl)} Minuten · '
             f'{bl[0]["von"]} bis {bl[-1]["bis"]} Uhr</span></div>')
    return "".join(z)


LOGO = '<img class="logo" src="assets/empiria-logo.svg" alt="empiria">'


def fuss(nr, von):
    return (f'<div class="fuss"><span>Workshop Vision &amp; Strategie · {DATUM}</span>'
            f'<span>Seite {nr} von {von}</span></div>')


def seite1(k, bl, eng):
    titelblock = f'''<h1>Workshop<br><span class="hl">Vision &amp; Strategie.</span></h1>
    <p class="unterzeile"><b>{DATUM}</b> · {bl[0]["von"]} bis {bl[-1]["bis"]} Uhr ·
      {sum(b["min"] for b in bl)} Minuten</p>'''
    ziele = "".join(f'<div class="ziel"><span class="nr">{n}</span>'
                    f"<b>{h}</b><p>{p}</p></div>" for n, h, p in k["ziele"])
    if eng:
        return (f'<div class="page eng">{LOGO}{titelblock}'
                f'<div style="height:7mm"></div>'
                f'<p class="tag">Ziel des Termins</p><div class="ziele">{ziele}</div>'
                f'<p class="tag">Der Ablauf</p>{uebersicht_html(bl)}')
    return (f'<div class="page">{LOGO}{titelblock}'
            f'<div style="height:11mm"></div>'
            f'<p class="tag">Ziel des Termins</p>'
            f'<h2>Gemeinsam vertreten wir die Vision und verwirklichen sie.</h2>'
            f'<div class="ziele">{ziele}</div>'
            f'<div class="zitat"><p>„{k["zitat"]}“</p><span>Wunschergebnis</span></div>'
            f'<div class="nichtziel"><span>Nicht Ziel des Termins</span>'
            f'<p>{k["nicht_ziel"]}</p></div>'
            f'<p class="tag">Der Ablauf</p>{uebersicht_html(bl)}')


def bauen(fassung):
    bl, k = bloecke(), kopf()
    eng = fassung == "kompakt"
    verteilung = VERTEILUNG[fassung]
    gesamt = len(verteilung) + (0 if eng else 1)
    seiten = []

    if eng:
        erste = seite1(k, bl, True) + '<div style="height:6mm"></div>'
        erste += "".join(block_html(b, True) for b in bl
                         if int(b["nr"]) in verteilung[0])
        seiten.append(erste + fuss(1, gesamt) + "</div>")
        rest = verteilung[1:]
    else:
        seiten.append(seite1(k, bl, False) + fuss(1, gesamt) + "</div>")
        rest = verteilung

    for i, gruppe in enumerate(rest, start=2):
        kl = "page eng" if eng else "page"
        inhalt = "".join(block_html(b, eng) for b in bl if int(b["nr"]) in gruppe)
        # Abstand unter dem Logo, damit der erste Block nicht daran klebt
        # Das Logo reicht bis rund 20 mm unter die Oberkante. Mit nur
        # wenigen Millimetern darunter steht die erste Ueberschrift auf
        # seiner Hoehe und wirkt gedraengt.
        luft = "14mm" if eng else "6mm"
        seiten.append(f'<div class="{kl}">{LOGO}<div style="height:{luft}"></div>'
                      f'{inhalt}{fuss(i, gesamt)}</div>')

    titel = f"Agenda {DATUM} – Workshop Vision und Strategie"
    return (f'<!doctype html><html lang="de"><head><meta charset="utf-8">'
            f"<title>{titel}</title>"
            f'<link rel="stylesheet" href="assets/fonts/fonts.local.css">'
            f"<style>{CSS}</style></head><body>{''.join(seiten)}</body></html>")


def main():
    os.chdir(ROOT)
    BUILD.mkdir(exist_ok=True)
    link = BUILD / "assets"
    if not link.exists():
        link.symlink_to(SITE / "assets")
    ziel = pathlib.Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 \
        else pathlib.Path.home() / "Downloads"
    ziel.mkdir(parents=True, exist_ok=True)

    for fassung, name in (("moderation", "Agenda-Vision-Strategie-Moderation"),
                          ("kompakt", "Agenda-Vision-Strategie-Kompakt")):
        src = BUILD / f"_src_{fassung}.html"
        src.write_text(bauen(fassung), encoding="utf-8")
        pdf = ziel / f"{name}.pdf"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu",
                        "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                        "--virtual-time-budget=8000", "file://" + str(src)],
                       capture_output=True, timeout=180)
        if not pdf.exists():
            raise SystemExit(f"Rendern fehlgeschlagen: {fassung}")
        print(f"{name}.pdf  ({pdf.stat().st_size // 1024} KB)  ->  {ziel}")

        # Die kompakte Fassung haengt auch in der Terminuebersicht der
        # Projektplanung - dorthin samt Vorschaubild der ersten Seite.
        if fassung == "kompakt":
            web = SITE / "assets" / "projekte"
            shutil.copy(pdf, web / "sv-agenda-vision-strategie.pdf")
            vorlage = EMPIRIA / "werkzeuge" / "pdf-vorlage"
            if not vorlage.is_dir():
                raise SystemExit(f"PDF-Werkzeug von empiria fehlt: {vorlage}")
            sys.path.insert(0, str(vorlage))
            from vorschaubilder import screenshot_pages, png_to_webp
            with tempfile.TemporaryDirectory() as td:
                shots = screenshot_pages(str(src), [1], td)
                png_to_webp(shots[1],
                            str(web / "sv-agenda-vision-strategie-vorschau.webp"))
            print(f"{'':<4}-> entwicklung-empiria/assets/projekte/sv-agenda-vision-strategie.pdf + Vorschau")


if __name__ == "__main__":
    main()
