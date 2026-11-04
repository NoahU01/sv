#!/usr/bin/env python3
"""Methoden aus dem Methodenkoffer des empiria-Dashboards übernehmen (eine Quelle, nichts doppelt pflegen).

Kopiert assets/methoden/ (methoden.js, methoden-render.js, methoden.css und die Arbeitsblätter, die der Kunde
sehen darf) aus dem Dashboard-Repo in dieses Repo und schreibt die Auswahl des Projekts (Dashboard:
projekte.projektseite.methoden – leer = alle) nach auswahl.js im selben Ordner. Interne Arbeitsblätter
(intern: true) gehen nie mit.
Läuft auf Daniels Always-on-Mac.  Aufruf:  python3 werkzeuge/methoden_uebernehmen.py  – danach committen und pushen.
"""
import json, os, re, shutil, subprocess, sys

PROJEKT = 1
ZIEL = "entwicklung-empiria/assets/methoden"          # Ordner im Repo, relativ zur Repo-Wurzel
HIER = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HIER)
QUELLE = os.path.expanduser("~/Projekte/empiria-dashboard/assets/methoden")
sys.path.insert(0, os.path.expanduser("~/AlwaysOn/supabase"))
import sql  # noqa: E402

ziel = os.path.join(REPO, ZIEL)
os.makedirs(os.path.join(ziel, "dateien"), exist_ok=True)
for f in ("methoden.js", "methoden-render.js", "methoden.css"):
    shutil.copy(os.path.join(QUELLE, f), os.path.join(ziel, f))
# nur Arbeitsblätter, die nicht intern sind
daten = subprocess.run(["node", "-e", "global.window={};require(process.argv[1]);console.log(JSON.stringify(window.METHODEN))",
                        os.path.join(QUELLE, "methoden.js")], capture_output=True, text=True, check=True).stdout
methoden = json.loads(daten)
noetig = set()
for m in methoden:
    for b in m.get("arbeitsblaetter") or []:
        if not b.get("intern"):
            noetig.update([b["datei"]] + ([b["bild"]] if b.get("bild") else []))
for f in os.listdir(os.path.join(ziel, "dateien")):
    if f not in noetig: os.remove(os.path.join(ziel, "dateien", f))
for f in noetig:
    shutil.copy(os.path.join(QUELLE, "dateien", f), os.path.join(ziel, "dateien", f))
ps = (sql.ausfuehren(f"select projektseite from projekte where id={PROJEKT}") or [{}])[0].get("projektseite") or {}
auswahl = ps.get("methoden") or None
with open(os.path.join(ziel, "auswahl.js"), "w", encoding="utf-8") as f:
    f.write("/* erzeugt von werkzeuge/methoden_uebernehmen.py – Auswahl im Dashboard (projekte.projektseite.methoden), null = alle */\n")
    f.write("window.METHODEN_AUSWAHL = " + json.dumps(auswahl) + ";\n")
print(f"Methoden übernommen: {len(methoden)} im Koffer, Auswahl: {auswahl or 'alle'}, Arbeitsblätter: {len(noetig)} Dateien")
