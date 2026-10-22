#!/usr/bin/env python3
"""Druckfassungen der Projektseiten - je Seite ein sauber gefuelltes Blatt.

Die Seiten sind fuer den Bildschirm gebaut: Kopfleiste, Fusszeile,
Entwicklungsmenue, aufklappbare Kaesten. Fuer den Druck faellt die Huelle
weg, die Kaesten stehen im gewuenschten Zustand, und der Inhalt wird auf
das Blatt skaliert.

Zwei Dinge, die beim Bauen Zeit gekostet haben und hier festgehalten sind:

  * Die Seite laeuft in einem Rahmen fester Breite, der skaliert wird.
    Ein zoom auf html verschiebt die Breakpoints mit - die Seite faellt
    dann in ihr schmales Layout, obwohl das Blatt breit genug waere.
  * Wie viele Blattseiten herauskommen, laesst sich nicht zuverlaessig
    vorhersagen. Deshalb wird gerendert, nachgezaehlt und bei Bedarf
    enger gestellt, bis es passt.

Aufruf:  python3 _projektquelle/werkzeuge/pdf-projekt/seiten_drucken.py [name ...]
         DRUCK_ZIEL=<ordner> setzt das Ausgabeverzeichnis.
"""
import contextlib, functools, http.server, json, os, pathlib, re
import socketserver, subprocess, sys, threading

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent          # SV-Repo (umgezogen aus empiria, 22.10.2026)
SITE = ROOT / "entwicklung-empiria"       # gebaute Projektseiten
BUILD = SITE / "_druck_tmp"               # muss unter SITE liegen
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PX_JE_MM = 96 / 25.4
BREITE_STD = 1240                          # Desktop-Breite wie am Schreibtisch

BLATT = {"A4": (210, 297), "A3": (297, 420), "A2": (420, 594),
         "A1": (594, 841)}


def masse(blatt, quer, rand):
    b, h = BLATT[blatt]
    if quer:
        b, h = h, b
    return b, h, (b - 2 * rand) * PX_JE_MM, (h - 2 * rand) * PX_JE_MM


# --- Was im Rahmen passieren soll, bevor gemessen und gedruckt wird -------
AKKORDEON = """
var will = %s;
d.querySelectorAll('.fl-ebene').forEach(function (e) {
  var nr = ((e.querySelector('.fl-kopf-nr') || {}).textContent || '').trim();
  var auf = will.indexOf(nr) > -1;
  e.classList.toggle('is-offen', auf);
  var k = e.querySelector('.fl-kopf');
  if (k) k.setAttribute('aria-expanded', auf ? 'true' : 'false');
});
"""

NUR_WERKZEUG = AKKORDEON % '["03"]' + """
d.querySelectorAll('.fl-ebene').forEach(function (e) {
  var nr = ((e.querySelector('.fl-kopf-nr') || {}).textContent || '').trim();
  if (nr !== '03') e.remove();
});
var kz = d.querySelector('.fl-kopf-zeile');
if (kz) kz.remove();
// Die Abstaende der Seite weg: Der Kasten soll das Blatt fuellen.
d.querySelectorAll('.section, .container, main').forEach(function (e) {
  e.style.padding = '0'; e.style.margin = '0'; e.style.maxWidth = 'none';
});
var e = d.querySelector('.fl-ebene');
if (e) { e.style.border = '0'; e.style.borderRadius = '0'; }
"""

WERKZEUG_OFFEN = AKKORDEON % '["03"]' + """
d.querySelectorAll('.fl-ebene').forEach(function (e) {
  var nr = ((e.querySelector('.fl-kopf-nr') || {}).textContent || '').trim();
  if (nr !== '03') e.remove();
});
var kz = d.querySelector('.fl-kopf-zeile');
if (kz) kz.remove();
d.querySelectorAll('.section, .container, main').forEach(function (e) {
  e.style.paddingTop = '0'; e.style.marginTop = '0';
});
"""

