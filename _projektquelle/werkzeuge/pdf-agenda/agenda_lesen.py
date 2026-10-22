#!/usr/bin/env python3
"""Liest die Agenda aus der Website - damit nichts doppelt gepflegt wird.

Quelle ist _projektquelle/entwicklung-empiria-quelle/projekte/sv-abstimmung-hal.html
(SV-Repo, Branch daniel). Aendert sich dort ein
Leitfrage, aendert sie sich beim naechsten Lauf auch im PDF.

Die Felder eines Blocks treten in fuenf Formen auf; der Parser gibt sie
als neutrale Struktur zurueck, damit die Layouts sie frei setzen koennen:

    text      ein Absatz
    warnung   ein Absatz, der im Druck markiert wird
    liste     Aufzaehlung (ab-liste, ab-fragen)
    kette     nummerierte Schritte mit Titel und Erklaerung
    rollen    Begriffspaare mit Erklaerung
"""
import html as _html, pathlib, re

QUELLE = pathlib.Path("_projektquelle/entwicklung-empiria-quelle/projekte/sv-abstimmung-hal.html")
BEGINN = (14, 30)          # Uhrzeit des Termins - nur im PDF, nicht auf der Seite


def rein(s):
    """HTML raus, Entities aufloesen, Leerraum normalisieren."""
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", _html.unescape(s)).replace("\xa0", " ").strip()


def _dd_lesen(dd, klasse):
    if "ab-warnung" in klasse:
        return ("warnung", rein(dd))
    if "<div class=\"ab-rollen\"" in dd:
        rollen = []
        for r in re.findall(r'<div class="ab-rolle[^"]*">(.*?)</div>', dd, re.S):
            b = re.search(r"<b>(.*?)</b>", r, re.S)
            s = re.search(r"<small>(.*?)</small>", r, re.S)
            rollen.append((rein(b.group(1)) if b else "",
                           rein(s.group(1)) if s else ""))
        return ("rollen", rollen)
    if "<ol" in dd:
        glieder = []
        for li in re.findall(r"<li([^>]*)>(.*?)</li>", dd, re.S):
            b = re.search(r"<b>(.*?)</b>", li[1], re.S)
            titel = rein(b.group(1)) if b else ""
            rest = rein(re.sub(r"(?s)<b>.*?</b>", "", li[1]))
            glieder.append((titel, rest, "ist-reserve" in li[0]))
        return ("kette", glieder)
    if "<ul" in dd:
        return ("liste", [rein(x) for x in re.findall(r"<li>(.*?)</li>", dd, re.S)])
    return ("text", rein(dd))


def bloecke():
    t = QUELLE.read_text(encoding="utf-8")
    i = t.index('<div class="ab-ablauf">')
    j = t.index("</main>", i)
    raus, uhr = [], BEGINN[0] * 60 + BEGINN[1]
    for b in re.split(r'<div class="ab-block', t[i:j])[1:]:
        m = re.search(r'<span class="ab-nr">(\d+)</span>', b)
        if not m:
            continue
        dauer = int(re.search(r"--min:(\d+)", b).group(1))
        felder = []
        for kl, dt, ddkl, dd in re.findall(
                r'<div class="ab-feld([^"]*)">\s*<dt>(.*?)</dt>\s*'
                r'<dd([^>]*)>(.*?)</dd>', b, re.S):
            art, inhalt = _dd_lesen(dd, ddkl)
            felder.append({"label": rein(dt), "art": art, "inhalt": inhalt})
        raus.append({
            "nr": m.group(1),
            "titel": rein(re.search(r'ab-marke-titel">(.*?)</span>', b, re.S).group(1)),
            "min": dauer,
            "von": f"{uhr // 60}:{uhr % 60:02d}",
            "bis": f"{(uhr + dauer) // 60}:{(uhr + dauer) % 60:02d}",
            "kern": "ab-block--kern" in b[:80],
            "felder": felder,
        })
        uhr += dauer
    return raus


def kopf():
    t = QUELLE.read_text(encoding="utf-8")
    ziele = [(rein(n), rein(h), rein(p)) for n, h, p in re.findall(
        r'<span class="ab-ziel-nr">(.*?)</span>\s*<h3>(.*?)</h3>\s*<p>(.*?)</p>',
        t, re.S)]
    zitat = rein(re.search(r"<blockquote>(.*?)</blockquote>", t, re.S).group(1))
    nicht = rein(re.search(r'<div class="ab-abgrenzung">.*?<p>(.*?)</p>', t, re.S).group(1))
    return {"ziele": ziele, "zitat": zitat, "nicht_ziel": nicht}


if __name__ == "__main__":
    bl = bloecke()
    print(f"{len(bl)} Bloecke, {sum(b['min'] for b in bl)} Minuten, "
          f"{bl[0]['von']} bis {bl[-1]['bis']} Uhr")
    for b in bl:
        arten = ", ".join(f"{f['label']}:{f['art']}" for f in b["felder"])
        print(f"  {b['nr']} {b['von']}-{b['bis']} ({b['min']:>2} Min) "
              f"{b['titel'][:42]:<44} {arten}")
    k = kopf()
    print(f"\nZiele: {len(k['ziele'])} | Zitat {len(k['zitat'])} Z. | "
          f"Nicht-Ziel {len(k['nicht_ziel'])} Z.")
