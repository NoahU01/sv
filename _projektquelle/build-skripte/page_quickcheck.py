# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/ecstatic-nice-gauss/mnt/outputs/_work")
from build_common import *

# ---- Content per Situation (aus den 3 OnePager-Handouts, auf Du-Ansprache umgestellt) ----
SITUATIONS = [
    {
        "key": "budget",
        "title": "Optimale Weiterbildung",
        "frage": "Wie setzt Du Dein Weiterbildungsbudget optimal ein, um die langfristigen Ziele Deines Bereichs zu erreichen?",
        "zielgruppe_title": "Führungskräfte im Innen- und Außendienst",
        "zielgruppe_text": "Der Quick-Check richtet sich an die erste und zweite Führungsebene im Innen- und Außendienst. Er unterstützt Dich dabei, die Weiterentwicklung Deines Teams und Deiner Vertriebseinheit strategisch, strukturiert und zielorientiert zu gestalten.",
        "zielgruppe_bullets": ["Hauptabteilungsleiter:in / Vertriebsdirektor:in", "Abteilungsleiter:in / Organisationsdirektor:in"],
        "themenfokus_title": "Fehlende Transparenz über optimalen Budgeteinsatz",
        "themenfokus_text": "Du stehst vor der Aufgabe, Dein Team gezielt weiterzuentwickeln, um Bereichs- und Vertriebsziele nachhaltig zu erreichen. Gleichzeitig fehlt häufig ein transparenter Gesamtüberblick über Entwicklungsbedarf und passende Qualifizierungsmaßnahmen zur optimalen Nutzung des Weiterbildungsbudgets. Die Klärung ist oft zeitaufwendig, einzelne Seminarbuchungen erfolgen punktuell &mdash; ohne konsequente strategische Ausrichtung auf die Ziele Deines Verantwortungsbereichs.",
        "mehrwert_title": "Qualifizierung systematisch auf Zielerreichung ausrichten",
        "mehrwert_text": "Der Quick-Check unterstützt Dich dabei, Qualifizierungsmaßnahmen strukturiert und zielgerichtet auf die strategischen Ziele Deines Verantwortungsbereichs auszurichten &mdash; mit geringem Vorbereitungsaufwand:",
        "mehrwert_bullets": ["Klar formulierte Leitfragen", "Strukturierte, praxiserprobte Vorgehensweise", "Schnelle Orientierung bei Prioritäten &amp; Maßnahmen", "Transparenz über passende Entwicklungsoptionen", "Eine fundierte Entscheidungsgrundlage im Rahmen Deines Weiterbildungsbudgets"],
        "ergebnis_text": "Du weißt, welche Fähigkeiten Dein Bereich künftig wirklich braucht &mdash; und wo die entscheidenden Lücken liegen. Du kannst gezielt Entwicklungsmaßnahmen anstoßen und Dein Budget dort einsetzen, wo es den größten Nutzen für Deine Ziele bringt.",
        "sparring_minutes": 90,
        "sparring_agenda": [
            ("5'", "Einführung und Ergebnisklärung", "Wiederholung Ziel und Vorgehen, Schaffung Transparenz zum angestrebten Ergebnis."),
            ("15'", "Gemeinsames Verständnis für alle schaffen", "Kurze Besprechung aller Leitfragen und Ergebnisse, Gesamtüberblick erlangen, keine Detaildiskussionen."),
            ("5'", "Festlegung Schwerpunkt", "Eingrenzung des Themas zur vertieften Analyse."),
            ("50'", "Fokussierung auf relevante Problemstellung", "Gezielte Detaildiskussion, Ableitung Handlungsoptionen und deren Auswirkungen."),
            ("15'", "Abschluss &amp; Ergebnissicherung", "Wiederholung Gesamtüberblick, Dokumentation Ergebnis und weiteres Vorgehen."),
        ],
        "pdf_uri": ONEPAGER_BUDGET_PDF_URI,
        "pdf_filename": "SV-Akademie-OnePager-Optimale-Weiterbildung.pdf",
        "preview_uri": ONEPAGER_BUDGET_PREVIEW_URI,
    },
    {
        "key": "klaerung",
        "title": "Klärung Weiterbildungsbedarf",
        "frage": "Wie kannst Du ein noch unklares Weiterbildungs-/Weiterentwicklungsthema möglichst effizient klären?",
        "zielgruppe_title": "Führungskräfte und Personalreferent:innen",
        "zielgruppe_text": "Das Angebot richtet sich an Führungskräfte sowie an Personalreferentinnen und Personalreferenten, die ein Anliegen zu wirksamem Lernen oder persönlicher Weiterentwicklung strukturiert klären und zielgerichtet voranbringen möchten.",
        "zielgruppe_bullets": ["Hauptabteilungsleiter:in / Vertriebsdirektor:in", "Abteilungsleiter:in / Organisationsdirektor:in", "Gruppenleiter:in / LVO / Coach &amp; Multiplikator:in", "Personalreferent:in"],
        "themenfokus_title": "Fehlende Struktur &amp; Effizienz in der Klärung von Entwicklungsanliegen",
        "themenfokus_text": "Du stehst häufig vor der Herausforderung, einen Weiterbildungs- oder Entwicklungsbedarf zu erkennen und einzuordnen, ohne ihn bereits klar benennen zu können. Gleichzeitig wird die SV Akademie als zentraler Ansprechpartner genutzt, jedoch fehlt oft eine strukturierte Grundlage für die Klärung des Anliegens. Klassische Abstimmungstermine sind in solchen Fällen zeitintensiv, wenig fokussiert und führen nicht immer zu klaren, umsetzbaren Ergebnissen.",
        "mehrwert_title": "Handlungsklarheit von Beginn an, minimaler Eigenaufwand für Dich",
        "mehrwert_text": "Der strukturierte Quick-Check ermöglicht es Dir, mit minimalem Zeitaufwand Transparenz über den tatsächlichen Entwicklungsbedarf und das passende weitere Vorgehen zu gewinnen:",
        "mehrwert_bullets": ["Kompakte Vorab-Checkliste", "Klar vorbereiteter Sparringstermin mit definierter Agenda", "Professionelle Gesprächsführung"],
        "ergebnis_text": "Klarheit in vier Punkten: Alle Rahmenbedingungen sind transparent, offene Entscheidungsfragen sind identifiziert, konkrete nächste Schritte sind definiert und die Frage nach bestehendem oder individuellem Bildungsangebot ist geklärt.",
        "sparring_minutes": 60,
        "sparring_agenda": [
            ("5'", "Einführung und Ergebnisklärung", "Wiederholung Ziel und Vorgehen, Schaffung Transparenz zum angestrebten Ergebnis."),
            ("10'", "Gemeinsames Verständnis für alle schaffen", "Kurze Besprechung aller Leitfragen und Ergebnisse, Gesamtüberblick erlangen, keine Detaildiskussionen."),
            ("10'", "Festlegung Schwerpunkt", "Eingrenzung des Themas zur vertieften Analyse."),
            ("30'", "Fokussierung auf relevante Problemstellung", "Gezielte Detaildiskussion, Ableitung Handlungsoptionen und deren Auswirkungen."),
            ("5'", "Abschluss &amp; Ergebnissicherung", "Wiederholung Gesamtüberblick, Dokumentation Ergebnis und weiteres Vorgehen."),
        ],
        "pdf_uri": ONEPAGER_KLAERUNG_PDF_URI,
        "pdf_filename": "SV-Akademie-OnePager-Klaerung-Weiterbildungsbedarf.pdf",
        "preview_uri": ONEPAGER_KLAERUNG_PREVIEW_URI,
    },
    {
        "key": "aufbau",
        "title": "Aufbau Bildungsthema",
        "frage": "Wie muss Dein eigenes Schulungsthema aufgebaut sein, damit Mitarbeitende wirklich lernen und sich weiterentwickeln?",
        "zielgruppe_title": "Bereiche der SV, die eigene Schulungen umsetzen möchten",
        "zielgruppe_text": "Der Quick-Check richtet sich an Bereiche, Abteilungen und Vertriebseinheiten, die ein eigenes Schulungs- oder Weiterbildungsthema umsetzen möchten. Wir unterstützen Dich dabei, dieses Thema so zu konzipieren und umzusetzen, dass Mitarbeitende wirklich lernen und sich weiterentwickeln.",
        "zielgruppe_bullets": [],
        "themenfokus_title": "Unsicherheit bei Aufbau und Umsetzung von Schulungen",
        "themenfokus_text": "Viele Bereiche möchten ein Fachthema schulen, sind sich aber unsicher, wie sie das sinnvoll und wirksam umsetzen können. Oft stellt sich die Frage: Welche Lernform ist die richtige? Wie muss eine Schulung aufgebaut sein, damit sie nachhaltig wirkt? Soll ein externer Trainer eingesetzt werden &mdash; und worauf ist dabei zu achten? Ohne Erfahrung im Bereich Lernen und Weiterentwicklung besteht die Gefahr, dass Maßnahmen zwar durchgeführt werden, aber wenig Wirkung zeigen oder schnell verpuffen.",
        "mehrwert_title": "Wirksames Lernen statt verpuffter Maßnahmen",
        "mehrwert_text": "Dieser Quick-Check gibt Dir Sicherheit, Dein Schulungsthema von Anfang an richtig aufzusetzen. Gemeinsam schauen wir, welche Lernformate und Methoden zu Deinem Thema passen und wie Du Deine Maßnahme sinnvoll aufbaust. Du erhältst einen klaren Ablauf, Orientierung bei den nächsten Schritten und ein durchdachtes Lernkonzept &mdash; mit wenig Zeitaufwand und mit nachhaltigem Nutzen für Deine Mitarbeitenden.",
        "mehrwert_bullets": [],
        "ergebnis_text": "Dein Weiterbildungsthema ist klar konzipiert: Ziel, Zielgruppe sowie gewünschte Wirkung sind definiert, und Du hast eine konkrete Empfehlung für das passende Format. Du kannst nun fundiert entscheiden und die Umsetzung gezielt planen.",
        "sparring_minutes": 60,
        "sparring_agenda": [
            ("5'", "Einführung und Ergebnisklärung", "Wiederholung Ziel und Vorgehen, Schaffung Transparenz zum angestrebten Ergebnis."),
            ("10'", "Gemeinsames Verständnis für alle schaffen", "Kurze Besprechung aller Leitfragen und Ergebnisse, Gesamtüberblick erlangen, keine Detaildiskussionen."),
            ("10'", "Festlegung Schwerpunkt", "Eingrenzung des Themas zur vertieften Analyse."),
            ("30'", "Fokussierung auf relevante Problemstellung", "Gezielte Detaildiskussion, Ableitung Handlungsoptionen und deren Auswirkungen."),
            ("5'", "Abschluss &amp; Ergebnissicherung", "Wiederholung Gesamtüberblick, Dokumentation Ergebnis und weiteres Vorgehen."),
        ],
        "pdf_uri": ONEPAGER_AUFBAU_PDF_URI,
        "pdf_filename": "SV-Akademie-OnePager-Aufbau-Bildungsthema.pdf",
        "preview_uri": ONEPAGER_AUFBAU_PREVIEW_URI,
    },
]