NUR_PROTOKOLL = """
// Nur das Protokoll - der Rest der Seite bleibt auf dem Bildschirm.
var pr = d.querySelector('#protokoll');
d.querySelectorAll('main > *, body > main ~ *').forEach(function (e) {
  if (e !== pr && !e.contains(pr)) e.remove();
});
d.querySelectorAll('main section').forEach(function (e) {
  if (e !== pr) e.remove();
});
// Die Abstaende der Seite weg, damit der Abschnitt das Blatt fuellt.
d.querySelectorAll('.section, .container, main').forEach(function (e) {
  e.style.paddingTop = '0'; e.style.paddingBottom = '0';
  e.style.marginTop = '0'; e.style.marginBottom = '0';
});
"""

STRAHL_AUF = """
// Der Zeitstrahl liegt in einem waagerecht scrollenden Streifen.
d.querySelectorAll('[class*="__scroll"]').forEach(function (e) {
  e.style.overflow = 'visible';
  e.style.width = 'max-content';
});
// Den Umschalter samt seinem Kasten entfernen - sonst bleibt ein leerer
// Rahmen mit der Aufschrift "Darstellung" stehen.
var u = d.querySelector('.mk__ansichten');
if (u) { var k = u.closest('.mk__box') || u.parentElement; (k || u).remove(); }
"""

AUFTRAEGE = {
    "projektmodule": dict(
        seite="sv-akademie", blatt="A3", quer=False, rand=10, breite=1040,
        zustand="", zustaende=[AKKORDEON % '["02"]', WERKZEUG_OFFEN],
        seiten=2,
        datei="SV-Akademie-Projektmodule-A3",
        titel="SV Akademie – Projektmodule"),
    "werkzeugkasten": dict(
        seite="sv-akademie", blatt="A3", quer=True, rand=10, breite=980,
        zustand=NUR_WERKZEUG,
        datei="SV-Akademie-Werkzeugkasten-A3-quer",
        titel="SV Akademie – Werkzeugkasten"),
    "selbstverstaendnis": dict(
        seite="sv-selbstverstaendnis", blatt="A3", quer=False, rand=14,
        breite=900, zustand="",
        datei="SV-Akademie-Selbstverstaendnis-A3",
        titel="SV Akademie – Selbstverständnis"),
    "protokoll": dict(
        seite="sv-selbstverstaendnis", blatt="A3", quer=False, rand=12,
        breite=1240, zustand=NUR_PROTOKOLL,
        datei="SV-Akademie-Weg-zum-Leitbild-A3",
        titel="SV Akademie – Der Weg zum Leitbild"),
    "projektplanung": dict(
        seite="sv-projektplanung", blatt="A3", quer=False, rand=14,
        breite=900, zustand="",
        datei="SV-Akademie-Projektplanung-A3",
        titel="SV Akademie – Projektplanung und Termine"),
    "meilensteine-fein": dict(
        seite="sv-meilensteine-fein", blatt="A1", quer=True, rand=15,
        breite=3750, zustand=STRAHL_AUF,
        datei="SV-Akademie-Meilensteine-fein-A1-quer",
        titel="SV Akademie – Meilensteine (fein)"),
    "meilensteine-hell": dict(
        seite="sv-meilensteine", blatt="A1", quer=True, rand=15,
        breite=5200, zustand=STRAHL_AUF,
        datei="SV-Akademie-Meilensteine-hell-A1-quer",
        titel="SV Akademie – Meilensteine (hell)"),
}

