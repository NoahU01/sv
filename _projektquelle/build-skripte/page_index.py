# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_common import *
from illustrations import (illustration_quickcheck_flat,
                            illustration_portal_flat, illustration_community_flat)

with open(os.path.join(WORKDIR, "kreislauf_inline.svg"), encoding="utf-8") as _f:
    KREISLAUF_SVG_INLINE = _f.read()

# ---- Custom line icons (Streamline-Ultimate-Stil, monochrome, currentColor) ----
ICON_TEMPO = '''<svg viewBox="0 0 250 250" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="10"><path d="M30 210h190"/><path d="M30 210V40"/><path d="M50 172l50-50 40 30 78-78"/><path d="M183 44h35v35"/></g></svg>'''

ICON_VERTRAUEN = '''<svg viewBox="0 0 250 250" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="10"><path d="M35 45h180a20 20 0 0 1 20 20v110a20 20 0 0 1 -20 20h-90l-45 40v-40H35a20 20 0 0 1 -20 -20V65a20 20 0 0 1 20 -20Z"/><path d="M125 152c-38-24-38-58-11-58 13 0 11 13 11 13s-2-13 11-13c27 0 27 34-11 58Z"/></g></svg>'''

ICON_FUEHRUNG = '''<svg viewBox="0 0 250 250" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="10"><circle cx="125" cy="125" r="100"/><path d="M160 90l-25 55-55 25 25-55 55-25Z"/></g></svg>'''

# ---- Hochgeladene Icons (1.svg/2.svg/3.svg) fuer die Section "Genau hierfuer gibt es die SV Akademie" ----
ICON_UPLOAD_1 = '''<svg viewBox="-25 -25 800 800" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="50"><path d="m305.46875000000006 386.50000000000006 -130.3125 65.46875000000001a61.65625000000001 61.65625000000001 0 0 1 -82.8125 -27.437500000000004h0a61.65625000000001 61.65625000000001 0 0 1 27.437500000000004 -82.8125l192.93750000000003 -96.87500000000001 36.96875000000001 73.59375000000001"/><path d="M326.5625 272.31250000000006a61.65625000000001 61.65625000000001 0 0 1 27.406250000000004 -82.8125l192.96875000000003 -96.87500000000001 83.09375 165.375 -159.75000000000003 80.25000000000001"/><path d="m23.437500000000004 459.18750000000006 68.90625000000001 -34.65625"/><path d="M588.1838392906251 37.25212103437501 615.7435989625001 23.403057500000003l0 0 110.84863418437502 220.58976840625002 0 0 -27.559759671875003 13.849063531250001a61.68750000000001 61.68750000000001 0 0 1 -82.81764641875002 -27.421392268750004l-55.438348565625006 -110.32280695937501a61.68750000000001 61.68750000000001 0 0 1 27.407360800000003 -82.84556917500001Z"/><path d="M482.18750000000006 356.25000000000006a93.75000000000001 93.75000000000001 0 1 1 -125.93750000000003 -41.56250000000001 93.75000000000001 93.75000000000001 0 0 1 125.93750000000003 41.56250000000001Z"/><path d="m398.43750000000006 492.18750000000006 0 234.37500000000003"/><path d="m187.50000000000003 726.5625000000001 143.46875000000003 -263.03125"/><path d="m609.3750000000001 726.5625000000001 -143.46875000000003 -263.03125"/></g></svg>'''

