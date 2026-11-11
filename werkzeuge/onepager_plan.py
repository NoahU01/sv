#!/usr/bin/env python3
"""Projektplanung SV Akademie – zwei Blätter A3 quer im Corporate Design der SV (Daniel, 11.11.2026).
Muster: SV Schadenmanagement (Repo sv-schadenmanagement, werkzeuge/onepager_vorstand.py + onepager_sv.py):
roter Kopfbalken, Überschrift weiß links, SV-Logo weiß rechts; eine Inhaltsfläche mit dem Plan und den Markierungen 1 2 3.

  Blatt 1  Gesamtplan bis Ende 2028: 1 das Ziel (Level 5) · 2 der Weg über fünf Ergebnisstufen ·
           3 hervorgehoben Level 2 „Das Fundament steht“
  Blatt 2  Was jetzt vor uns liegt (bis Level 1, 19.01.2027): 1 heute – die Strategie wird konkretisiert ·
           2 bis 15.01.2027 LEA und Webseite · 3 am 19.01.2027 LEA go-live JAT

Quelle: empiria-Dashboard (Projekt 1). Gezeigt werden nur die drei Stoßrichtungen unter „Vision & Strategie umsetzen“,
die Linie Projektmanagement bleibt draußen. Schriftsystem wie beim Schadenmanagement: Sparkasse Head für Überschrift,
Nummern und Aussagen-Titel; Sparkasse Text (Lt/Rg) für alles Übrige; Farben Schwarz, SV-Grau, SV-Rot nur für Balken
und Nummern, die drei Stoßrichtungen in den SV-Akzentfarben.

Die Schriften sind lizenziert (exclusive use by DSGV): Sie werden eingebettet, die HTML-Datei entsteht deshalb nur
temporär außerhalb des Repos.
Aufruf:  python3 werkzeuge/onepager_plan.py [ziel.pdf]
"""
import base64, datetime as dt, html, re, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, str(Path.home() / "AlwaysOn/supabase"))
import sql  # noqa: E402
import fitz  # noqa: E402

HIER = Path(__file__).resolve().parent
P = 1
HEUTE = dt.date(2026, 11, 16)          # Abteilungsbesprechung – an diesem Tag wird das Blatt gezeigt
SCHRIFTEN = Path.home() / "nextcloud_EMP/empiria GmbH - Intern/Webseiten/Web_AVRG/entwicklung/schriften"
LOGO = (HIER / "sv-logo.svg").read_text()
ROT, SCHWARZ, TEXT, GRAU1, GRAU2, GRAU3, LINIE, RASTER = "#EE0000", "#000000", "#444444", "#666666", "#999999", "#999999", "#E3E3E3", "#E9E9E9"
FARBEN = ["#9B348E", "#2C57D2", "#00ACD3"]   # Reihenfolge der Stoßrichtungen wie im Dashboard (SV-Akzentfarben)
FW, FH = 376, 214                       # Inhaltsfläche in mm (A3 quer abzüglich Rand, Kopf, Fuß)
ZIEL = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / (
    "nextcloud_EMP/empiria GmbH - Intern/claude/Ausarbeitungen/01 Projekte/empiria – SV Akademie/"
    f"{dt.date.today():%Y-%m-%d} SV Akademie Projektplanung (A3 quer) – SV.pdf")


def e(t):
    return html.escape(str(t or ""))


def d(s):
    return dt.date.fromisoformat(str(s)[:10]) if s else None


straenge = sql.ausfuehren(f"select id, titel, eltern_id, reihenfolge from projekt_straenge where projekt_id={P} order by reihenfolge")
pakete = sql.ausfuehren(f"select id, titel, strang_id, beginnt_am, faellig_am, vorgaenger, projektgate_id, status from projekt_pakete where projekt_id={P}")
gates = sql.ausfuehren(f"select id, titel, faellig_am, beschreibung from aufgaben where projekt_id={P} and art='projektgate' order by faellig_am")
gruppe = next(s for s in straenge if s["eltern_id"] is None and "vision" in s["titel"].lower())
oben = sorted([s for s in straenge if s["eltern_id"] == gruppe["id"]], key=lambda s: s["reihenfolge"])   # die drei Stoßrichtungen
for i, s in enumerate(oben):
    s["_farbe"] = FARBEN[i % len(FARBEN)]


