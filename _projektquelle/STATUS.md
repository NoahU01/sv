# SV Akademie – Strategie-Homepage (Mock-up) — Statusnotiz

Stand: 05.08.2026, Runde 4 abgeschlossen (Du-Ansprache durchgängig, statisches Kreislauf-Bild,
Flat-Illustrationen, über-uns komplett überarbeitet inkl. PDF-Vorschau, Team-Grid, Einbettung & Rolle).
Alle 5 Seiten neu gebaut, validiert (HTML-Tag-Balance + JS-Syntax fehlerfrei) und final kopiert.

## Ziel
Voll funktionsfähiges, aber nicht live geschaltetes HTML-Dokument (kein Hosting, kein SSL nötig),
das das mit der Strategie entwickelte Geschäftsmodell der SV Akademie als Homepage visualisiert.
Zielgruppe der Website selbst: intern zur Präsentation/Diskussion beim Kunden.

## Zielgruppe der SV Akademie (Inhalt der Website)
Mitarbeitende und Vertriebspartner der SV (Sparkassen-Finanzgruppe) — interne Weiterbildung/Personalentwicklung,
kein Endkunden-Retailgeschäft.

## Struktur (aktueller Stand: fertig gebaut)
5 verlinkte HTML-Dateien im Ordner `SV-Akademie-Website/` (eine Ebene über diesem Ordner):

1. **index.html** – Hauptseite in der vom Kunden vorgegebenen Logik:
   Header (Nutzenversprechen) → Problem → Lösung & USP → Zusammenarbeit (4 Schritte) →
   Leadmagnet "Was jetzt?" (3 Kacheln: Portal 24/7, Quick-Check, Community-Austausch) →
   FAQ (Akkordeon) → Kontakt (Formular + CTA) → Footer mit Impressum/Datenschutz (als Pop-up-Mockup)
2. **ueber-uns.html** – echte Unterseite, Inhalt basiert auf dem hochgeladenen PDF
   "01_EMP_SV Akademie_Selbstverständnis 4.0.pdf" (Antrieb, 3 Handlungsfelder, Haltung/Werte)
3. **portal.html** – Mock-up der Login-Seite für das noch nicht existierende "Portal 24/7",
   inkl. Dashboard-Vorschau (Trainings, Mediathek, Fortschritt) ohne echten Login
4. **quickcheck.html** – Buchungsseite "Quick-Check Bedarfsklärung": 3 Auswahlmöglichkeiten
   (Für mich persönlich / Für mein Team / Für meine Vertriebseinheit) mit jeweils eigenen
   Zielfragen, Terminslot-Auswahl, Buchungsformular, PDF-Download (echter Vorbereitungsleitfaden),
   .ics-Kalenderdownload
5. **community.html** – Buchungsseite für den digitalen Community-Austausch (Webinar-Stil),
   Agenda-Vorschau, vergangene Termine, Anmeldeformular, .ics-Kalenderdownload