ICON_UPLOAD_2 = '''<svg viewBox="-25 -25 800 800" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="50"><path d="M672.9156250000001 581.2500000000001H352.084375L168.75000000000003 718.7500000000001v-137.50000000000003H77.08343750000002C52.63875 581.2500000000001 31.250000000000004 559.8625000000001 31.250000000000004 535.415625V77.08343750000002C31.250000000000004 52.63875 52.63875 31.250000000000004 77.08343750000002 31.250000000000004H672.9156250000001C697.3625000000001 31.250000000000004 718.7500000000001 52.63875 718.7500000000001 77.08343750000002V535.415625c0 24.446875000000002 -21.387500000000003 45.834375 -45.834375 45.834375Z"/><path d="M398.51875 441.3531250000001c-11.93125 12.90625 -32.265625 13.109375000000002 -44.45312500000001 0.4437500000000001L220.69562500000004 303.19468750000004c-27.500000000000004 -27.500000000000004 -33.611250000000005 -70.2778125 -18.333437500000002 -106.94468750000001 27.500000000000004 -55.00000000000001 103.88843750000001 -67.2221875 146.6659375 -24.444375000000004l24.44375 24.444375000000004 24.446875000000002 -24.444375000000004C443.75 125.9725 517.0843750000001 138.19468750000001 544.584375 196.25000000000003c18.33125 36.666875000000005 12.221875 79.44468750000001 -18.334375 106.94468750000001l-127.73125 138.15843750000002Z"/></g></svg>'''

ICON_UPLOAD_3 = '''<svg viewBox="-25 -25 800 800" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="50"><path d="M373.4375 331.25 23.437500000000004 200.00031250000004l350 -134.37468750000002 353.12500000000006 134.37468750000002L373.4375 331.25Z"/><path d="M585.9375000000001 253.12562500000004V421.87500000000006c-140.62500000000003 87.5 -281.25000000000006 87.5 -421.87500000000006 0V253.12562500000004"/><path d="M79.68718750000002 221.875625V509.37500000000006"/><path d="M135.9375 565.6250000000001c0 -31.250000000000004 -25.000000000000004 -56.25000000000001 -56.25000000000001 -56.25000000000001s-56.25000000000001 25.000000000000004 -56.25000000000001 56.25000000000001v118.75000000000001h112.50000000000001v-118.75000000000001Z"/></g></svg>'''

HERO = '''
<section class="hero">
  <div class="wrap">
    <div>
      <div class="eyebrow eyebrow-white"><span></span>Für Führungskräfte, Mitarbeitende &amp; Vertriebspartner der SV</div>
      <h1>Wir sind Dein Ansprechpartner für Bildung und Weiterentwicklung.</h1>
      <p class="lead">Wir begleiten Dich aktiv und persönlich in Deiner beruflichen und persönlichen Entwicklung. Kein Suchen, kein Rätselraten &mdash; wir finden gemeinsam mit Dir, was Dich wirklich weiterbringt.</p>
      <div class="hero-ctas">
        <a href="quickcheck.html" class="btn btn-ghost">Quick-Check starten</a>
        <a href="portal.html" class="btn btn-outline">KI-Lernassistent entdecken &rarr;</a>
      </div>
    </div>
    <div class="hero-visual">
      <img src="''' + ROCKET_URI + '''" alt="SV Akademie Rakete" />
    </div>
  </div>
</section>
'''

TRUSTBAR = '''
<section class="trust-bar">
  <div class="wrap">
    <div class="trust-stat">
      <b>ca. 5.000</b>
      <span>Mitarbeitende im Innen- und Außendienst der SV</span>
    </div>
    <div class="trust-stat">
      <b>ca. 25.000</b>
      <span>Marktmitarbeitende unserer Sparkassen</span>
    </div>
    <div class="trust-stat">
      <b>&uuml;ber 100.000</b>
      <span>bereits abgeschlossene Selbstlernkurse</span>
    </div>
  </div>
</section>
'''