# ---- Leitfragen je Situation (Du-Ansprache) ----
LEITFRAGEN = {
    "budget": [
        ("Strategischer Bezug", [
            "Wie willst/musst Du Deinen Verantwortungsbereich künftig positionieren?",
            "Welche Ziele müssen in den nächsten 12&ndash;24 Monaten unbedingt erreicht werden?",
            "Was entscheidet maßgeblich darüber, ob diese Ziele erreicht werden?",
            "Welche Veränderungen wirken aktuell oder absehbar auf Deinen Bereich? (z.&nbsp;B. Markt, Vertrieb, Kundenverhalten, Organisation)",
        ]),
        ("Zukünftige Fähigkeiten", [
            "Welche Fähigkeiten werden künftig entscheidend sein, um Deine Ziele zu erreichen?",
            "Welche Kompetenzen sind im Team heute bereits stark ausgeprägt?",
            "Wo bestehen klare Lücken?",
            "Welche Rollen verändern sich durch neue Anforderungen?",
        ]),
        ("Priorisierung", [
            "Welche drei Kompetenzen sind für Deinen Bereich am kritischsten?",
            "Welche Kompetenzen werden kurzfristig benötigt?",
            "Welche Kompetenzen sind langfristig aufzubauen?",
        ]),
        ("Rahmenbedingungen", [
            "Welches Budget steht zur Verfügung?",
            "Welchen zeitlichen Rahmen hast Du bzw. Dein Team für Weiterbildung realistisch zur Verfügung?",
        ]),
        ("Deine konkrete Erwartung an das Gespräch", [
            "Welche offenen Fragen möchtest Du in diesem Sparring klären?",
            "Welches konkrete Ergebnis erwartest Du vom Sparring?",
        ]),
    ],
    "klaerung": [
        ("Ausgangssituation", [
            "Was ist der Auslöser für das Anliegen?",
            "Worum geht es konkret?",
            "Welche Überlegungen hast Du dazu bereits angestellt?",
        ]),
        ("Zielbild", [
            "Was soll sich durch die Maßnahme konkret verändern oder verbessern?",
            "Wie zahlt das Vorhaben auf Unternehmens-, Vertriebs- oder Personalziele ein?",
        ]),
        ("Dringlichkeit und Timing", [
            "Wie dringend ist das Thema?",
            "Bis wann sollte eine Umsetzung sinnvollerweise erfolgen?",
        ]),
        ("Abstimmung und Beteiligte", [
            "Ist das Vorhaben mit der Führungsebene abgestimmt?",
            "Wer soll inhaltlich oder organisatorisch beteiligt sein?",
            "Wer soll die Maßnahme Deiner Meinung nach durchführen?",
        ]),
        ("Budget und Finanzierung", [
            "Welches Budget steht zur Verfügung?",
            "Budget des Anfragers selbst oder von PW7, oder erfolgt eine Aufteilung? (Hinweis: SB-Vereinbarung bzw. Kostenstellenbelastung.)",
        ]),
    ],
    "aufbau": [
        ("Thema und Ziel", [
            "Welches Thema soll vermittelt werden?",
            "Was ist der Hintergrund des Themas (z.&nbsp;B. gesetzliche Vorgabe, strategische Initiative, Projekt, Vertriebsimpuls)?",
            "Welches konkrete Ergebnis soll mit der Maßnahme erreicht werden?",
        ]),
        ("Zielgruppe und Umfang", [
            "An wen richtet sich die Maßnahme genau?",
            "Wie viele Personen sollen teilnehmen?",
        ]),
        ("Rahmen und Umsetzung", [
            "Bis wann soll die Maßnahme umgesetzt sein?",
            "Gibt es bereits Vorstellungen zum Format (z.&nbsp;B. Präsenz, Webinar, Selbstlernkurs)?",
            "Welches Budget steht zur Verfügung?",
        ]),
        ("Entscheidung", [
            "Wer trifft die finale Entscheidung zur Umsetzung?",
        ]),
    ],
}