def name(s):
    return s["titel"].split(" ", 1)[1] if s["titel"][:2].isdigit() else s["titel"]


def kurz(s):
    """wie ubKurz im Dashboard: Digitalisierung → DI, USP Mensch → UM, Sichtbarkeit & Außenwirkung → SA"""
    w = [x for x in re.sub(r"&|\bund\b", " ", name(s)).split() if x]
    return (w[0][0] + w[1][0]).upper() if len(w) > 1 else w[0][:2].upper()


def kinder(sid):
    """Linien einer Stoßrichtung: ihre Stränge – oder sie selbst, wenn die Pakete direkt an ihr hängen."""
    k = sorted([s for s in straenge if s["eltern_id"] == sid], key=lambda s: s["reihenfolge"])
    return k or [next(s for s in straenge if s["id"] == sid)]


def eltern(p):
    k = next(s for s in straenge if s["id"] == p["strang_id"])
    return next((s for s in oben if s["id"] in (k["eltern_id"], k["id"])), None)


def zustand(p):
    """Zustand am Tag HEUTE: vorbei = fertig, begonnen = läuft, sonst offen. Halte ohne Beginn: am Tag selbst läuft er."""
    a, b = d(p["beginnt_am"]), d(p["faellig_am"])
    if p["status"] == "fertig" or (b and b < HEUTE):
        return "fertig"
    if not a:
        return "läuft" if b == HEUTE else "offen"
    return "läuft" if a <= HEUTE else "offen"


# ---------- SVG-Bausteine (Einheit mm) ----------
def pill(x1, x2, y, h, stroke=GRAU2, sw=0.45, fill="#fff"):
    w = max(x2 - x1, h)
    return f'<rect x="{x1:.2f}" y="{y - h / 2:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{h / 2:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def halt(x, y, r, stroke, sw, fill="#fff"):
    return f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def balken(x, y1, y2, w=4.2, sw=1.0):
    return f'<rect x="{x - w / 2:.2f}" y="{y1:.2f}" width="{w}" height="{y2 - y1:.2f}" rx="{w / 2}" fill="#fff" stroke="{SCHWARZ}" stroke-width="{sw}"/>'


def text(x, y, t, cls="", anchor="start"):
    return f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}" text-anchor="{anchor}">{e(t)}</text>'


def stossrichtung(x, y, s, zweizeilig=False):
    o = f'<rect x="{x:.2f}" y="{y - 2.4:.2f}" width="5.8" height="4.8" rx="1.1" fill="{s["_farbe"]}"/>' + text(x + 2.9, y + 1, kurz(s), "badge", "middle")
    teile = name(s).split(" & ")
    if zweizeilig and len(teile) > 1:
        return o + text(x + 8, y + 1, teile[0] + " &", "sname") + text(x + 8, y + 5, teile[1], "sname")
    return o + text(x + 8, y + 1, name(s), "sname")


def nummer(x, y, n, r=3.6):
    return (f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r}" fill="{ROT}"/>'
            f'<text x="{x:.2f}" y="{y + 1.55:.2f}" class="nr" text-anchor="middle">{n}</text>')


def leitlinie(punkte):
    pfad = "M" + " L".join(f"{a:.2f} {b:.2f}" for a, b in punkte)
    a, b = punkte[-1]
    return (f'<path d="{pfad}" fill="none" stroke="{SCHWARZ}" stroke-width="0.35"/>'
            f'<circle cx="{a:.2f}" cy="{b:.2f}" r="1" fill="{SCHWARZ}"/>')


def notiz(x, y, w, n, titel, inhalt):
    """Nummer + kurze Aussage, die Nummer sitzt links am Titel."""
    return (nummer(x + 3.6, y + 3.4, n) +
            f'<foreignObject x="{x + 10:.2f}" y="{y:.2f}" width="{w - 10:.2f}" height="140">'
            f'<div xmlns="http://www.w3.org/1999/xhtml" class="no"><p class="no-t">{titel}</p>{inhalt}</div></foreignObject>')