# Dieses CSS wird in den Rahmen injiziert.
INNEN_CSS = """
html, body { margin: 0 !important; padding: 0 !important;
             background: #fff !important; }
/* Ohne das misst man mitten in der Aufklapp-Animation. */
*, *::before, *::after { transition: none !important; animation: none !important; }
/* Die Seite zieht ihren Koerper auf Fensterhoehe, damit die Fusszeile
   unten klebt - auf dem Blatt erzeugt das eine leere zweite Seite. */
html, body, main, .vt-falt, .k, .me, .me__buehne
  { min-height: 0 !important; height: auto !important; }
/* Die Huelle gehoert auf den Bildschirm, nicht auf das Blatt. */
header.site-header, footer.site-footer, .dev-dd, .dev-band,
.k-bar { display: none !important; }
/* Der Umschalter fein/dunkel/hell ist Bildschirmbedienung - der Kopf mit
   Titel und Legende bleibt. me__quer ist eine Verbindungslinie im
   Diagramm, kein Bedienelement. */
.mk__ansichten, .mk__darstellung { display: none !important; }
/* Popups liegen auf dem Bildschirm ueber der Seite und sind zu; im Druck
   stehen sie im Fluss und machen die Seite ein Vielfaches hoeher. */
.modal-overlay, .dbx-pop, .k-pop, [role="dialog"] { display: none !important; }
/* Der graue Grund kostet im Druck nur Farbe. Dafuer bekommen die weissen
   Kaesten eine Kante, damit sie nicht im Papier verschwinden. */
.vt-falt--grau, main, .section { background: #fff !important; }
.fl-ebene { border: .8pt solid #d8d4cf !important; box-shadow: none !important; }
/* Der Lesecontainer darf die ganze Blattbreite nutzen. */
.container { max-width: none !important; padding-left: 8px !important;
             padding-right: 8px !important; }
"""