# Zuständige Gruppenleiter:in je Situation (für Excel-Versand der Leitfragen-Antworten)
GRUPPENLEITER = {
    "budget": "Marie-Therese Herzig",
    "klaerung": "Marie-Therese Herzig",
    "aufbau": "Lukas Euring",
}

SITUATIONS_BY_KEY = {s["key"]: s for s in SITUATIONS}


def bullets_html(items):
    if not items:
        return ''
    return '<ul style="padding-left:20px; color:var(--dunkelgrau1); margin:14px 0 0; font-size:.9rem;">' + "".join(['<li>' + i + '</li>' for i in items]) + '</ul>'


def agenda_html(items):
    rows = []
    for time_label, title, text in items:
        rows.append('<div class="problem-row"><div class="num-badge" style="width:34px;height:34px;font-size:.72rem;">' + time_label + '</div><div><b>' + title + '</b><p class="muted small" style="margin:4px 0 0;">' + text + '</p></div></div>')
    return "".join(rows)


def leitfragen_fields_html(key, groups):
    parts = []
    counter = 0
    for title, qs in groups:
        q_html = []
        for q in qs:
            fid = "lf_" + key + "_" + str(counter)
            counter += 1
            q_html.append('<div class="form-field"><label for="' + fid + '">' + q + '</label><textarea id="' + fid + '" class="leitfrage-input" rows="2" style="resize:vertical;"></textarea></div>')
        parts.append('<div style="margin-bottom:26px;"><h4 style="margin-bottom:12px;">' + title + '</h4>' + "".join(q_html) + '</div>')
    return "".join(parts)