def absaetze(t):
    """Zeilen mit „•“ werden zur Liste, übrige zu Absätzen – wie im Fenster des Dashboards."""
    h, liste = "", []
    for z in [z.strip() for z in str(t or "").split("\n") if z.strip()]:
        if z[0] in "•-–":
            liste.append(z.lstrip("•-– ").strip()); continue
        if liste:
            h += '<ul class="no-l">' + "".join(f"<li>{e(x)}</li>" for x in liste) + "</ul>"; liste = []
        h += f'<p class="no-b">{e(z)}</p>'
    if liste:
        h += '<ul class="no-l">' + "".join(f"<li>{e(x)}</li>" for x in liste) + "</ul>"
    return h


def umbruch(t, n):
    zeilen, z = [], ""
    for w_ in t.split():
        if len(z) + len(w_) + 1 > n and z:
            zeilen.append(z); z = w_
        else:
            z = (z + " " + w_).strip()
    return zeilen + [z]


# ---------- Blatt 1: Gesamtplan ----------
def plan_gesamt():
    """Gesamtplan September 2026 bis Ende 2028. Die Zeitachse ist je Level gleichmäßig, die ersten beiden Level
    (mit den meisten Paketen) bekommen mehr Breite – wie im Dashboard, wo Monate mit vielen Halten breiter sind."""
    LINKS, PW = 46, 262
    a0 = d("2026-09-01")
    grenzen = [a0] + [d(g["faellig_am"]) for g in gates]
    anteile = [0.27, 0.33] + [0.40 / (len(gates) - 2)] * (len(gates) - 2)

    def x(t):
        t = min(max(t, grenzen[0]), grenzen[-1])
        pos = 0.0
        for i in range(len(gates)):
            g0, g1 = grenzen[i], grenzen[i + 1]
            if t <= g1:
                return LINKS + PW * (pos + anteile[i] * (t - g0).days / max((g1 - g0).days, 1))
            pos += anteile[i]
        return LINKS + PW

    # Level-Titel oben auf gleicher Höhe (Gleiches auf gleicher Höhe), die Balken beginnen unter dem längsten Titel
    TITEL = {g["id"]: umbruch(g["titel"], 17) for g in gates}
    BALKEN = 15.4 + (max(len(z) for z in TITEL.values()) - 1) * 3.6 + 4
    lanes, y = [], BALKEN + 8
    for s in oben:
        s["_y"] = y
        for k in kinder(s["id"]):
            lanes.append((s, k, y)); y += 13
        y += 13
    H = y
    W = LINKS + PW + 6
    o = []
    for s in oben:
        o.append(stossrichtung(0, s["_y"], s, zweizeilig=True))
    for s, k, ly in lanes:
        o.append(f'<line x1="{LINKS - 2}" y1="{ly:.2f}" x2="{W - 3:.2f}" y2="{ly:.2f}" stroke="{LINIE}" stroke-width="1.3" stroke-linecap="round"/>')
    lane_y = {k["id"]: ly for s, k, ly in lanes}
    for p in pakete:
        ly = lane_y.get(p["strang_id"])
        if ly is None:
            continue
        a, b = d(p["beginnt_am"]), d(p["faellig_am"])
        z = zustand(p)
        if a and b:
            o.append(pill(x(a), x(b), ly, 2.4, SCHWARZ if z == "läuft" else GRAU2, 0.7 if z == "läuft" else 0.45, LINIE if z == "fertig" else "#fff"))
        elif b:
            o.append(halt(x(b), ly, 1.25, SCHWARZ if z == "läuft" else GRAU2, 0.7 if z == "läuft" else 0.45, LINIE if z == "fertig" else "#fff"))
    xbs = []
    for i, gg in enumerate(gates):
        xb = x(d(gg["faellig_am"])) + (0 if i < len(gates) - 1 else 3)
        xbs.append(xb)
        letzt = i == len(gates) - 1
        o.append(balken(xb, BALKEN, H - 4, 5.2 if letzt else 4.2, 1.5 if letzt else 1.0))
        o.append(text(xb, 10, f"Level {i + 1} · {d(gg['faellig_am']).strftime('%d.%m.%Y')}", "lvl", "middle"))
        for j, zl in enumerate(TITEL[gg["id"]]):
            o.append(text(xb, 15.4 + j * 3.6, zl, "mtit", "middle"))
    return "".join(o), W, H, {"bars": xbs, "oben": 6}


