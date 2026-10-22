# -*- coding: utf-8 -*-
"""Daten für die Zielansichten (Zuflussplan, U-Bahn-Plan, Startfreigabe).

Quelle ist entwicklung_strategie.json – dieselbe Datei wie der Meilensteinplan.
Schreibt entwicklung-empiria/assets/projekte/ziel-daten.js. Nach jeder Änderung
an der JSON-Datei einmal laufen lassen:  python3 ziel_daten.py
"""
import json, os
HIER = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HIER))
d = json.load(open(os.path.join(HIER, "entwicklung_strategie.json"), encoding="utf-8"))
daten = {
    "zielbild": d.get("zielbild", {}),
    "straenge": [{k: s.get(k) for k in ("id", "kurz", "label", "verantwortung", "farbe")} for s in d["straenge"]],
    "meilensteine": [{k: m.get(k) for k in ("id", "nr", "termin", "titel", "ergebnis", "braucht")} for m in d["meilensteine"]],
    "schritte": [{k: s.get(k) for k in ("id", "strang", "meilenstein", "titel", "status", "braucht")} for s in d["schritte"]],
}
ziel = os.path.join(ROOT, "entwicklung-empiria", "assets", "projekte", "ziel-daten.js")
with open(ziel, "w", encoding="utf-8") as f:
    f.write("/* erzeugt von _projektquelle/build-skripte/ziel_daten.py – nicht von Hand ändern */\n")
    f.write("window.ZIEL_DATEN = " + json.dumps(daten, ensure_ascii=False, indent=1) + ";\n")
print("ziel-daten.js geschrieben:", len(daten["schritte"]), "Schritte,", len(daten["meilensteine"]), "Meilensteine")