# =====================================================================
# 1) quickcheck.html — schlanke Auswahlseite (gleicher Look wie KI-Lernassistent)
# =====================================================================

QC_SELECT_CARDS = "\n".join([
    '''      <a href="quickcheck-''' + s["key"] + '''.html" class="choice-card">
        <h3>''' + s["title"] + '''</h3>
        <p class="muted small">''' + s["frage"] + '''</p>
        <span class="card-more-link">Quick-Check starten &rarr;</span>
      </a>'''
    for s in SITUATIONS
])

QC_SELECT_BODY = '''
<div style="background: linear-gradient(180deg, var(--rot) 0%, #6a1f66 42%, var(--dunkelgrau2) 100%);">
  <section class="page-hero" style="background:transparent; text-align:center; padding:90px 0 90px;">
    <div class="wrap" style="max-width:700px;">
      <div class="eyebrow eyebrow-white" style="justify-content:center; display:flex;">Kurz und knapp: In vier Schritten zur Klarheit</div>
      <h1>Quick-Check Bedarfsklärung</h1>
      <p style="margin:16px 0 0;"><span class="pill pill-red">Nur für Führungskräfte</span></p>
      <p class="lead" style="opacity:.9; max-width:600px; margin:16px auto 0;">Die Beantwortung der Leitfragen dauert ca. 20 Minuten und ist die professionelle Vorarbeit für ein zielgerichtetes Sparringsgespräch mit der SV Akademie.</p>
    </div>
  </section>

  <section class="section" style="padding:0 0 130px;">
    <div class="wrap">
      <h2 style="color:#fff; text-align:center; margin-bottom:32px;">Welche Situation trifft auf Dich zu?</h2>
      <div class="grid grid-3">
''' + QC_SELECT_CARDS + '''
      </div>
    </div>
  </section>
</div>
'''