def blatt1():
    plan, W, H, a = plan_gesamt()
    s = 0.85
    oben_ = 6                                 # die drei Aussagen auf gleicher Höhe
    oy = oben_ + 68 - a["oben"] * s           # Plan mit deutlichem Abstand unter den drei Aussagen
    teile = [f'<g transform="translate(0 {oy:.2f}) scale({s})">{plan}</g>']
    xb = [v * s for v in a["bars"]]           # Level 1 bis 5
    x1 = xb[-1] + 30                          # das Ziel: rechts hinter dem Ende des Plans
    ny = oben_ + 3.4
    oberkante = oy + a["oben"] * s
    teile.append(leitlinie([(xb[0], ny + 3.6), (xb[0], oberkante)]))
    teile.append(leitlinie([(xb[2], ny + 3.6), (xb[2], oberkante)]))   # 3 steht auf Level 3 (Daniel, 11.11.2026)
    ym = oy + (oben[0]["_y"] + 13) * s        # 1: an der Nummer herunter, dann zum Ziel-Balken
    teile.append(leitlinie([(x1, ny + 3.6), (x1, ym), (xb[-1] + 2.6, ym)]))
    g1, g2, g3, g4, g5 = gates
    namen = ", ".join(name(s_) for s_ in oben[:-1]) + " sowie " + name(oben[-1])
    teile.append(notiz(xb[0] - 3.6, oben_, xb[2] - xb[0] - 4, 2, "Der Weg dorthin führt<br>über fünf Ergebnisstufen",
                       '<p class="no-b">Jede Stufe beschreibt einen Zustand, der erreicht ist. Die Arbeitspakete der drei '
                       f'Stoßrichtungen {e(namen)} sind auf diese Stufen ausgerichtet und in ihre Abhängigkeiten gebracht.</p>'
                       f'<p class="no-b"><b>Level 1 am {d(g1["faellig_am"]).strftime("%d.%m.%Y")}:</b> LEA geht auf der '
                       'Jahresauftakttagung live.</p>'
                       f'<p class="no-b"><b>Level 2 am {d(g2["faellig_am"]).strftime("%d.%m.%Y")}:</b> {e(g2["titel"])}.</p>'))
    teile.append(notiz(xb[2] - 3.6, oben_, x1 - xb[2] - 6, 3, "Ende 2027 ist die „beste<br>Akademie“ sichtbar",
                       f'<p class="no-b"><b>Level 3 am {d(g3["faellig_am"]).strftime("%d.%m.%Y")}:</b> {e(g3["titel"])}.</p>'
                       '<p class="no-b">Angebote, Kanäle und Formate laufen im Alltag. LEOS 2.0 ist von Juli bis Dezember 2027 umgesetzt.</p>'))
    teile.append(notiz(x1 - 3.6, oben_, FW - x1 + 3.6, 1, "Das Ziel: die beste<br>Akademie der Branche",
                       f'<p class="no-b"><b>Bis {d(g5["faellig_am"]).strftime("%d.%m.%Y")}:</b> {e(g5["titel"])}. '
                       'Sie ist die beste Akademie der Versicherungsbranche und sichert die menschliche Wettbewerbsfähigkeit '
                       'im KI-Zeitalter – langfristig.</p>'
                       f'<p class="no-b"><b>Level 4 am {d(g4["faellig_am"]).strftime("%d.%m.%Y")}:</b> {e(g4["titel"])} – '
                       'Wirkung wird gemessen und belegt.</p>'))
    return seite("Das Ziel steht. Der Weg auch",
                 "Bis Ende 2028 ist die SV Akademie die beste Akademie der Branche. Der Weg dorthin ist in fünf Ergebnisstufen geplant.",
                 "".join(teile))