PROBLEM = '''
<section class="section" id="problem">
  <div class="wrap">
    <div class="eyebrow">Unsere grundlegenden Annahmen zur Zukunft</div>
    <h2>Genau hierfür gibt es die SV Akademie</h2>
    <p class="muted" style="max-width:900px; font-size:1.05rem;">Die Zielbilder und Entwicklungsbedarfe im Innen- und Außendienst verändern sich mit zunehmender Geschwindigkeit. Damit Du und Dein Team fit für die Zukunft bleiben, braucht es echte Begleitung in der beruflichen und persönlichen Entwicklung &mdash; keine Weiterbildung von der Stange.</p>

    <div class="grid grid-3" style="margin-top:40px;">
      <div class="card reveal problem-card">
        <div class="icon-badge-circle">''' + ICON_UPLOAD_1 + '''</div>
        <h3>Zukunftskompetenzen</h3>
        <p class="muted small">Die Personalstrategie macht sichtbar, welche Kompetenzen für die SV-Strategie künftig entscheidend sind.</p>
        <button type="button" class="card-more-link" onclick="openModal('problemModal1')">Mehr anzeigen &rarr;</button>
      </div>
      <div class="card reveal problem-card">
        <div class="icon-badge-circle">''' + ICON_UPLOAD_2 + '''</div>
        <h3>USP Menschlichkeit</h3>
        <p class="muted small">Im KI-Zeitalter werden Beziehungen und menschliche Nähe noch wichtiger.</p>
        <button type="button" class="card-more-link" onclick="openModal('problemModal3')">Mehr anzeigen &rarr;</button>
      </div>
      <div class="card reveal problem-card">
        <div class="icon-badge-circle">''' + ICON_UPLOAD_3 + '''</div>
        <h3>Lernen der Zukunft</h3>
        <p class="muted small">Lernen wird zunehmend individueller &mdash; wir begleiten Dich dabei persönlich.</p>
        <button type="button" class="card-more-link" onclick="openModal('problemModal4')">Mehr anzeigen &rarr;</button>
      </div>
    </div>
  </div>
</section>

<div class="modal-overlay" id="problemModal1">
  <div class="modal-box" style="max-width:520px; text-align:left;">
    <button class="modal-close" onclick="closeModal('problemModal1')">&times;</button>
    <div class="icon-badge-circle" style="margin:0 auto 20px;">''' + ICON_UPLOAD_1 + '''</div>
    <h3 style="text-align:center; margin-bottom:16px;">Zukunftskompetenzen</h3>
    <p class="muted">Die Personalstrategie fokussiert auf die Zukunftskompetenzen, die für die erfolgreiche und wirksame Umsetzung der SV-Strategie besonders relevant sind.</p>
    <p class="muted" style="margin-top:14px;">Mitarbeitende und Vertriebspartner benötigen Begleitung in ihrer beruflichen und persönlichen Entwicklung, um fit für die Zukunft zu bleiben.</p>
  </div>
</div>

<div class="modal-overlay" id="problemModal3">
  <div class="modal-box" style="max-width:520px; text-align:left;">
    <button class="modal-close" onclick="closeModal('problemModal3')">&times;</button>
    <div class="icon-badge-circle" style="margin:0 auto 20px;">''' + ICON_UPLOAD_2 + '''</div>
    <h3 style="text-align:center; margin-bottom:16px;">USP Menschlichkeit</h3>
    <p class="muted">Die KI wird einen Großteil der Prozesse im Innen- und Außendienst tiefgreifend ändern. Beziehungen, Vertrauen und menschliche Nähe werden immer wichtiger &mdash; nicht unwichtiger.</p>
    <p class="muted" style="margin-top:14px;">Die SV muss schneller reagieren, um genau darin wettbewerbsfähig zu bleiben.</p>
  </div>
</div>

<div class="modal-overlay" id="problemModal4">
  <div class="modal-box" style="max-width:520px; text-align:left;">
    <button class="modal-close" onclick="closeModal('problemModal4')">&times;</button>
    <div class="icon-badge-circle" style="margin:0 auto 20px;">''' + ICON_UPLOAD_3 + '''</div>
    <h3 style="text-align:center; margin-bottom:16px;">Lernen der Zukunft</h3>
    <p class="muted">Das Lernen wird deutlich individualisierter ablaufen &ndash; auch durch den Einsatz digitaler, KI-gestützter Tools. Umso mehr fokussieren wir auf die Begleitung durch echte Menschen.</p>
  </div>
</div>
'''

LOESUNG = '''
<section class="section" id="loesung" style="padding-bottom:0;">
  <div class="wrap">
    <div class="eyebrow">Zukunft sichern</div>
    <h2>Aktive Kompetenzentwicklung statt Warten auf Anfragen.</h2>
    <p style="max-width:720px; font-size:1.08rem;">Wir behalten die zukünftig notwendigen Skills stets im Blick, schaffen dafür professionelle Weiterbildungsbedingungen und überführen sie in eine passgenaue, KI-gestützte Lernarchitektur.</p>

    <div class="cycle-diagram reveal" style="text-align:center; margin-top:20px; padding:30px 10px 0;">
      ''' + KREISLAUF_SVG_INLINE + '''
    </div>
  </div>
</section>
'''