## Design / Markenwelt
- Farben: vollständig aus `Farben.pptx` extrahiert (Sparkassen-Rot #EE0000 als Leitfarbe,
  Grautöne #444–#F0F0F0, Akzente Violet #9B348E, Blau #2C57D2, Hellblau #00ACD3,
  Dunkelgrün #009864, Gelb #FFC900, Orange #FF8F00). Werte stehen in `build-skripte/build_common.py` (Dict `C`).
- Fonts: "Sparkasse Head" (Headlines) und "Sparkasse Lt" (Fließtext), als Base64 eingebettet.
- Logos: `svakademie.png` (farbig) und `svakademie-weiss-neg.png` (weiß, für dunkle Flächen).
- Bildwelt: bewusst grafisch/illustrativ statt Fotos (Raketen-Illustration aus dem Selbstbild-PDF,
  3 Streamline-Ultimate-Icons für die 3 Handlungsfelder), da keine Fotos bereitgestellt wurden.
- Layout-Vorbild: sparkassenversicherung.de (Look, nicht Inhalt) — kräftige Rot-Hero, Cloud-Divider
  wie im Selbstbild-PDF, Karten-Module, klare CTAs.

## Technischer Aufbau
- Alles in sich geschlossen: Fonts/Logos/Rakete als Base64 (data URI) direkt im HTML, keine externen
  Abhängigkeiten, funktioniert offline per Doppelklick.
- Build erfolgt über Python-Skripte (nicht Hand-HTML), damit Änderungen an Farben/Fonts/Nav zentral
  in `build_common.py` + `style.css.tpl` + `shared.js.tpl` gemacht werden können und sich automatisch
  auf alle 5 Seiten auswirken. Einzelne Seiteninhalte stehen in `page_*.py`.
- Reihenfolge zum Neu-Bauen: zuerst `build_common.py` läuft (lädt `assets_b64.json`), dann die
  einzelnen `page_*.py`-Skripte, die jeweils eine fertige HTML-Datei schreiben.
- PDF-Leitfaden wird mit `make_pdf.py` (reportlab) erzeugt und in `assets_b64.json` unter dem Key
  `leitfaden_pdf` abgelegt.
- Interaktive Elemente sind "echt" (kein Fake): Akkordeon, Modals/Pop-ups, mobile Navigation,
  Formular-Mock-Submits mit Bestätigungs-Pop-up, echter PDF-Download, echter .ics-Kalenderdownload.
- Kontakt-/Buchungsformulare senden technisch nichts (rein clientseitiges Mock-up, wie in der
  Anfrage vorgesehen — die Seite soll nicht live gehen).

## Offene Punkte / mögliche nächste Schritte
- Visuelle Prüfung im echten Browser steht noch aus (in der Cloud-Sandbox war kein Headless-Browser
  lauffähig, daher nur automatisierte Struktur-/Code-Prüfung: HTML-Tag-Balance, JS-Syntax,
  Base64-Integrität, Linkprüfung — alles fehlerfrei).
- Feedback zu Copy/Tonalität der Problem-/Lösungs-/FAQ-Texte steht noch aus (aktuell professionell
  entworfen basierend auf Selbstbild-PDF, aber nicht mit Kunde final abgestimmt).
- Eventuell echte Fotos später gegen die grafische Bildwelt austauschen, falls gewünscht.
- Rechtliche Hinweise (Impressum/Datenschutz) sind bewusst als Platzhalter/Pop-up markiert
  ("Strategie-Mock-up, nicht produktiv im Einsatz") — für eine echte Veröffentlichung zu ersetzen.

## Wie es weitergeht
Diese Unterhaltung im Cowork-Chat einfach fortsetzen — der komplette Verlauf inkl. aller
Entscheidungen bleibt erhalten. Alternativ: diesen Ordner (`SV-Akademie-Website/`, inkl.
`_projektquelle/`) an eine neue Unterhaltung anhängen bzw. den Inhalt dieser Datei einfügen,
falls in einem neuen Chat weitergearbeitet wird.

## Stand 30.09.2026 (Branch `daniel`)
- Build-Skripte laufen lokal: `cd _projektquelle/build-skripte` und dann
  `python3 page_index.py`, `page_ueberuns.py`, `page_portal.py`, `page_quickcheck.py`, `page_community.py`.
  Die Seiten werden direkt ins Repo-Wurzelverzeichnis geschrieben. HTML nie von Hand ändern.
- Menüpunkt „/ Entwicklung /“ (Aufbau wie auf der empiria-Seite): Unterseiten + Archiv. Unter „Unterseiten“ stehen nur
  neue Seiten, die Daniel entwickelt und die noch nicht auf main sind – keine bestehenden Seiten der Hauptnavigation.
  Einträge pflegen in `build_common.py` (`DEV_UNTERSEITEN`, `DEV_ARCHIV`). Sichtbar nur lokal und auf den
  Vercel-Vorschauen (`svakademie-git-…`, `svakademie-<hash>-…`), auf der Live-Adresse entfernt.
- Behoben: Handy-Menü war nur 56 px hoch und die Seite auf dem Handy doppelt so breit
  (`backdrop-filter` am Header). Burger-Menü jetzt unter 1280 px (vorher lief die Leiste ab ~1100 px aus dem Bild).