# ---------- Blatt 2: was jetzt vor uns liegt ----------
def plan_naechste():
    LINKS, VOR, PW = 58, 9, 236
    g1 = gates[0]
    a0, b0 = d("2026-10-01"), d("2027-02-28")

    def x(t):   # Halte vor Oktober (30.09.) stehen auf dem Startgleis vor dem ersten Monat
        return LINKS + VOR + max((t - a0).days, -4) / ((b0 - a0).days + 1) * PW

    # alles, was vor Level 1 beginnt oder fällig ist – auch Pakete, die erst in Level 2 enden (Lernen der Zukunft)
    rel = [p for p in pakete if eltern(p) and (d(p["beginnt_am"]) or d(p["faellig_am"])) <= d(g1["faellig_am"])]
    fokus = [s for s in oben if any(eltern(p)["id"] == s["id"] for p in rel)]
    lanes, y = [], 38
    for s in fokus:
        s["_kopf"] = y; y += 13
        for k in kinder(s["id"]):
            if any(p["strang_id"] == k["id"] for p in rel):
                lanes.append((s, k, y)); y += 18
        y += 1
    TY = y + 4                                      # Zeile für die Gremientermine (schwarze Rauten wie im Dashboard)
    H, W = TY + 6, LINKS + VOR + PW + 4
    o = []
    MON = {1: "Jan.", 2: "Feb.", 3: "März", 4: "Apr.", 5: "Mai", 6: "Juni", 7: "Juli", 8: "Aug.", 9: "Sept.", 10: "Okt.", 11: "Nov.", 12: "Dez."}
    m = a0
    while m <= b0:
        xm = x(m)
        o.append(f'<line x1="{xm:.2f}" y1="30" x2="{xm:.2f}" y2="{H:.1f}" stroke="{RASTER}" stroke-width="0.3"/>')
        o.append(text(xm + 1.4, 33.5, f"{MON[m.month]} {m.year}", "monat"))
        m = (m.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
    for s in fokus:
        o.append(stossrichtung(0, s["_kopf"], s))
    lane_y = {}
    for s, k, ly in lanes:
        lane_y[k["id"]] = ly
        o.append(f'<line x1="{LINKS + 1}" y1="{ly:.2f}" x2="{W:.2f}" y2="{ly:.2f}" stroke="{LINIE}" stroke-width="1.3" stroke-linecap="round"/>')
        if k["id"] != s["id"]:                       # direkt an der Stoßrichtung: kein eigener Linienname
            o.append(text(LINKS - 4, ly + 1, k["titel"], "lname", "end"))
        fertig = [p for p in rel if p["strang_id"] == k["id"] and zustand(p) == "fertig"]
        if fertig:                                    # gefahrener Weg bis zum Ende des Erledigten
            xa = max(x(d(p["faellig_am"])) for p in fertig)
            o.append(f'<line x1="{LINKS + 1:.2f}" y1="{ly:.2f}" x2="{xa:.2f}" y2="{ly:.2f}" stroke="{s["_farbe"]}" stroke-width="1.3"/>'
                     f'<line x1="{LINKS + 1:.2f}" y1="{ly - 1.7:.2f}" x2="{LINKS + 1:.2f}" y2="{ly + 1.7:.2f}" stroke="{s["_farbe"]}" stroke-width="1.1" stroke-linecap="round"/>')
    pos, anker = {}, {}
    for p in rel:
        b = x(d(p["faellig_am"]))
        pos[str(p["id"])] = (x(d(p["beginnt_am"])) if p["beginnt_am"] else b, b, lane_y[p["strang_id"]])
    for p in rel:   # gestrichelte Abhängigkeit zwischen Linien: vom Ende der Vorarbeit senkrecht, dann waagerecht hinein
        for v in p["vorgaenger"] or []:
            if v in pos and str(p["id"]) in pos:
                xa1, xb1, y1 = pos[v]
                xa2, xb2, y2 = pos[str(p["id"])]
                if abs(y1 - y2) < 0.1:
                    continue
                xs = min(xb1, xa2 - 3)
                o.append(f'<path d="M{xs:.2f} {y1 + (2.1 if y2 > y1 else -2.1):.2f} V{y2:.2f} H{xa2 - 0.3:.2f}" fill="none" stroke="{GRAU2}" stroke-width="0.35" stroke-dasharray="1 1.4"/>')
    for p in sorted(rel, key=lambda p: p["beginnt_am"] or p["faellig_am"]):
        xa, xb, ly = pos[str(p["id"])]
        z = zustand(p)
        stark = z == "läuft"
        s_ = eltern(p)
        if p["beginnt_am"]:
            o.append(pill(xa, xb, ly, 4.2, SCHWARZ if stark else GRAU2, 0.9 if stark else 0.5, LINIE if z == "fertig" else "#fff"))
            dat = f"{d(p['beginnt_am']).strftime('%d.%m.')} – {d(p['faellig_am']).strftime('%d.%m.%Y')}"
        elif z == "fertig":                          # erledigter Halt: kleiner Punkt auf der gefahrenen Linie
            o.append(halt(xb, ly, 1.3, "#fff", 0.5, s_["_farbe"]))
            dat = d(p["faellig_am"]).strftime("%d.%m.%Y")
        else:                                         # anstehender Halt: Ring wie im Dashboard
            o.append(halt(xb, ly, 2.4, SCHWARZ if stark else GRAU2, 1.0 if stark else 0.5))
            dat = d(p["faellig_am"]).strftime("%d.%m.%Y")
        cls = "ptit stark" if stark else "ptit"
        breite = (xb - xa) - 4 if p["beginnt_am"] else 26
        zeilen = umbruch(p["titel"], max(10, int(breite / 1.7))) if len(p["titel"]) * 1.7 > breite else [p["titel"]]
        if not p["beginnt_am"] and z == "fertig":    # erledigter Halt: Name klein unter der Linie – oben bleibt Platz für das Laufende
            for j, zl in enumerate(zeilen):
                o.append(text(xb, ly + 5.6 + j * 3.4, zl, "pdat", "middle"))
            continue
        for j, zl in enumerate(zeilen):
            o.append(text((xa + xb) / 2, ly - 4.2 - (len(zeilen) - 1 - j) * 3.6, zl, cls, "middle"))
        if p["beginnt_am"]:
            o.append(text((xa + xb) / 2, ly + 6.4, dat, "pdat", "middle"))
        if p["titel"] == "Lernen der Zukunft":
            anker["lzk"] = (xb + 2.1, ly)
    xb = x(d(g1["faellig_am"]))                      # Level 1
    o.append(balken(xb, 36, H, 4.6, 1.2))
    o.append(text(xb, 14, f"Level 1 · {d(g1['faellig_am']).strftime('%d.%m.%Y')}", "lvl", "middle"))
    o.append(text(xb, 19, g1["titel"], "mtit", "middle"))
    anker["m1"] = (xb, 9)
    xh = x(HEUTE)                                    # Heute-Linie wie im Dashboard: gestrichelt, oben die Marke „Heute“
    o.append(f'<line x1="{xh:.2f}" y1="30" x2="{xh:.2f}" y2="{TY - 3:.2f}" stroke="{SCHWARZ}" stroke-width="0.45" stroke-dasharray="1.4 1.4"/>')
    o.append(f'<rect x="{xh - 5.4:.2f}" y="24.2" width="10.8" height="4" rx="2" fill="{SCHWARZ}"/>' + text(xh, 27.1, "Heute", "heute", "middle"))
    # Gremientermin als Raute; die Abteilungsbesprechung am 16.11. steht schon als Halt auf der Linie Kommunikation – keine zweite Marke
    xt = x(d("2026-12-08"))
    o.append(f'<rect x="{xt - 1.9:.2f}" y="{TY - 1.9:.2f}" width="3.8" height="3.8" fill="{SCHWARZ}" transform="rotate(45 {xt:.2f} {TY:.2f})"/>')
    o.append(text(xt + 4, TY + 1, "Strategieklausur 08./09.12.", "termin"))
    anker["heute"] = (x(HEUTE), TY - 3)
    return "".join(o), W, H, anker


def blatt2():
    """Zwei Punkte (Daniel, 11.11.2026): 1 LEA geht am 19.01. live · 2 parallel: was Lernen der Zukunft bedeutet."""
    plan, W, H, a = plan_naechste()
    s, oy = 0.78, 48

    def t(p):
        return (p[0] * s, oy + p[1] * s)

    g1 = gates[0]
    teile = [f'<g transform="translate(0 {oy}) scale({s})">{plan}</g>']
    mx, my = t(a["m1"])                      # 1 – über Level 1, Bezugslinie senkrecht nach unten auf den Level-Titel
    y1 = 2
    teile.append(leitlinie([(mx, y1 + 7), (mx, oy + 9 * s)]))
    teile.append(notiz(mx - 3.6, y1, min(150, FW - mx + 3.6), 1, f"Am {d(g1['faellig_am']).strftime('%d.%m.%Y')} geht LEA live",
                       absaetze(g1["beschreibung"])))
    lx, ly = t(a["lzk"])                     # 2 – rechts neben dem Ende von Lernen der Zukunft, Bezugslinie waagerecht
    x2 = W * s + 10
    teile.append(leitlinie([(x2, ly), (lx + 1.2, ly)]))
    teile.append(notiz(x2 - 3.6, ly - 3.4, FW - x2 + 3.6, 2, "Parallel: Was bedeutet<br>Lernen der Zukunft?",
                       '<p class="no-b">Von November bis Ende Februar entsteht das Bild: Welche Zukunftskompetenzen braucht die SV, '
                       'wie greifen die drei Ebenen ineinander, und welche Rolle hat der Trainer der Zukunft?</p>'
                       '<p class="no-b"><b>Ab April 2027</b> bauen darauf das Konzept Kompetenzentwicklung sowie Tools, Formate '
                       'und Medien auf.</p>'))
    return seite("Bis zur Jahresauftakttagung geht LEA live",
                 "Am 19.01.2027 geht der KI-Assistent LEA auf der Jahresauftakttagung live. Parallel klären wir, was Lernen der "
                 "Zukunft für die SV Akademie bedeutet.",
                 "".join(teile))


# ---------- Seite im SV-Design ----------
def schrift(datei):
    return "data:font/ttf;base64," + base64.b64encode((SCHRIFTEN / datei).read_bytes()).decode()


def logo_weiss():
    return "data:image/svg+xml;base64," + base64.b64encode(re.sub(r'fill="#[0-9A-Fa-f]{6}"', 'fill="#FFFFFF"', LOGO).encode()).decode()


def seite(h1, lead, inhalt):
    return (f'<section class="blatt"><header class="svk"><h1>{e(h1)}</h1><img src="{logo_weiss()}" alt="SV SparkassenVersicherung"></header>'
            f'<p class="lead">{e(lead)}</p>'
            f'<svg class="flaeche" viewBox="0 0 {FW} {FH}" xmlns="http://www.w3.org/2000/svg">{inhalt}</svg>'
            f'<footer class="fuss"><span></span><span>www.sparkassenversicherung.de</span></footer></section>')


def css(abstand):
    return f"""
@font-face{{font-family:'SV Head';src:url({schrift('SparkasseHead_Rg.ttf')});font-weight:100 900}}
@font-face{{font-family:'SV Text';src:url({schrift('SparLt.ttf')});font-weight:100 499}}
@font-face{{font-family:'SV Text';src:url({schrift('SparRg.ttf')});font-weight:500 900}}
@page {{ size: 420mm 297mm; margin: 0; }}
* {{ box-sizing: border-box; font-synthesis: none; letter-spacing: normal !important; }}
html, body {{ margin: 0; background: #fff; }}
body {{ font-family: 'SV Text', Arial, sans-serif; color: {SCHWARZ}; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
.blatt {{ width: 420mm; height: 297mm; margin: 0; background: #fff; position: relative; display: flex; flex-direction: column;
  padding: 0 22mm 10mm; break-after: page; overflow: hidden; }}
.svk {{ margin: 0 -22mm; padding: 11mm 22mm; background: {ROT}; display: flex; align-items: center; justify-content: space-between; gap: 20mm; }}
.svk h1 {{ margin: 0; font: 400 30pt/1.1 'SV Head', Arial, sans-serif; color: #fff; }}
.svk img {{ height: 13mm; width: auto; flex: none; }}
.lead {{ margin: {abstand:.2f}mm 0 0; max-width: 240mm; font: 400 10.5pt/1.5 'SV Text', Arial, sans-serif; color: {TEXT}; }}
.flaeche {{ display: block; width: 376mm; height: 214mm; margin-top: 8mm; overflow: visible; }}
.flaeche text {{ font-family: 'SV Text', Arial, sans-serif; fill: {SCHWARZ}; }}
.flaeche .badge {{ font-size: 2.5px; font-weight: 700; fill: #fff; }}
.flaeche .sname {{ font-size: 3.2px; font-weight: 700; }}
.flaeche .lname {{ font-size: 2.8px; fill: {GRAU1}; }}
.flaeche .lvl {{ font-size: 2.6px; fill: {GRAU1}; }}
.flaeche .mtit {{ font-size: 3.1px; font-weight: 700; }}
.flaeche .monat {{ font-size: 2.6px; fill: {GRAU2}; }}
.flaeche .ptit {{ font-size: 3px; font-weight: 400; fill: {TEXT}; paint-order: stroke; stroke: #fff; stroke-width: .9px; stroke-linejoin: round; }}
.flaeche .ptit.stark {{ font-weight: 700; fill: {SCHWARZ}; }}
.flaeche .heute {{ font-size: 2.4px; font-weight: 700; fill: #fff; }}
.flaeche .termin {{ font-size: 2.9px; font-weight: 700; }}
.flaeche .pdat {{ font-size: 2.5px; fill: {GRAU2}; }}
.flaeche .nr {{ font: 400 5px 'SV Head', Arial, sans-serif; fill: #fff; }}
/* Aussagen an den Nummern – in der Fläche gilt 1 px = 1 mm */
.no {{ font-family: 'SV Text', Arial, sans-serif; color: {TEXT}; padding-left: .6px; }}
.no-t {{ margin: 0 0 2.6px; font: 400 5px/1.3 'SV Head', Arial, sans-serif; color: {SCHWARZ}; text-wrap: balance; }}
.no-b {{ margin: 0 0 2px; font: 400 3.4px/5px 'SV Text', Arial, sans-serif; }}
.no-b b {{ font-weight: 700; color: {SCHWARZ}; }}
.no-l {{ margin: 0 0 2px; padding: 0; list-style: none; }}
.no-l li {{ position: relative; padding: 0 0 1.4px 3.4px; font: 400 3.4px/5px 'SV Text', Arial, sans-serif; }}
.no-l li::before {{ content: "•"; position: absolute; left: 0; color: {SCHWARZ}; }}
.fuss {{ display: flex; justify-content: space-between; margin-top: auto; font: 400 7pt/1 'SV Text', Arial, sans-serif; color: {GRAU1}; }}
"""


def bauen(abstand, pdf):
    html_ = ('<!doctype html><html lang="de"><head><meta charset="utf-8"><title>SV Akademie – Projektplanung</title>'
             f'<style>{css(abstand)}</style></head><body>' + blatt1() + blatt2() + "</body></html>")
    tmp = Path(tempfile.mkdtemp()) / "projektplanung-sv.html"
    tmp.write_text(html_, encoding="utf-8")
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--no-pdf-header-footer",
                    "--virtual-time-budget=5000", f"--print-to-pdf={pdf}", tmp.as_uri()], capture_output=True)
    tmp.unlink()