def quelle(a, zoom=1.0, hoehe=None):
    """Druckquelle: je Zustand ein Blatt, jedes in einem Rahmen fester Breite.

    Ein zoom auf html wuerde die Breakpoints mitverschieben - die Seite
    faellt dann in ihr schmales Layout, obwohl das Blatt breit genug
    waere. Im Rahmen behaelt sie den Viewport vom Schreibtisch.

    Mehrere Blaetter brauchen mehrere Rahmen: Ein iframe bricht nicht
    ueber eine Seitengrenze um.
    """
    bmm, hmm, bpx, hpx = masse(a["blatt"], a["quer"], a["rand"])
    rb = a["breite"]
    zustaende = a.get("zustaende") or [a["zustand"]]
    h = hoehe or round(hpx / zoom)
    rahmen, skripte = [], []
    for i, z in enumerate(zustaende):
        rahmen.append(f'<div class="blatt"><div class="rahmen">'
                      f'<iframe id="s{i}" src="/projekte/{a["seite"]}.html">'
                      f'</iframe></div></div>')
        skripte.append(f"""
document.getElementById('s{i}').addEventListener('load', function () {{
  var d = this.contentDocument;
  var st = d.createElement('style');
  st.textContent = {json.dumps(INNEN_CSS)};
  d.head.appendChild(st);
  {z}
  fertig({i}, d);
}});""")
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<title>{a['titel']}</title><style>
@page {{ size: {bmm}mm {hmm}mm; margin: {a['rand']}mm; }}
html, body {{ margin: 0; padding: 0; background: #fff; }}
.blatt {{ display: flex; align-items: center; justify-content: center;
          width: {round(bpx)}px; height: {round(hpx)}px; }}
.blatt + .blatt {{ break-before: page; page-break-before: always; }}
.rahmen {{ width: {round(rb * zoom)}px; height: {round(h * zoom)}px;
           overflow: hidden; flex: none; }}
iframe {{ width: {rb}px; height: {h}px; border: 0; display: block;
          transform: scale({zoom:.4f}); transform-origin: top left; }}
</style></head><body>
{"".join(rahmen)}
<script>
var masse = {{}}, offen = {len(zustaende)};
function fertig(i, d) {{
  setTimeout(function () {{
    var unten = 0, breit = 0;
    d.querySelectorAll('body *').forEach(function (e) {{
      var b = e.getBoundingClientRect();
      if (b.height > 0) {{
        unten = Math.max(unten, b.bottom);
        breit = Math.max(breit, b.right);
      }}
    }});
    masse[i] = [Math.ceil(breit), Math.ceil(unten)];
    if (Object.keys(masse).length === offen) {{
      var mb = 0, mh = 0;
      for (var k in masse) {{ mb = Math.max(mb, masse[k][0]);
                              mh = Math.max(mh, masse[k][1]); }}
      document.title = 'MASS|' + mb + '|' + mh;
    }}
  }}, 800);
}}
{"".join(skripte)}
</script></body></html>"""


@contextlib.contextmanager
def server():
    class Still(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    handler = functools.partial(Still, directory=str(SITE))
    socketserver.TCPServer.allow_reuse_address = True
    srv = socketserver.TCPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    try:
        yield f"http://127.0.0.1:{srv.server_address[1]}"
    finally:
        srv.shutdown()
        srv.server_close()


def messen(a, basis):
    """Inhaltsmasse im Rahmen - ungeskaliert, in der Renderbreite."""
    tmp = BUILD / f"_mess_{a['seite']}.html"
    tmp.write_text(quelle(a, 1.0, 2400), encoding="utf-8")
    r = subprocess.run(
        [CHROME, "--headless=new", "--disable-gpu",
         f"--window-size={a['breite'] + 40},1200",
         "--virtual-time-budget=6000", "--dump-dom",
         f"{basis}/_druck_tmp/{tmp.name}"],
        capture_output=True, text=True, timeout=180).stdout
    tmp.unlink()
    m = re.search(r"<title>MASS\|(\d+)\|(\d+)</title>", r)
    if not m:
        raise SystemExit(f"Messung fehlgeschlagen: {a['seite']}")
    return int(m.group(1)), int(m.group(2))


def seitenzahl(pdf):
    return max(int(x) for x in re.findall(rb"/Count (\d+)", pdf.read_bytes()))


def main(namen):
    BUILD.mkdir(exist_ok=True)
    ziel = pathlib.Path(os.environ.get(
        "DRUCK_ZIEL", pathlib.Path.home() / "Downloads" / "SV-Akademie-Druck"))
    ziel.mkdir(parents=True, exist_ok=True)

    with server() as basis:
        for name in namen:
            a = AUFTRAEGE[name]
            bmm, hmm, bpx, hpx = masse(a["blatt"], a["quer"], a["rand"])
            breite, hoehe = messen(a, basis)
            # Breite und Hoehe muessen auf das Blatt - der kleinere
            # Massstab gewinnt.
            zoom = min(bpx / max(breite, a["breite"]), hpx / hoehe)
            src = BUILD / f"_druck_{name}.html"
            pdf = ziel / f"{a['datei']}.pdf"
            for _ in range(10):
                src.write_text(quelle(a, zoom, hoehe), encoding="utf-8")
                subprocess.run(
                    [CHROME, "--headless=new", "--disable-gpu",
                     "--no-pdf-header-footer", f"--print-to-pdf={pdf}",
                     "--virtual-time-budget=8000",
                     f"{basis}/_druck_tmp/{src.name}"],
                    capture_output=True, timeout=240)
                if not pdf.exists():
                    raise SystemExit(f"Rendern fehlgeschlagen: {name}")
                if seitenzahl(pdf) <= a.get("seiten", 1):
                    break
                zoom *= 0.96
            print(f"{name:20s} {a['blatt']}{'quer' if a['quer'] else 'hoch':>5s}"
                  f"  Inhalt {breite}x{hoehe}  Zoom {zoom:.2f}"
                  f"  {seitenzahl(pdf)} Seite(n)"
                  f"  fuellt {min(100, round(hoehe * zoom / hpx * 100)):>3}%"
                  f"  -> {a['datei']}.pdf")
    print(f"\nAlles in: {ziel}")


if __name__ == "__main__":
    main(sys.argv[1:] or list(AUFTRAEGE))
