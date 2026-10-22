#!/usr/bin/env python3
"""Design-Stand empiria im Projekt-Repository SV Akademie (Entscheidung A, Daniel 22.10.2026).

Die Projektseiten nutzen einen festgehaltenen Stand des empiria-Designs
(Stildatei, Skript, Logos, Schriften). Welcher Stand das ist, steht in
_projektquelle/cd/empiria-design.json - je Datei die Git-Kennung aus dem
empiria-Repo (NoahU01/empiria, Branch main).

Ändert sich das empiria-Design, übernimmt dieses Projekt den neuen Stand
nicht von selbst. Erst prüfen, Daniel fragen, nach seinem Ja übernehmen:

    python3 _projektquelle/werkzeuge/cd_abgleich.py               # nur prüfen
    python3 _projektquelle/werkzeuge/cd_abgleich.py --uebernehmen # nach Daniels Ja

Danach die Seiten im Browser ansehen und committen.
Braucht das empiria-Repo daneben (~/Projekte/empiria) oder EMPIRIA_REPO.
"""
import datetime, json, os, pathlib, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
STAND = ROOT / "_projektquelle" / "cd" / "empiria-design.json"
EMPIRIA = pathlib.Path(os.environ.get("EMPIRIA_REPO", pathlib.Path.home() / "Projekte" / "empiria"))


def git(*a, binaer=False):
    r = subprocess.run(["git", "-C", str(EMPIRIA), *a], capture_output=True, check=True)
    return r.stdout if binaer else r.stdout.decode().strip()


def main():
    if not (EMPIRIA / ".git").exists():
        sys.exit(f"empiria-Repo nicht gefunden: {EMPIRIA}")
    stand = json.loads(STAND.read_text(encoding="utf-8"))
    zweig = stand["zweig"]
    git("fetch", "-q", "origin", zweig)
    ref = f"origin/{zweig}"
    neu = {}
    for hier, dort in stand["dateien"].items():
        try:
            neu[hier] = git("rev-parse", f"{ref}:{dort}")
        except subprocess.CalledProcessError:
            neu[hier] = None
    geaendert = [h for h in stand["dateien"] if neu[h] != stand["kennungen"].get(h)]
    if not geaendert:
        print(f"Design-Stand aktuell (empiria {zweig}, festgehalten am {stand['festgehalten_am']}).")
        return
    print(f"Neuer Design-Stand bei empiria ({zweig}) – {len(geaendert)} Datei(en) anders:")
    for h in geaendert:
        print(f"  {'fehlt dort' if neu[h] is None else 'geändert  '}  {h}")
    if "--uebernehmen" not in sys.argv:
        print("\nNichts übernommen. Erst nach Daniels Ja: --uebernehmen")
        return
    for h in geaendert:
        if neu[h] is None:
            sys.exit(f"Abbruch: {stand['dateien'][h]} gibt es bei empiria nicht mehr – bitte klären.")
        (ROOT / h).write_bytes(git("show", f"{ref}:{stand['dateien'][h]}", binaer=True))
        stand["kennungen"][h] = neu[h]
    stand["commit"] = git("rev-parse", "--short", ref)
    stand["festgehalten_am"] = datetime.date.today().strftime("%d.%m.%Y")
    STAND.write_text(json.dumps(stand, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("\nÜbernommen. Seiten im Browser prüfen, dann committen.")


if __name__ == "__main__":
    main()