def abstaende(pdf, seite_):
    """(a) Unterkante Balken bis Unterkante Überschrift, (b) Unterkante Balken bis zur ersten Zeile darunter – in mm."""
    s_ = fitz.open(pdf)[seite_]; dpi = 300
    pm = s_.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72), clip=fitz.Rect(0, 0, s_.rect.width, 200))
    w, h, n, b = pm.width, pm.height, pm.n, pm.samples
    f = lambda x, y: tuple(b[(y * w + x) * n:(y * w + x) * n + 3])
    unten = max(y for y in range(h) if f(3, y)[0] > 200 and f(3, y)[1] < 60) + 1
    li, re_ = int(w * 0.04), int(w * 0.6)
    oben_schrift = max(y for y in range(unten) for x in range(li, re_, 2) if min(f(x, y)) > 200)
    inhalt = next(y for y in range(unten, h) if any(max(f(x, y)) < 200 for x in range(li, w - li, 2)))
    mm = lambda p: p / dpi * 25.4
    return mm(unten - oben_schrift - 1), mm(inhalt - unten)


if __name__ == "__main__":
    pdf = str(Path(tempfile.mkdtemp()) / "sv.pdf")
    abstand = 8.0
    bauen(abstand, pdf)
    soll, ist = abstaende(pdf, 0)
    abstand += soll - ist                    # unter dem Balken so viel Weißraum wie im Balken unter der Überschrift
    bauen(abstand, pdf)
    for i in range(2):
        soll, ist = abstaende(pdf, i)
        print(f"Seite {i + 1}: im Balken {soll:.1f} mm, darunter {ist:.1f} mm")
    dok = fitz.open(pdf); dok.set_metadata({"title": "SV Akademie – Projektplanung"})
    print("Seiten:", len(dok), "· Schriften:", sorted({x[3].split("+")[-1] for p in dok for x in p.get_fonts()}))
    dok.save(str(ZIEL), garbage=3, deflate=True)
    print("geschrieben:", ZIEL)