ZUSAMMENARBEIT = '''
<section class="section bg-grau" id="zusammenarbeit" style="--tl-cols:3;">
  <div class="wrap">
    <div class="eyebrow">Klarheit im Vorgehen</div>
    <h2>So läuft die Zusammenarbeit ab.</h2>
    <p class="muted" style="max-width:760px; font-size:1.05rem;">Vom Eintritt in die SV an begleiten wir Führungskräfte, Mitarbeitende und Vertriebspartner in ihrer beruflichen und persönlichen Entwicklung und machen sie fit für morgen. Dabei steht bei uns der Mensch im Fokus &mdash; der USP Mensch.</p>

    <div class="grid grid-3" style="margin-top:40px; align-items:stretch;">
      <div class="card lead-card reveal" style="position:relative;">
        <span class="pill pill-red" style="position:absolute; top:18px; left:18px; z-index:2; box-shadow:0 4px 10px rgba(0,0,0,.1);">Nur für Führungskräfte</span>
        <div class="illus-box">''' + illustration_quickcheck_flat() + '''</div>
        <div class="step-tag"><span class="step-num">1</span>Bedarf klären</div>
        <h3>Quick-Check Bedarfsklärung</h3>
        <p class="muted">Egal ob Dein Bedarf schon klar ist oder erst strukturiert werden muss: Beantworte wenige Leitfragen, buche direkt einen Termin &mdash; und Du bekommst Klarheit.</p>
        <a href="quickcheck.html" class="btn btn-outline btn-block">Quick-Check buchen</a>
      </div>
      <div class="card lead-card reveal">
        <div class="illus-box">''' + illustration_portal_flat() + '''</div>
        <div class="step-tag"><span class="step-num">2</span>Organisieren &amp; selbst loslegen</div>
        <h3>KI-Lernassistent</h3>
        <p class="muted">Dein jederzeit erreichbarer Zugang zu unseren Weiterbildungsangeboten. Du musst nicht suchen &mdash; unser KI-Assistent macht Dir zielgenaue Vorschläge und hilft Dir direkt weiter.</p>
        <a href="portal.html" class="btn btn-primary btn-block">KI-Lernassistent entdecken</a>
      </div>
      <div class="card lead-card reveal">
        <div class="illus-box">''' + illustration_community_flat() + '''</div>
        <div class="step-tag"><span class="step-num">3</span>Im Austausch bleiben</div>
        <h3>Community-Austausch</h3>
        <p class="muted">Wir wollen mit Dir in Kontakt bleiben &mdash; mit Energie, nützlichem Input und Austausch von Mensch zu Mensch. Sichere Dir Deinen Platz beim nächsten digitalen Community-Austausch.</p>
        <a href="community.html" class="btn btn-outline btn-block">Termin sichern</a>
      </div>
    </div>
  </div>
</section>
'''

