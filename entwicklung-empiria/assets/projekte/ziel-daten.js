/* erzeugt von _projektquelle/build-skripte/ziel_daten.py – nicht von Hand ändern */
window.ZIEL_DATEN = {
 "zielbild": {
  "kurz": "Transformation der SV Akademie",
  "text": "Platzhalter – Zielbild folgt."
 },
 "straenge": [
  {
   "id": "t1",
   "kurz": "T1",
   "label": "Transformation 1",
   "frage": "Rollen, Prozesse, KI etc.",
   "beschreibung": "",
   "verantwortung": "Lukas Euring",
   "farbe": "#C51F5D"
  },
  {
   "id": "t2",
   "kurz": "T2",
   "label": "Transformation 2",
   "frage": "USP Mensch, Zukunftskompetenzen, Lernen der Zukunft etc.",
   "beschreibung": "",
   "verantwortung": "Philip Dreyer & Stefanie Frank",
   "farbe": "#8613A1"
  },
  {
   "id": "sa",
   "kurz": "SA",
   "label": "Sichtbarkeit & Außenwirkung",
   "frage": "",
   "beschreibung": "",
   "verantwortung": "Marie Herzig",
   "farbe": "#0B9FBD"
  }
 ],
 "meilensteine": [
  {
   "id": "m1",
   "nr": 1,
   "termin": "Ende 2026",
   "titel": "Big Bang",
   "ergebnis": [
    "Die Webseite ist live.",
    "Der KI-Assistent Lea läuft.",
    "Zielbild und Strategie werden von Michael Sauerbrunn und dem Team der SV Akademie voll unterstützt."
   ],
   "braucht": [
    "sa-1-golive",
    "t1-1-lea",
    "t2-1-brainstorming"
   ]
  },
  {
   "id": "m2",
   "nr": 2,
   "termin": "30.06.2027",
   "titel": "Das Fundament steht",
   "ergebnis": [
    "Das Fundament steht: Produkte und Leistungssystem, Kommunikationskonzept 2.0 und LEOS 2.0 sind konzipiert.",
    "Die grundlegende Außenwirkung als „beste Akademie“ ist angelegt."
   ],
   "braucht": [
    "t1-2-auftrag",
    "t2-2-brainstorming",
    "sa-2-kommunikation"
   ]
  },
  {
   "id": "m3",
   "nr": 3,
   "termin": "31.12.2027",
   "titel": "",
   "ergebnis": [
    "Das Zielbild „beste Akademie“ ist nach außen sichtbar und wird so wahrgenommen.",
    "Angebote, Kanäle und Formate laufen im Alltag."
   ],
   "braucht": [
    "t1-3",
    "t2-3",
    "sa-3"
   ]
  },
  {
   "id": "m4",
   "nr": 4,
   "termin": "30.06.2028",
   "titel": "",
   "ergebnis": [
    "Das Erreichte ist untermauert: Wirkung wird gemessen und belegt.",
    "Angebote und Abläufe werden gezielt optimiert."
   ],
   "braucht": [
    "t1-4",
    "t2-4",
    "sa-4"
   ]
  },
  {
   "id": "m5",
   "nr": 5,
   "termin": "31.12.2028",
   "titel": "",
   "ergebnis": [
    "Die SV Akademie hebt das Zielbild auf das nächste Level.",
    "Die Position als „beste Akademie“ ist langfristig gesichert."
   ],
   "braucht": [
    "t1-5",
    "t2-5",
    "sa-5"
   ]
  }
 ],
 "termine": [
  {
   "id": "t-abteilung-11-2026",
   "titel": "Abteilungsbesprechung SV Akademie (PW7)",
   "monat": "2026-11",
   "tag": 16,
   "wann": "16.11.2026",
   "zusatz": "",
   "info": "Einbindung des Teams",
   "schritt": "sa-1-abteilung"
  },
  {
   "id": "t-schulungsinfotag-12-2026",
   "titel": "Schulungsinfotag Vertrieb",
   "monat": "2026-12",
   "tag": 4,
   "wann": "04.12.2026",
   "zusatz": "",
   "info": "Information der Vertriebsführungskräfte zu den Schulungen 2027. Vorstellung Homepage, Quickchecks und Lea (KI-Assistent).",
   "schritt": "sa-1-golive"
  },
  {
   "id": "t-versand-12-2026",
   "titel": "Versand der Unterlagen",
   "monat": "2026-12",
   "tag": 7,
   "wann": "07.12.2026",
   "zusatz": "",
   "info": "an alle Vertriebseinheiten",
   "schritt": "sa-1-golive"
  },
  {
   "id": "t-klausur-12-2026",
   "titel": "Strategieklausur",
   "monat": "2026-12",
   "tag": 8,
   "wann": "08./09.12.2026",
   "zusatz": "zwei Tage",
   "info": "Hotel Rössle",
   "schritt": null
  }
 ],
 "schritte": [
  {
   "id": "t1-1-taskforce",
   "strang": "t1",
   "meilenstein": "m1",
   "titel": "Taskforce KI: Ideen für Lea",
   "beschreibung": null,
   "status": "erreicht",
   "braucht": [],
   "ergebnis": "Die Taskforce KI hat Ideen zur Umsetzung des KI-Assistenten Lea entwickelt.",
   "details": [
    "Taskforce KI wird tätig",
    "Ideen zur Umsetzung des KI-Assistenten Lea"
   ],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": "2026-09",
   "zeitraum": null
  },
  {
   "id": "t1-1-copilot",
   "strang": "t1",
   "meilenstein": "m1",
   "titel": "Pilotierung Copilot Pro",
   "beschreibung": null,
   "status": "aktiv",
   "braucht": [
    "t1-1-taskforce"
   ],
   "ergebnis": "Copilot Pro wird pilotiert – ab November 2026.",
   "details": [
    "Start ab November 2026"
   ],
   "wer": "",
   "kritisch": {
    "grund": "Wie lange die Pilotierung läuft, ist offen.",
    "blockiert": "Davon hängt ab, wann die Entwicklung des KI-Assistenten Lea starten kann – und mit ihr die Kette bis zur Webseite."
   },
   "termin": "",
   "von": null,
   "monat": "2026-10",
   "zeitraum": null
  },
  {
   "id": "t1-1-lea",
   "strang": "t1",
   "meilenstein": "m1",
   "titel": "Entwicklung KI-Assistent Lea",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "t1-1-copilot"
   ],
   "ergebnis": "Der KI-Assistent Lea ist entwickelt.",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": "Oktober bis 24.11.2026",
   "von": "2026-10",
   "monat": "2026-11",
   "zeitraum": null
  },
  {
   "id": "t1-1-webseite",
   "strang": "t1",
   "meilenstein": "m1",
   "titel": "Webseite umsetzen und live schalten",
   "beschreibung": null,
   "status": "offen",
   "braucht": [],
   "ergebnis": "Die Webseite ist umgesetzt und live – voraussichtlich innerhalb des SharePoints.",
   "details": [
    "Voraussichtlich innerhalb des SharePoints"
   ],
   "wer": "",
   "kritisch": null,
   "termin": "09.11. bis 27.11.2026",
   "von": "2026-11",
   "monat": "2026-11",
   "zeitraum": true
  },
  {
   "id": "t1-2-mak",
   "strang": "t1",
   "meilenstein": "m2",
   "titel": "MAK",
   "beschreibung": null,
   "status": "offen",
   "braucht": [],
   "ergebnis": "",
   "details": [
    "Planung",
    "Zukünftige Ausstattung"
   ],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": null,
   "zeitraum": null
  },
  {
   "id": "t1-2-leos",
   "strang": "t1",
   "meilenstein": "m2",
   "titel": "LEOS 2.0",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "t1-2-mak"
   ],
   "ergebnis": "",
   "details": [
    "Konzeption unseres zukünftigen zentralen Systems"
   ],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": null,
   "zeitraum": null
  },
  {
   "id": "t1-2-auftrag",
   "strang": "t1",
   "meilenstein": "m2",
   "titel": "Sicherstellung Auftrag Dr. Jan: „1 Akademie“",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "t1-2-leos"
   ],
   "ergebnis": "",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": null,
   "zeitraum": null
  },
  {
   "id": "t1-3",
   "strang": "t1",
   "meilenstein": "m3",
   "titel": "T1 · Stufe 3",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "m2"
   ],
   "ergebnis": "Platzhalter – Details folgen.",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": null,
   "zeitraum": null
  },
  {
   "id": "t1-4",
   "strang": "t1",
   "meilenstein": "m4",
   "titel": "T1 · Stufe 4",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "t1-3"
   ],
   "ergebnis": "Platzhalter – Details folgen.",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": null,
   "zeitraum": null
  },
  {
   "id": "t1-5",
   "strang": "t1",
   "meilenstein": "m5",
   "titel": "T1 · Stufe 5",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "t1-4"
   ],
   "ergebnis": "Platzhalter – Details folgen.",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": null,
   "zeitraum": null
  },
  {
   "id": "t2-1-brainstorming",
   "strang": "t2",
   "meilenstein": "m1",
   "titel": "Brainstorming Zukunftskompetenzen",
   "beschreibung": "Brainstorming zu Zukunftskompetenzen und zum Lernen der Zukunft.",
   "status": "offen",
   "braucht": [],
   "ergebnis": "",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": "2026-11",
   "zeitraum": null
  },
  {
   "id": "t2-2-produkte",
   "strang": "t2",
   "meilenstein": "m2",
   "titel": "Produkte und Leistungssystem",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "t2-1-brainstorming"
   ],
   "ergebnis": "",
   "details": [
    "Gesamtbild",
    "Produkte – Beispiele: aktive Kompetenzentwicklung, systematische Beratung",
    "Konzept für die aktive Kompetenzentwicklung entwickeln"
   ],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": null,
   "zeitraum": null
  },
  {
   "id": "t2-2-lernen",
   "strang": "t2",
   "meilenstein": "m2",
   "titel": "Lernen der Zukunft: Tools, Formate und Medien",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "t2-1-brainstorming"
   ],
   "ergebnis": "",
   "details": [
    "Laufend sichten, testen und bereitstellen",
    "Egal ob Videos, Podcasts, automatisierte Präsentationserstellung usw."
   ],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": null,
   "zeitraum": null
  },
  {
   "id": "t2-2-brainstorming",
   "strang": "t2",
   "meilenstein": "m2",
   "titel": "Brainstorming zu den drei Ebenen und zur Rolle Trainer der Zukunft",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "t2-2-produkte",
    "t2-2-lernen"
   ],
   "ergebnis": "",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": null,
   "zeitraum": null
  },
  {
   "id": "t2-3",
   "strang": "t2",
   "meilenstein": "m3",
   "titel": "T2 · Stufe 3",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "m2"
   ],
   "ergebnis": "Platzhalter – Details folgen.",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": null,
   "zeitraum": null
  },
  {
   "id": "t2-4",
   "strang": "t2",
   "meilenstein": "m4",
   "titel": "T2 · Stufe 4",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "t2-3"
   ],
   "ergebnis": "Platzhalter – Details folgen.",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": null,
   "zeitraum": null
  },
  {
   "id": "t2-5",
   "strang": "t2",
   "meilenstein": "m5",
   "titel": "T2 · Stufe 5",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "t2-4"
   ],
   "ergebnis": "Platzhalter – Details folgen.",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": null,
   "zeitraum": null
  },
  {
   "id": "sa-1-team",
   "strang": "sa",
   "meilenstein": "m1",
   "titel": "Team abholen",
   "beschreibung": null,
   "status": "aktiv",
   "braucht": [],
   "ergebnis": "",
   "details": [],
   "wer": "GLs",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": "2026-09",
   "zeitraum": null
  },
  {
   "id": "sa-1-hal",
   "strang": "sa",
   "meilenstein": "m1",
   "titel": "Abstimmung HAL M.S.",
   "beschreibung": null,
   "status": "aktiv",
   "braucht": [
    "sa-1-team"
   ],
   "ergebnis": "",
   "details": [],
   "wer": "AL",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": "2026-10",
   "zeitraum": null
  },
  {
   "id": "sa-1-pw7",
   "strang": "sa",
   "meilenstein": "m1",
   "titel": "PW7-Radio",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "sa-1-hal"
   ],
   "ergebnis": "",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": "2026-10",
   "zeitraum": null
  },
  {
   "id": "sa-1-puls",
   "strang": "sa",
   "meilenstein": "m1",
   "titel": "SV-Pulskanal",
   "beschreibung": null,
   "status": "offen",
   "braucht": [],
   "ergebnis": "",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": "2026-10",
   "zeitraum": null
  },
  {
   "id": "sa-1-abteilung",
   "strang": "sa",
   "meilenstein": "m1",
   "titel": "Abteilungsbesprechung 11/2026",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "sa-1-pw7",
    "sa-1-puls"
   ],
   "ergebnis": "",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": "2026-11",
   "zeitraum": null
  },
  {
   "id": "sa-1-golive",
   "strang": "sa",
   "meilenstein": "m1",
   "titel": "GoLive: Schulungsinfotag Vertrieb",
   "beschreibung": "Information der Vertriebsführungskräfte zu den Schulungen 2027. Vorstellung Homepage, Quickchecks und Lea (KI-Assistent).",
   "status": "offen",
   "braucht": [
    "sa-1-abteilung",
    "t1-1-webseite"
   ],
   "ergebnis": "",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": "04.12.2026",
   "von": null,
   "monat": "2026-12",
   "zeitraum": null
  },
  {
   "id": "sa-2-kommunikation",
   "strang": "sa",
   "meilenstein": "m2",
   "titel": "Kommunikationskonzept 2.0",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "sa-1-golive"
   ],
   "ergebnis": "",
   "details": [
    "Festlegung und Analyse von Zielgruppen",
    "Kanäle, die wir nutzen wollen",
    "Community-Formate"
   ],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": null,
   "zeitraum": null
  },
  {
   "id": "sa-3",
   "strang": "sa",
   "meilenstein": "m3",
   "titel": "SA · Stufe 3",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "m2"
   ],
   "ergebnis": "Platzhalter – Details folgen.",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": null,
   "zeitraum": null
  },
  {
   "id": "sa-4",
   "strang": "sa",
   "meilenstein": "m4",
   "titel": "SA · Stufe 4",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "sa-3"
   ],
   "ergebnis": "Platzhalter – Details folgen.",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": null,
   "zeitraum": null
  },
  {
   "id": "sa-5",
   "strang": "sa",
   "meilenstein": "m5",
   "titel": "SA · Stufe 5",
   "beschreibung": null,
   "status": "offen",
   "braucht": [
    "sa-4"
   ],
   "ergebnis": "Platzhalter – Details folgen.",
   "details": [],
   "wer": "",
   "kritisch": null,
   "termin": null,
   "von": null,
   "monat": null,
   "zeitraum": null
  }
 ]
};