html_select = page_shell(
    "Quick-Check Bedarfsklärung — SV Akademie",
    "Wähle Deine Situation und starte direkt den passenden Quick-Check: in ca. 20 Minuten die professionelle Vorarbeit für Dein Sparringsgespräch mit der SV Akademie.",
    "quickcheck.html",
    QC_SELECT_BODY,
)
with open(os.path.join(SITEDIR, "quickcheck.html"), "w", encoding="utf-8") as f:
    f.write(html_select)
print("quickcheck.html written:", len(html_select), "chars")


# =====================================================================
# 2) Drei eigenständige Landingpages je Situation
# =====================================================================

def build_situation_page(s):
    zg_bul = bullets_html(s["zielgruppe_bullets"])
    mw_bul = bullets_html(s["mehrwert_bullets"])
    agenda = agenda_html(s["sparring_agenda"])
    modal_id = "pdfModal_" + s["key"]
    open_onclick = "openModal(" + repr(modal_id) + ")"
    close_onclick = "closeModal(" + repr(modal_id) + ")"
    download_onclick = "downloadDataUri(" + repr(s["pdf_uri"]) + ", " + repr(s["pdf_filename"]) + ")"
    lf_fields = leitfragen_fields_html(s["key"], LEITFRAGEN[s["key"]])
    gruppenleiter = GRUPPENLEITER[s["key"]]

    body = '''
<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow eyebrow-white">Quick-Check Bedarfsklärung</div>
    <h1>''' + s["title"] + '''</h1>
    <p class="lead" style="opacity:.9; max-width:680px;">''' + s["frage"] + '''</p>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid grid-3" style="align-items:stretch;">
      <div class="card">
        <div class="step-tag"><span class="step-num">1</span>Zielgruppe</div>
        <h3>''' + s["zielgruppe_title"] + '''</h3>
        <p class="muted small">''' + s["zielgruppe_text"] + '''</p>
        ''' + zg_bul + '''
      </div>
      <div class="card">
        <div class="step-tag"><span class="step-num">2</span>Themenfokus</div>
        <h3>''' + s["themenfokus_title"] + '''</h3>
        <p class="muted small">''' + s["themenfokus_text"] + '''</p>
      </div>
      <div class="card">
        <div class="step-tag"><span class="step-num">3</span>Dein Mehrwert</div>
        <h3>''' + s["mehrwert_title"] + '''</h3>
        <p class="muted small">''' + s["mehrwert_text"] + '''</p>
        ''' + mw_bul + '''
      </div>
    </div>

    <div class="sparring-box" style="margin-top:34px;">
      <div class="step-tag"><span class="step-num">4</span>Das Sparringsgespräch</div>
      <h3>In ''' + str(s["sparring_minutes"]) + ''' Minuten Klarheit schaffen</h3>
      <p class="muted small" style="margin-bottom:14px;">Gemeinsam klären wir Dein Anliegen in einem strukturierten Gespräch auf Basis Deiner beantworteten Leitfragen. Du erhältst Klarheit über Deine Handlungsoptionen und das mögliche weitere Vorgehen.</p>
      ''' + agenda + '''
    </div>

    <div class="two-col" style="margin-top:24px; align-items:center;">
      <div class="card" style="height:100%;">
        <div class="step-tag"><span class="step-num">5</span>Ergebnis &amp; nächster Schritt</div>
        <p class="muted small" style="margin:0;">''' + s["ergebnis_text"] + '''</p>
      </div>
      <div class="pdf-preview-card" onclick="''' + open_onclick + '''">
        <div class="pdf-preview-thumb"><img src="''' + s["preview_uri"] + '''" alt="Vorschau OnePager ''' + s["title"] + '''" /></div>
        <div>
          <h3 style="margin-bottom:6px;">OnePager: ''' + s["title"] + '''</h3>
          <p class="muted small" style="margin-bottom:14px;">Alle Infos zu dieser Situation im Überblick.</p>
          <span class="btn btn-outline btn-sm">Vorschau ansehen &rarr;</span>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="modal-overlay" id="''' + modal_id + '''">
  <div class="modal-box pdf-modal-box">
    <button class="modal-close" onclick="''' + close_onclick + '''">&times;</button>
    <div class="pdf-modal-scroll">
      <img src="''' + s["preview_uri"] + '''" alt="Vorschau OnePager ''' + s["title"] + '''" />
    </div>
    <div class="pdf-modal-footer">
      <button class="btn btn-primary" onclick="''' + download_onclick + '''">Als PDF herunterladen</button>
    </div>
  </div>
</div>

<section class="section bg-grau">
  <div class="wrap">
    <div class="eyebrow">Deine Vorbereitung</div>
    <h2>Deine Leitfragen zur Vorbereitung</h2>
    <p class="muted" style="max-width:640px;">Folgende kompakte Leitfragen bereiten Dich auf das Sparringsgespräch vor. Beantworte sie direkt hier &mdash; gerne auch im Führungsteam.</p>
    <div class="card" style="margin-top:24px;">
      ''' + lf_fields + '''
    </div>

    <div class="card" style="margin-top:20px;" id="leitfragenSubmitCard">
      <div class="form-check">
        <input type="checkbox" id="copyEmailCheck" />
        <label for="copyEmailCheck">Ich möchte zusätzlich eine Kopie meiner Antworten per E-Mail erhalten.</label>
      </div>
      <div class="form-field" id="copyEmailField" style="display:none; margin-top:16px; max-width:360px;">
        <label>Deine E-Mail-Adresse</label>
        <input type="email" id="copyEmailInput" placeholder="name@sv.de" />
      </div>
      <button type="button" class="btn btn-primary" id="submitLeitfragenBtn" style="margin-top:20px;" disabled>Antworten abschließen &amp; übermitteln</button>
      <p class="small muted" id="leitfragenHint" style="margin-top:10px; margin-bottom:0;">Bitte fülle zunächst alle Leitfragen aus.</p>
    </div>

    <div class="card" id="leitfragenConfirmBox" style="display:none; margin-top:20px; background:#E1F5EC; border-color:#B9E4CE;">
      <p class="muted" id="leitfragenConfirmText" style="margin:0 0 16px;"></p>
      <button type="button" class="btn btn-outline btn-sm" id="downloadCsvBtn">Antworten als CSV herunterladen</button>
    </div>
  </div>
</section>

<section class="section" id="booking">
  <div class="wrap">
    <div class="eyebrow">Letzter Schritt</div>
    <h2>Termin auswählen &amp; buchen</h2>
    <div class="two-col" style="align-items:flex-start; margin-top:24px;">
      <div class="card">
        <h3>Verfügbare Termine</h3>
        <p class="muted small">Alle Termine als Videocall, ca. 20 Minuten.</p>
        <div class="slot-grid" id="slotGrid">
          <button type="button" class="slot-btn">Mo 10.08. &middot; 09:00</button>
          <button type="button" class="slot-btn">Mo 10.08. &middot; 14:00</button>
          <button type="button" class="slot-btn">Di 11.08. &middot; 11:00</button>
          <button type="button" class="slot-btn">Mi 12.08. &middot; 09:30</button>
          <button type="button" class="slot-btn">Mi 12.08. &middot; 15:00</button>
          <button type="button" class="slot-btn">Do 13.08. &middot; 10:00</button>
        </div>
      </div>
      <div class="card">
        <h3>Deine Angaben</h3>
        <form id="quickcheckForm">
          <div class="form-row">
            <div class="form-field"><label>Vorname</label><input type="text" required /></div>
            <div class="form-field"><label>Nachname</label><input type="text" required /></div>
          </div>
          <div class="form-field"><label>E-Mail</label><input type="email" required /></div>
          <button type="submit" class="btn btn-primary btn-block" id="quickcheckSubmit" disabled>Termin verbindlich buchen</button>
          <p class="small muted" id="submitHint" style="margin-top:10px;">Bitte schließe zuerst Deine Leitfragen oben ab.</p>
        </form>
      </div>
    </div>
  </div>
</section>

<div class="modal-overlay" id="quickcheckModal">
  <div class="modal-box">
    <button class="modal-close" onclick="closeModal('quickcheckModal')">&times;</button>
    <div class="modal-icon">&#10003;</div>
    <h3>Dein Quick-Check ist gebucht!</h3>
    <p class="muted">Du erhältst in Kürze eine Bestätigung per E-Mail. Lade Dir gerne schon jetzt den OnePager zu Deiner Situation herunter oder speichere den Termin direkt in Deinem Kalender.</p>
    <a href="''' + s["pdf_uri"] + '''" download="''' + s["pdf_filename"] + '''" class="btn btn-outline btn-block" style="margin-bottom:10px;">OnePager herunterladen (PDF)</a>
    <button class="btn btn-primary btn-block" onclick="downloadQuickcheckIcs()">Termin in Kalender speichern</button>
  </div>
</div>
'''

    extra_js = '''
var leitfragenSubmitted = false;
var leitfragenCsvUrl = null;
var selectedSlot = null;
var GRUPPENLEITER_NAME = ''' + repr(gruppenleiter) + ''';

function updateLeitfragenSubmitState(){
  if (leitfragenSubmitted) return;
  var inputs = document.querySelectorAll(".leitfrage-input");
  var allFilled = inputs.length > 0 && Array.prototype.every.call(inputs, function(t){ return t.value.trim().length > 0; });
  var copyChecked = document.getElementById("copyEmailCheck").checked;
  var emailVal = document.getElementById("copyEmailInput").value.trim();
  var emailOk = !copyChecked || /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(emailVal);
  var btn = document.getElementById("submitLeitfragenBtn");
  var hint = document.getElementById("leitfragenHint");
  btn.disabled = !(allFilled && emailOk);
  if (!allFilled) {
    hint.textContent = "Bitte fülle zunächst alle Leitfragen aus.";
  } else if (!emailOk) {
    hint.textContent = "Bitte gib eine gültige E-Mail-Adresse an.";
  } else {
    hint.textContent = "";
  }
}
document.querySelectorAll(".leitfrage-input").forEach(function(t){
  t.addEventListener("input", updateLeitfragenSubmitState);
});
document.getElementById("copyEmailCheck").addEventListener("change", function(){
  document.getElementById("copyEmailField").style.display = this.checked ? "block" : "none";
  updateLeitfragenSubmitState();
});
document.getElementById("copyEmailInput").addEventListener("input", updateLeitfragenSubmitState);

document.getElementById("submitLeitfragenBtn").addEventListener("click", function(){
  var inputs = document.querySelectorAll(".leitfrage-input");
  var rows = [["Frage","Antwort"]];
  inputs.forEach(function(t){
    var label = document.querySelector("label[for=\\"" + t.id + "\\"]");
    rows.push([label ? label.textContent : t.id, t.value]);
  });
  function csvEscape(v){
    return "\\"" + String(v).replace(/"/g, "\\"\\"") + "\\"";
  }
  var csv = "\\uFEFF" + rows.map(function(r){ return r.map(csvEscape).join(";"); }).join("\\r\\n");
  var blob = new Blob([csv], { type: "text/csv;charset=utf-8" });
  leitfragenCsvUrl = URL.createObjectURL(blob);

  var msg = "Deine Antworten wurden an " + GRUPPENLEITER_NAME + " übermittelt.";
  if (document.getElementById("copyEmailCheck").checked) {
    msg += " Eine Kopie wurde an " + document.getElementById("copyEmailInput").value.trim() + " gesendet.";
  }
  document.getElementById("leitfragenConfirmText").textContent = msg;
  document.getElementById("leitfragenConfirmBox").style.display = "block";

  leitfragenSubmitted = true;
  this.disabled = true;
  updateSubmitState();
});

document.getElementById("downloadCsvBtn").addEventListener("click", function(){
  if (!leitfragenCsvUrl) return;
  downloadDataUri(leitfragenCsvUrl, "sv-akademie-quick-check-leitfragen-''' + s["key"] + '''.csv");
});

document.querySelectorAll(".slot-btn").forEach(function(btn){
  btn.addEventListener("click", function(){
    document.querySelectorAll(".slot-btn").forEach(function(b){ b.classList.remove("selected"); });
    btn.classList.add("selected");
    selectedSlot = btn.textContent;
    updateSubmitState();
  });
});

function updateSubmitState(){
  var submitBtn = document.getElementById("quickcheckSubmit");
  var hint = document.getElementById("submitHint");
  if (!leitfragenSubmitted) {
    submitBtn.disabled = true;
    hint.textContent = "Bitte schließe zuerst Deine Leitfragen oben ab.";
  } else if (!selectedSlot) {
    submitBtn.disabled = true;
    hint.textContent = "Bitte wähle zunächst einen Termin aus.";
  } else {
    submitBtn.disabled = false;
    hint.textContent = "Ausgewählt: " + selectedSlot;
  }
}
updateSubmitState();

document.getElementById("quickcheckForm").addEventListener("submit", function(e){
  e.preventDefault();
  if (!selectedSlot || !leitfragenSubmitted) return;
  openModal("quickcheckModal");
});

function downloadQuickcheckIcs(){
  var d = new Date();
  d.setDate(d.getDate() + 3);
  d.setHours(10,0,0,0);
  downloadIcs({
    title: "SV Akademie: Quick-Check ''' + s["title"] + '''",
    description: "Dein Quick-Check Termin mit der SV Akademie (ca. 20 Minuten, Videocall).",
    location: "Online (Videocall)",
    start: d,
    durationMinutes: 20,
    filename: "sv-akademie-quick-check-''' + s["key"] + '''"
  });
}
'''

    filename = "quickcheck-" + s["key"] + ".html"
    html = page_shell(
        s["title"] + " — Quick-Check Bedarfsklärung — SV Akademie",
        s["frage"],
        filename,
        body,
        extra_js=extra_js,
        header_override=minimal_header_html(),
    )
    with open(os.path.join(SITEDIR, filename), "w", encoding="utf-8") as f:
        f.write(html)
    print(filename, "written:", len(html), "chars")


for s in SITUATIONS:
    build_situation_page(s)