FAQ_ITEMS = [
    ("Wer kann die Angebote der SV Akademie nutzen?",
     "Alle Mitarbeitenden und Vertriebspartner der SV im Rahmen ihrer Tätigkeit &mdash; unabhängig davon, ob Du neu einsteigst oder Dich gezielt weiterentwickeln möchtest."),
    ("Was kostet die Teilnahme?",
     "Unsere Beratungen und unsere Community sind grundsätzlich kostenfrei, und wir freuen uns über jeden, der diese Angebote nutzt.<br/><br/>"
     "Die Kosten einer bereits geplanten Weiterbildungsmaßnahme sind im KI-Lernassistenten dargestellt. Individuelle Maßnahmen stimmen wir gezielt mit Dir ab.<br/><br/>"
     "Oftmals gibt es aber auch Möglichkeiten, die Dein Weiterbildungsbudget nicht belasten &mdash; sprich uns gerne darauf an!"),
    ("Wie läuft der Quick-Check ab?",
     "Du bist Führungskraft und hast Klärungsbedarf im Bereich Weiterbildung? Dann bist Du hier genau richtig.<br/><br/>"
     "Egal, ob Dein Bedarf bereits klar ist, dieser noch strukturiert werden muss oder Du wissen willst, wie Du Dein Weiterbildungsbudget optimal einsetzen kannst: Beantworte wenige Leitfragen, buche direkt anschließend einen passenden Termin und Du bekommst Klarheit."),
    ("Was ist der KI-Lernassistent?",
     "Dein jederzeit erreichbarer Zugang zu unseren Weiterbildungsangeboten.<br/><br/>"
     "Probiere es direkt aus: Du musst nicht nach den passenden Trainings suchen, der KI-Assistent übernimmt die Suche und macht Dir zielgenaue Vorschläge &mdash; bis hin zu ineinander stimmigen Trainingskombinationen."),
    ("Was ist der Community-Austausch und wie melde ich mich an?",
     "Wir wollen mit Dir in Kontakt bleiben. Mit viel Energie, nützlichem Input und vor allem Austausch von Mensch zu Mensch.<br/><br/>"
     "Die Community der SV Akademie findet regelmäßig online statt, und wir freuen uns bereits jetzt auf Dich!<br/><br/>"
     "Anmeldung über die Buchungsseite zum Community-Austausch: Termin auswählen, kurz anmelden, fertig &mdash; inklusive Erinnerung für Deinen Kalender."),
]

faq_html = []
for i, (q, a) in enumerate(FAQ_ITEMS):
    faq_html.append('''
      <div class="accordion-item''' + (' open' if i == 0 else '') + '''">
        <button class="accordion-trigger">''' + q + '''<span class="accordion-plus">+</span></button>
        <div class="accordion-panel" style="''' + ('max-height:500px;' if i == 0 else '') + '''">
          <div class="accordion-panel-inner">''' + a + '''</div>
        </div>
      </div>''')

FAQ = '''
<section class="section" id="faq">
  <div class="wrap" style="max-width:820px;">
    <div class="eyebrow">Kurz &amp; knapp</div>
    <h2>Häufige Fragen</h2>
    <div class="accordion" style="margin-top:20px;">
      ''' + "\n".join(faq_html) + '''
    </div>
  </div>
</section>
'''

KONTAKT = '''
<section class="section bg-dunkel" id="kontakt">
  <div class="wrap">
    <div class="two-col" style="align-items:center;">
      <div class="reveal">
        <div class="eyebrow">Jetzt loslegen</div>
        <h2>Bereit für Deinen nächsten Entwicklungsschritt?</h2>
        <p style="opacity:.85; max-width:480px;">Du musst nicht wissen, wo Du anfängst &mdash; wir finden das gemeinsam heraus. Wähl den Einstieg, der gerade zu Dir passt.</p>
      </div>
      <div class="reveal center">
        <img src="''' + ROCKET_URI + '''" alt="SV Akademie" style="max-width:150px; margin:0 auto;" />
      </div>
    </div>
    <div class="reveal" style="display:flex; gap:16px; flex-wrap:wrap; justify-content:center; margin-top:38px;">
      <a href="quickcheck.html" class="btn btn-ghost">Quick-Check starten</a>
      <a href="portal.html" class="btn btn-primary">KI-Lernassistent entdecken</a>
      <a href="community.html" class="btn btn-ghost">Community-Austausch</a>
    </div>
  </div>
</section>
'''

BODY = HERO + TRUSTBAR + PROBLEM + LOESUNG + ZUSAMMENARBEIT + FAQ + KONTAKT

html = page_shell(
    "SV Akademie — Dein Ansprechpartner für Bildung und Weiterentwicklung",
    "Die SV Akademie begleitet Führungskräfte, Mitarbeitende und Vertriebspartner der SV aktiv in ihrer beruflichen und persönlichen Entwicklung.",
    "index.html",
    BODY,
)

with open(os.path.join(SITEDIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(html)

print("index.html written:", len(html), "chars")
