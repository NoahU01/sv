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
   "verantwortung": "Lukas Euring",
   "farbe": "#EE0000"
  },
  {
   "id": "t2",
   "kurz": "T2",
   "label": "Transformation 2",
   "verantwortung": "Philip Dreyer & Stefanie Frank",
   "farbe": "#AC1033"
  },
  {
   "id": "sa",
   "kurz": "SA",
   "label": "Sichtbarkeit & Außenwirkung",
   "verantwortung": "Marie Herzig",
   "farbe": "#6A1F66"
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
    "sa-1-golive"
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
 "schritte": [
  {
   "id": "t1-1-taskforce",
   "strang": "t1",
   "meilenstein": "m1",
   "titel": "Taskforce KI: Ideen für Lea",
   "status": "offen",
   "braucht": []
  },
  {
   "id": "t1-1-lea",
   "strang": "t1",
   "meilenstein": "m1",
   "titel": "Entwicklung KI-Assistent Lea",
   "status": "offen",
   "braucht": [
    "t1-1-taskforce"
   ]
  },
  {
   "id": "t1-1-webseite",
   "strang": "t1",
   "meilenstein": "m1",
   "titel": "Webseite umsetzen und live schalten",
   "status": "offen",
   "braucht": [
    "t1-1-lea"
   ]
  },
  {
   "id": "t1-2-mak",
   "strang": "t1",
   "meilenstein": "m2",
   "titel": "MAK",
   "status": "offen",
   "braucht": [
    "t1-1-webseite"
   ]
  },
  {
   "id": "t1-2-leos",
   "strang": "t1",
   "meilenstein": "m2",
   "titel": "LEOS 2.0",
   "status": "offen",
   "braucht": [
    "t1-2-mak"
   ]
  },
  {
   "id": "t1-2-auftrag",
   "strang": "t1",
   "meilenstein": "m2",
   "titel": "Sicherstellung Auftrag Dr. Jan: „1 Akademie“",
   "status": "offen",
   "braucht": [
    "t1-2-leos"
   ]
  },
  {
   "id": "t1-3",
   "strang": "t1",
   "meilenstein": "m3",
   "titel": "T1 · Stufe 3",
   "status": "offen",
   "braucht": [
    "t1-2-auftrag"
   ]
  },
  {
   "id": "t1-4",
   "strang": "t1",
   "meilenstein": "m4",
   "titel": "T1 · Stufe 4",
   "status": "offen",
   "braucht": [
    "t1-3"
   ]
  },
  {
   "id": "t1-5",
   "strang": "t1",
   "meilenstein": "m5",
   "titel": "T1 · Stufe 5",
   "status": "offen",
   "braucht": [
    "t1-4"
   ]
  },
  {
   "id": "t2-1-brainstorming",
   "strang": "t2",
   "meilenstein": "m1",
   "titel": "Brainstorming Zukunftskompetenzen und Lernen der Zukunft",
   "status": "offen",
   "braucht": []
  },
  {
   "id": "t2-2-produkte",
   "strang": "t2",
   "meilenstein": "m2",
   "titel": "Produkte und Leistungssystem",
   "status": "offen",
   "braucht": [
    "t2-1-brainstorming"
   ]
  },
  {
   "id": "t2-2-lernen",
   "strang": "t2",
   "meilenstein": "m2",
   "titel": "Lernen der Zukunft: Tools, Formate und Medien",
   "status": "offen",
   "braucht": [
    "t2-1-brainstorming"
   ]
  },
  {
   "id": "t2-2-brainstorming",
   "strang": "t2",
   "meilenstein": "m2",
   "titel": "Brainstorming zu den drei Ebenen und zur Rolle Trainer der Zukunft",
   "status": "offen",
   "braucht": [
    "t2-2-produkte",
    "t2-2-lernen"
   ]
  },
  {
   "id": "t2-3",
   "strang": "t2",
   "meilenstein": "m3",
   "titel": "T2 · Stufe 3",
   "status": "offen",
   "braucht": [
    "t2-2-brainstorming"
   ]
  },
  {
   "id": "t2-4",
   "strang": "t2",
   "meilenstein": "m4",
   "titel": "T2 · Stufe 4",
   "status": "offen",
   "braucht": [
    "t2-3"
   ]
  },
  {
   "id": "t2-5",
   "strang": "t2",
   "meilenstein": "m5",
   "titel": "T2 · Stufe 5",
   "status": "offen",
   "braucht": [
    "t2-4"
   ]
  },
  {
   "id": "sa-1-team",
   "strang": "sa",
   "meilenstein": "m1",
   "titel": "Team abholen",
   "status": "offen",
   "braucht": []
  },
  {
   "id": "sa-1-hal",
   "strang": "sa",
   "meilenstein": "m1",
   "titel": "Abstimmung HAL M.S.",
   "status": "offen",
   "braucht": [
    "sa-1-team"
   ]
  },
  {
   "id": "sa-1-pw7",
   "strang": "sa",
   "meilenstein": "m1",
   "titel": "PW7-Radio",
   "status": "offen",
   "braucht": [
    "sa-1-hal"
   ]
  },
  {
   "id": "sa-1-puls",
   "strang": "sa",
   "meilenstein": "m1",
   "titel": "SV-Pulskanal",
   "status": "offen",
   "braucht": [
    "sa-1-hal"
   ]
  },
  {
   "id": "sa-1-abteilung",
   "strang": "sa",
   "meilenstein": "m1",
   "titel": "Abteilungsbesprechung 11/2026",
   "status": "offen",
   "braucht": [
    "sa-1-pw7",
    "sa-1-puls",
    "t1-1-webseite"
   ]
  },
  {
   "id": "sa-1-golive",
   "strang": "sa",
   "meilenstein": "m1",
   "titel": "GoLive",
   "status": "offen",
   "braucht": [
    "sa-1-abteilung"
   ]
  },
  {
   "id": "sa-2-kommunikation",
   "strang": "sa",
   "meilenstein": "m2",
   "titel": "Kommunikationskonzept 2.0",
   "status": "offen",
   "braucht": [
    "sa-1-golive"
   ]
  },
  {
   "id": "sa-3",
   "strang": "sa",
   "meilenstein": "m3",
   "titel": "SA · Stufe 3",
   "status": "offen",
   "braucht": [
    "sa-2-kommunikation"
   ]
  },
  {
   "id": "sa-4",
   "strang": "sa",
   "meilenstein": "m4",
   "titel": "SA · Stufe 4",
   "status": "offen",
   "braucht": [
    "sa-3"
   ]
  },
  {
   "id": "sa-5",
   "strang": "sa",
   "meilenstein": "m5",
   "titel": "SA · Stufe 5",
   "status": "offen",
   "braucht": [
    "sa-4"
   ]
  }
 ]
};
