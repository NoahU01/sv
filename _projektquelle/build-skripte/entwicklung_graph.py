# -*- coding: utf-8 -*-
"""Rechnet den Strategie-Graphen einmal beim Build durch.

Übertragen aus sofort sichtbar (src/_data/strategieGraph.js, Branch daniel).
Damit bleiben die Seitenvorlagen dumm und alle Darstellungen teilen sich
dieselbe Wahrheit: Rang, Blockaden, Fortschritt und fertige Koordinaten für
die gezeichneten Varianten (Liniennetz "fein", Graph "dunkel"/"hell").

Nur für den Branch daniel – siehe entwicklung_seiten.py.
"""
import json, math, os

WORKDIR = os.path.dirname(os.path.abspath(__file__))


def _runde(x):
    # wie Math.round in JavaScript (x.5 rundet auf)
    return int(math.floor(x + 0.5))


def berechne(pfad=os.path.join(WORKDIR, "entwicklung_strategie.json")):
    with open(pfad, encoding="utf-8") as f:
        roh = json.load(f)

    nach_id = {s["id"]: s for s in roh["schritte"]}
    ist_fertig = lambda i: nach_id[i]["status"] == "erreicht"

    # --- Rang: längster Pfad von einem Startknoten ----------------------
    rang = {}

    def rang_von(i, pfad=None):
        pfad = pfad if pfad is not None else set()
        if i in rang:
            return rang[i]
        if i in pfad:
            raise ValueError('Zyklus im Strategie-Graphen bei "%s"' % i)
        pfad.add(i)
        vorher = [rang_von(b, pfad) for b in nach_id[i]["braucht"]]
        pfad.discard(i)
        wert = max(vorher) + 1 if vorher else 0
        rang[i] = wert
        return wert

    for s in roh["schritte"]:
        rang_von(s["id"])

    # --- Anreichern -----------------------------------------------------
    schritte = []
    for s in roh["schritte"]:
        offen = [b for b in s["braucht"] if not ist_fertig(b)]
        n = dict(s)
        n.setdefault("details", [])
        n.setdefault("offen", [])
        n.setdefault("wer", "")
        n.update({
            "rang": rang[s["id"]],
            "blockiertVon": offen,
            # machbar = alle Vorbedingungen stehen. dran = wird bearbeitet, entweder
            # weil es frei ist oder weil wir es bewusst vorgezogen haben ("aktiv").
            "machbar": s["status"] != "erreicht" and not offen,
            "dran": s["status"] != "erreicht" and (s["status"] == "aktiv" or not offen),
            "nachfolger": [a["id"] for a in roh["schritte"] if s["id"] in a["braucht"]],
            # Abhängigkeiten, die den Strang wechseln – nur die sind erklärungsbedürftig
            "querBraucht": [b for b in s["braucht"] if nach_id[b]["strang"] != s["strang"]],
        })
        schritte.append(n)

    schritt_nach_id = {s["id"]: s for s in schritte}

    def anteil(liste):
        if not liste:
            return 0
        return _runde(len([s for s in liste if s["status"] == "erreicht"]) / len(liste) * 100)

    straenge = []
    for i, strang in enumerate(roh["straenge"]):
        eigene = [s for s in schritte if s["strang"] == strang["id"]]
        straenge.append(dict(strang, spur=i, schritte=eigene, anzahl=len(eigene), fortschritt=anteil(eigene)))
    strang_nach_id = {t["id"]: t for t in straenge}

    meilensteine = []
    for m in roh["meilensteine"]:
        eigene = [s for s in schritte if s["meilenstein"] == m["id"]]
        meilensteine.append(dict(m, schritte=eigene, anzahl=len(eigene), fortschritt=anteil(eigene),
                                 erreicht=all(s["status"] == "erreicht" for s in eigene)))

    # Ergebnisstufen hängen an festen Terminen: Titel = Termin, ggf. mit Namen
    for m in meilensteine:
        termin, name = m.get("termin", ""), m.get("titel", "")
        m["titel"] = " · ".join(t for t in (termin, name) if t) or "Stufe %s" % m["nr"]

    aktueller = next((m for m in meilensteine if not m["erreicht"]), meilensteine[-1])

    aufwand_namen = {"S": "Klein (Stunden bis ein Tag)", "M": "Mittel (mehrere Tage)", "L": "Groß (Wochen)"}
    personen = roh.get("personen", {})
    for s in schritte:
        strang = strang_nach_id[s["strang"]]
        stein = next(m for m in meilensteine if m["id"] == s["meilenstein"])
        s["aufwandLabel"] = aufwand_namen.get(s["aufwand"], s["aufwand"])
        s["werName"] = personen.get(s["wer"], "")
        s["strangLabel"] = strang["label"]
        s["strangKurz"] = strang["kurz"]
        s["verantwortung"] = strang.get("verantwortung", "")
        s["farbe"] = strang["farbe"]
        s["spur"] = strang["spur"]
        s["meilensteinNr"] = stein["nr"]
        s["meilensteinTitel"] = stein["titel"]

    # --- Layout "fein": Liniennetz nach Meilensteinen --------------------
    # oben lässt Platz für die Stationsköpfe, damit sie nicht in den Linien liegen
    # SV: "oben" von 168 auf 232 – Platz für Ergebnisse als Punkteliste
    M = {"halt": 176, "station": 128, "spurLuft": 122, "oben": 232, "links": 92, "rechts": 92}

    # SV: Schritte eines Strangs mit gleichem Rang laufen parallel. Sie teilen
    # sich eine Spalte und liegen untereinander; die Linie verzweigt sich
    # davor und läuft danach wieder zusammen.
    M["ast"] = 44  # senkrechter Abstand paralleler Halte

    metro_halte = []
    metro_stationen = []
    x = M["links"]
    for m in meilensteine:
        pro_strang = []
        for st in straenge:
            eigene = [s for s in m["schritte"] if s["strang"] == st["id"]]
            raenge = sorted(set(s["rang"] for s in eigene))
            pro_strang.append([[s for s in eigene if s["rang"] == r] for r in raenge])
        breiteste = max([1] + [len(spalten) for spalten in pro_strang])
        for spur, spalten in enumerate(pro_strang):
            # Halte mittig im Abschnitt verteilen, damit kurze Stränge nicht kleben
            versatz = (breiteste - len(spalten)) / 2
            for i, gruppe in enumerate(spalten):
                for j, s in enumerate(gruppe):
                    ast = (j - (len(gruppe) - 1) / 2) * 2 * M["ast"] if len(gruppe) > 1 else 0
                    metro_halte.append({"id": s["id"], "x": x + (versatz + i + 0.5) * M["halt"],
                                        "y": M["oben"] + spur * M["spurLuft"] + ast})
        x += breiteste * M["halt"]
        metro_stationen.append({"id": m["id"], "nr": m["nr"], "titel": m["titel"], "ergebnis": m["ergebnis"],
                                "erreicht": m["erreicht"], "fortschritt": m["fortschritt"], "x": x + M["station"] / 2})
        x += M["station"]

    metro_pos = {h["id"]: h for h in metro_halte}
    for s in schritte:
        s["mx"] = metro_pos[s["id"]]["x"]
        s["my"] = metro_pos[s["id"]]["y"]

    # Auf einer Linie fährt man durch alle früheren Halte. Sie sind damit
    # stillschweigend Voraussetzung, auch ohne in "braucht" zu stehen.
    # Parallele Halte (gleiches x) setzen einander nicht voraus.
    for st in straenge:
        for s in st["schritte"]:
            s["metroVorher"] = [v["id"] for v in st["schritte"] if metro_pos[v["id"]]["x"] < metro_pos[s["id"]]["x"]]

    metro_breite = x + M["rechts"]
    metro_hoehe = M["oben"] + (len(straenge) - 1) * M["spurLuft"] + 96

    def strecke(x1, y1, x2, y2):
        if y1 == y2:
            return "M %s %s L %s %s" % (x1, y1, x2, y2)
        xm = (x1 + x2) / 2
        return "M %s %s C %s %s, %s %s, %s %s" % (x1, y1, xm, y1, xm, y2, x2, y2)

    metro_linien = []
    for spur, st in enumerate(straenge):
        y = M["oben"] + spur * M["spurLuft"]
        # Jeder Abschnitt gehört zu dem Halt, auf den er zuläuft: Ist dieser Halt
        # erledigt oder gerade dran, wird der Abschnitt davor dick gezeichnet.
        spalten_x = sorted(set(metro_pos[s["id"]]["x"] for s in st["schritte"]))
        spalten = [[s for s in st["schritte"] if metro_pos[s["id"]]["x"] == sx] for sx in spalten_x]
        start_x = M["links"] / 2
        ende_x = metro_breite - M["rechts"] / 2
        abschnitte = []
        vorige = []
        for gruppe in spalten:
            for s in gruppe:
                p = metro_pos[s["id"]]
                # Zulauf: von den Vorgängern im selben Strang, sonst von der ganzen Vorspalte
                quellen = [v for v in vorige if v["id"] in s["braucht"]] or vorige
                punkte = [(metro_pos[v["id"]]["x"], metro_pos[v["id"]]["y"]) for v in quellen] or [(start_x, y)]
                for qx, qy in punkte:
                    abschnitte.append({"pfad": strecke(qx, qy, p["x"], p["y"]),
                                       "dick": s["status"] == "erreicht" or s["dran"], "bis": s["id"]})
            vorige = gruppe
        # Hinter dem letzten Halt liegt kein erreichter Punkt mehr
        for v in vorige or [None]:
            qx, qy = (metro_pos[v["id"]]["x"], metro_pos[v["id"]]["y"]) if v else (start_x, y)
            abschnitte.append({"pfad": strecke(qx, qy, ende_x, y), "dick": False, "bis": None})
        metro_linien.append({"id": st["id"], "label": st["label"], "kurz": st["kurz"], "frage": st["frage"],
                             "verantwortung": st.get("verantwortung", ""),
                             "farbe": st["farbe"], "y": y, "fortschritt": st["fortschritt"], "abschnitte": abschnitte})

    # Nur Abhängigkeiten zwischen verschiedenen Strängen zeichnen – der Rest
    # steckt schon in der Linie selbst und würde das Bild zumüllen.
    metro_quer = []
    for s in schritte:
        for b in s["querBraucht"]:
            a, z = metro_pos[b], metro_pos[s["id"]]
            mitte = (a["y"] + z["y"]) / 2
            von = schritt_nach_id[b]
            metro_quer.append({
                "von": b, "nach": s["id"],
                "text": '%s „%s“ wartet auf %s „%s“' % (s["strangKurz"], s["titel"], von["strangKurz"], von["titel"]),
                "pfad": "M %s %s C %s %s, %s %s, %s %s" % (a["x"], a["y"], a["x"], mitte, z["x"], mitte, z["x"], z["y"]),
            })

    metro = {"breite": metro_breite, "hoehe": metro_hoehe, "linien": metro_linien,
             "stationen": metro_stationen, "quer": metro_quer}

    # --- Layout "dunkel"/"hell": Abschnitte je Ergebnisstufe ------------
    # Nicht nach reiner Abhängigkeitstiefe, sondern in Blöcken je Stufe. So
    # lassen sich Stationen wie im Liniennetz dazwischensetzen. Zulässig, weil
    # kein Schritt von einer späteren Stufe abhängt – alle Pfeile zeigen rechts.
    G2 = {"breite": 238, "hoehe": 110, "spaltenLuft": 58, "zeilenLuft": 16, "spurLuft": 56, "station": 132}

    lokal_rang = {}

    def lokal(i):
        if i in lokal_rang:
            return lokal_rang[i]
        s = schritt_nach_id[i]
        innen = [b for b in s["braucht"] if schritt_nach_id[b]["meilenstein"] == s["meilenstein"]]
        wert = max(lokal(b) for b in innen) + 1 if innen else 0
        lokal_rang[i] = wert
        return wert

    for s in schritte:
        lokal(s["id"])

    abschnitte = [{"stein": m, "spalten": max(lokal_rang[s["id"]] for s in m["schritte"]) + 1} for m in meilensteine]
    zelle2 = lambda m, lr, sid: [s for s in m["schritte"] if lokal_rang[s["id"]] == lr and s["strang"] == sid]

    g2_stapel = []
    for st in straenge:
        mx = 1
        for a in abschnitte:
            for lr in range(a["spalten"]):
                mx = max(mx, len(zelle2(a["stein"], lr, st["id"])))
        g2_stapel.append(mx)
    g2_spur_hoehe = [n * G2["hoehe"] + (n - 1) * G2["zeilenLuft"] for n in g2_stapel]
    g2_spur_y = [sum(g2_spur_hoehe[:i]) + i * G2["spurLuft"] for i in range(len(g2_spur_hoehe))]

    g2_stationen = []
    gx = 0
    for index, a in enumerate(abschnitte):
        for lr in range(a["spalten"]):
            for spur, st in enumerate(straenge):
                for i, s in enumerate(zelle2(a["stein"], lr, st["id"])):
                    s["g2x"] = gx + lr * (G2["breite"] + G2["spaltenLuft"])
                    s["g2y"] = g2_spur_y[spur] + i * (G2["hoehe"] + G2["zeilenLuft"])
        gx += a["spalten"] * G2["breite"] + (a["spalten"] - 1) * G2["spaltenLuft"] + G2["spaltenLuft"]
        m = a["stein"]
        g2_stationen.append({"id": m["id"], "nr": m["nr"], "titel": m["titel"], "ergebnis": m["ergebnis"],
                             "erreicht": m["erreicht"], "fortschritt": m["fortschritt"], "anzahl": m["anzahl"],
                             "x": gx + G2["station"] / 2, "letzte": index == len(abschnitte) - 1})
        gx += G2["station"] + G2["spaltenLuft"]

    def bogen2(a, b):
        x1 = a["g2x"] + G2["breite"]
        y1 = a["g2y"] + G2["hoehe"] / 2
        x2 = b["g2x"]
        y2 = b["g2y"] + G2["hoehe"] / 2
        dx = max(30, (x2 - x1) / 2)
        return "M %s %s C %s %s, %s %s, %s %s" % (x1, y1, x1 + dx, y1, x2 - dx, y2, x2, y2)

    g2_kanten = [{"von": b, "nach": s["id"], "quer": nach_id[b]["strang"] != s["strang"],
                  "pfad": bogen2(schritt_nach_id[b], s)} for s in schritte for b in s["braucht"]]

    graph2 = {
        "breite": gx - G2["spaltenLuft"],
        "hoehe": g2_spur_y[-1] + g2_spur_hoehe[-1],
        "knotenBreite": G2["breite"],
        "knotenHoehe": G2["hoehe"],
        # Wie weit das Bahnband oben und unten über die Karten hinausragt.
        # Die Leiste links muss denselben Wert verwenden.
        "bandLuft": 16,
        "kanten": g2_kanten,
        "stationen": g2_stationen,
        "spuren": [{"id": st["id"], "label": st["label"], "kurz": st["kurz"], "frage": st["frage"],
                    "verantwortung": st.get("verantwortung", ""),
                    "farbe": st["farbe"], "fortschritt": st["fortschritt"], "y": g2_spur_y[i],
                    "hoehe": g2_spur_hoehe[i]} for i, st in enumerate(straenge)],
    }

    return dict(roh, graph2=graph2, schritte=schritte, straenge=straenge, meilensteine=meilensteine,
                aktuellerMeilenstein=aktueller, fortschritt=anteil(schritte), anzahl=len(schritte),
                erledigt=[s for s in schritte if s["status"] == "erreicht"],
                machbar=[s for s in schritte if s["machbar"]], metro=metro)
