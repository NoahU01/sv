# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/ecstatic-nice-gauss/mnt/outputs/_work")
from build_common import *

ICON_PERSON = '''<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="6"><circle cx="50" cy="36" r="18"/><path d="M14 92c0-22 16-38 36-38s36 16 36 38"/></g></svg>'''

LEADER_PHOTO_SVG = '''<svg viewBox="0 0 150 150" xmlns="http://www.w3.org/2000/svg"><rect width="150" height="150" fill="#E3E3E3"/><g fill="#BBBBBB"><circle cx="75" cy="58" r="30"/><path d="M15 148c0-38 27-64 60-64s60 26 60 64"/></g></svg>'''

ICON_GROWTH = '<svg viewBox="0 0 250 250" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="10"><path d="M37.5,187.5l62.5-62.5,37.5,30,75-75"/><path d="M162.5,80h50v50"/></g></svg>'

# Gleiches Icon wie "Zukunftskompetenzen" in der Startseiten-Section "Genau hierfuer gibt es die SV Akademie" (page_index.py)
ICON_UPLOAD_1 = '''<svg viewBox="-25 -25 800 800" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="50"><path d="m305.46875000000006 386.50000000000006 -130.3125 65.46875000000001a61.65625000000001 61.65625000000001 0 0 1 -82.8125 -27.437500000000004h0a61.65625000000001 61.65625000000001 0 0 1 27.437500000000004 -82.8125l192.93750000000003 -96.87500000000001 36.96875000000001 73.59375000000001"/><path d="M326.5625 272.31250000000006a61.65625000000001 61.65625000000001 0 0 1 27.406250000000004 -82.8125l192.96875000000003 -96.87500000000001 83.09375 165.375 -159.75000000000003 80.25000000000001"/><path d="m23.437500000000004 459.18750000000006 68.90625000000001 -34.65625"/><path d="M588.1838392906251 37.25212103437501 615.7435989625001 23.403057500000003l0 0 110.84863418437502 220.58976840625002 0 0 -27.559759671875003 13.849063531250001a61.68750000000001 61.68750000000001 0 0 1 -82.81764641875002 -27.421392268750004l-55.438348565625006 -110.32280695937501a61.68750000000001 61.68750000000001 0 0 1 27.407360800000003 -82.84556917500001Z"/><path d="M482.18750000000006 356.25000000000006a93.75000000000001 93.75000000000001 0 1 1 -125.93750000000003 -41.56250000000001 93.75000000000001 93.75000000000001 0 0 1 125.93750000000003 41.56250000000001Z"/><path d="m398.43750000000006 492.18750000000006 0 234.37500000000003"/><path d="m187.50000000000003 726.5625000000001 143.46875000000003 -263.03125"/><path d="m609.3750000000001 726.5625000000001 -143.46875000000003 -263.03125"/></g></svg>'''

PAGEHERO = '''
<section class="page-hero">
  <div class="wrap">
    <div class="two-col" style="align-items:center; gap:50px;">
      <div class="reveal">
        <div class="eyebrow eyebrow-white">Unser Selbstverständnis</div>
        <h1>Wir glauben an die Kraft von Entwicklung.</h1>
        <p class="lead" style="opacity:.9; max-width:560px;">Wir sind überzeugt, dass Menschen, die wachsen, auch das Unternehmen wachsen lassen. Darum begleiten wir Dich als Mitarbeitende:r oder Vertriebspartner:in in Deiner beruflichen und persönlichen Entwicklung &mdash; und gestalten so die Zukunftsfähigkeit unserer SV.</p>
      </div>
      <div class="reveal leader-card">
        <div class="leader-photo">''' + LEADER_PHOTO_SVG + '''</div>
        <div class="leader-name">Andreas Lex</div>
        <div class="leader-role">Leiter der SV Akademie</div>
        <p class="leader-quote">&bdquo;Entwicklung gelingt dann am besten, wenn wir sie gemeinsam und aktiv gestalten &mdash; genau dafür steht unser Team jeden Tag.&ldquo;</p>
      </div>
    </div>
  </div>
</section>
'''

INTRO = '''
<section class="section">
  <div class="wrap two-col">
    <div class="reveal">
      <div class="eyebrow">Für wen wir da sind</div>
      <h2>Mitarbeitende und Vertriebspartner der SV.</h2>
      <p class="muted">Ob im Innendienst, im Vertrieb oder als selbstständige:r Vertriebspartner:in &mdash; die SV Akademie richtet sich an alle, die im Rahmen ihrer Tätigkeit für die SV wachsen und sich weiterentwickeln möchten. Wir machen Dich fit für morgen: fachlich, persönlich und mit Blick auf das, was im Alltag wirklich zählt.</p>
      <p class="muted">Als strategischer Entwicklungspartner denken wir mit, beraten Dich auf Augenhöhe und entwickeln uns selbst stetig weiter &mdash; verlässlich, serviceorientiert und mit klarem Blick für das Machbare.</p>
    </div>
    <div class="reveal">
      <div class="pdf-preview-card" onclick="openModal('pdfModal')">
        <div class="pdf-preview-thumb"><img src="''' + SELBSTBILD_PREVIEW_URI + '''" alt="Vorschau Selbstverständnis SV Akademie" /></div>
        <div>
          <h3 style="margin-bottom:6px;">Unser Selbstverständnis</h3>
          <p class="muted small" style="margin-bottom:14px;">Was uns antreibt, wofür wir stehen und wie wir zusammenarbeiten &mdash; schriftlich festgehalten.</p>
          <span class="btn btn-outline btn-sm">Vorschau ansehen &rarr;</span>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="modal-overlay" id="pdfModal">
  <div class="modal-box pdf-modal-box">
    <button class="modal-close" onclick="closeModal('pdfModal')">&times;</button>
    <div class="pdf-modal-scroll">
      <img src="''' + SELBSTBILD_PREVIEW_URI + '''" alt="Vorschau Selbstverständnis SV Akademie" />
    </div>
    <div class="pdf-modal-footer">
      <button class="btn btn-primary" onclick="downloadDataUri('''+ "'" + SELBSTBILD_PDF_URI + "'" + ''', 'sv-akademie-selbstverstaendnis.pdf')">Als PDF herunterladen</button>
    </div>
  </div>
</div>
'''

PILLARS = '''
<section class="section">
  <div class="wrap">
    <div class="eyebrow">Unsere 3 Teams</div>
    <h2>Wie wir Entwicklung möglich machen.</h2>
    <div class="grid grid-3" style="margin-top:40px;">
      <div class="card team-card reveal">
        <div class="icon-badge-circle">''' + ICON_CONVERSATION + '''</div>
        <h3>Personalentwicklung</h3>
        <p class="muted">Wir setzen wirksame Impulse durch sichtbare und kreative Personalentwicklung und verbinden Kompetenzentwicklung mit Unternehmenszielen.</p>
        <div class="team-hover-overlay">
          <div class="team-hover-photo">''' + LEADER_PHOTO_SVG + '''</div>
          <div class="team-hover-name">Marie-Therese Herzig</div>
          <div class="team-hover-role">Gruppenleiterin</div>
          <p class="team-hover-text">Du hast Klärungsbedarf zur Weiterbildung Deines Teams? Ich begleite Dich persönlich dabei.</p>
          <a href="quickcheck.html" class="btn btn-primary btn-sm">Quick-Check starten</a>
        </div>
      </div>
      <div class="card team-card reveal">
        <div class="icon-badge-circle">''' + ICON_ELEARNING + '''</div>
        <h3>Bildungsorganisation, -systeme und -medien</h3>
        <p class="muted">Wir schaffen den organisatorischen, technischen und medialen Rahmen für wirksames Lernen, liefern Support und hochwertigen Content.</p>
        <div class="team-hover-overlay">
          <div class="team-hover-photo">''' + LEADER_PHOTO_SVG + '''</div>
          <div class="team-hover-name">Lukas Euring</div>
          <div class="team-hover-role">Gruppenleiter</div>
          <p class="team-hover-text">Ich zeige Dir, wie Du im KI-Lernassistenten jederzeit die passenden Trainings findest.</p>
          <a href="portal.html" class="btn btn-primary btn-sm">KI-Lernassistent entdecken</a>
        </div>
      </div>
      <div class="card team-card reveal">
        <div class="icon-badge-circle">''' + ICON_GRADUATE + '''</div>
        <h3>Training und Bildungstransfer</h3>
        <p class="muted">Wir entwickeln wirksame und zeitgemäße Trainings, führen diese durch und schaffen nachhaltig begeisternde Lernerlebnisse.</p>
        <div class="team-hover-overlay">
          <div class="team-hover-photo">''' + LEADER_PHOTO_SVG + '''</div>
          <div class="team-hover-name">Philip Dreyer</div>
          <div class="team-hover-role">Gruppenleiter</div>
          <p class="team-hover-text">Lern mich und das Team beim nächsten Community-Austausch persönlich kennen.</p>
          <a href="community.html" class="btn btn-primary btn-sm">Community-Austausch</a>
        </div>
      </div>
    </div>
  </div>
</section>
'''

EINBETTUNG = '''
<section class="section bg-grau">
  <div class="wrap">
    <div class="two-col" style="align-items:start; gap:64px;">
      <div class="reveal">
        <div class="eyebrow">Unsere Einbettung &amp; Rolle</div>
        <h2>Mittendrin statt außen vor.</h2>
        <p class="muted" style="max-width:480px;">Wir arbeiten nicht losgelöst von Deinem Alltag, sondern eng verzahnt mit den Fachbereichen und der Personalentwicklung der SV. So verbinden wir strategische Ziele mit den konkreten Anforderungen, die Du in Deiner Rolle täglich erlebst &mdash; und stellen sicher, dass Weiterbildung dort ansetzt, wo sie wirklich wirkt.</p>
        <p class="muted" style="max-width:480px;">Als Bindeglied zwischen Unternehmensstrategie, Führungskräften und Mitarbeitenden sorgen wir dafür, dass Entwicklung kein Silo bleibt, sondern Teil des großen Ganzen wird.</p>
      </div>
      <div class="reveal" style="margin-top:90px;">
        <div class="detail-list">
          <div class="detail-row">
            <h3><span class="detail-icon-badge">''' + ICON_GROWTH + '''</span><span>Eigenverantwortung &amp; -motivation</span></h3>
            <div class="detail-reveal">
              <p class="muted small">Ohne Eigenverantwortung und intrinsische Motivation sind echte Entwicklungsschritte kaum möglich.</p>
              <button type="button" class="card-more-link" onclick="openModal('einbettungDetail1')">Mehr erfahren &rarr;</button>
            </div>
          </div>
          <div class="detail-row">
            <h3><span class="detail-icon-badge">''' + ICON_UPLOAD_1 + '''</span><span>Zukunftskompetenzen</span></h3>
            <div class="detail-reveal">
              <p class="muted small">KI-, Kunden-, Prozess- und weitere Schlüsselkompetenzen entlang des SV Kompetenzmodells.</p>
              <button type="button" class="card-more-link" onclick="openModal('einbettungDetail2')">Mehr erfahren &rarr;</button>
            </div>
          </div>
          <div class="detail-row">
            <h3><span class="detail-icon-badge">''' + ICON_CONVERSATION + '''</span><span>Personalentwicklung</span></h3>
            <div class="detail-reveal">
              <p class="muted small">Deine Führungskraft als erster Personalentwickler begleitet Deine individuelle Route.</p>
              <button type="button" class="card-more-link" onclick="openModal('einbettungDetail3')">Mehr erfahren &rarr;</button>
            </div>
          </div>
          <div class="detail-row">
            <h3><span class="detail-icon-badge">''' + ICON_ELEARNING + '''</span><span>Lernmanagement</span></h3>
            <div class="detail-reveal">
              <p class="muted small">Vielfältige Qualifizierungsformate der SV Akademie &mdash; inklusive Deinem Lernassistenten LEA.</p>
              <button type="button" class="card-more-link" onclick="openModal('einbettungDetail4')">Mehr erfahren &rarr;</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

<div class="modal-overlay" id="einbettungDetail1">
  <div class="modal-box" style="max-width:560px; text-align:left;">
    <button class="modal-close" onclick="closeModal('einbettungDetail1')">&times;</button>
    <h3 style="margin-bottom:16px;">Eigenverantwortung und -motivation</h3>
    <p class="muted">Eigenverantwortung und -motivation sind zwei essenzielle Voraussetzungen für die persönliche Entwicklung. Ohne sie sind echte Fortschritte kaum zu erzielen, da externe Einflüsse nicht ausreichen, um echte Veränderungen zu bewirken.</p>
    <p class="muted" style="margin-top:14px;">Wer sich selbst motivieren kann und Verantwortung für sich übernimmt, legt damit nicht nur aktiv die Basis für ein spürbar selbstbestimmtes, erfülltes Leben, sondern pflegt gleichzeitig auch die eigenen Ressourcen und festigt seine Resilienz.</p>
  </div>
</div>

<div class="modal-overlay" id="einbettungDetail2">
  <div class="modal-box" style="max-width:560px; text-align:left;">
    <button class="modal-close" onclick="closeModal('einbettungDetail2')">&times;</button>
    <h3 style="margin-bottom:16px;">Zukunftskompetenzen</h3>
    <p class="muted">Neben dem grundlegenden SV <a href="https://svnet.pr.sv.loc/svcms/_galleries_/download/mitarbeiter/personal-id/Darstellung-Kompetenzmodell-2023_Intranet.pdf" target="_blank" rel="noopener" style="color:var(--rot); font-weight:700;">Kompetenzmodell</a> sind das v.&nbsp;a.:</p>
    <ul style="padding-left:20px; color:var(--dunkelgrau1); margin:14px 0 0; font-size:.95rem; line-height:1.8;">
      <li>KI- &amp; Digitalkompetenz</li>
      <li>Kundenbegeisterungskompetenz</li>
      <li>Prozesskompetenz</li>
      <li>Projektkompetenz</li>
      <li>Innovationskompetenz</li>
      <li>Nachhaltigkeitskompetenz</li>
      <li>Führungskompetenz</li>
    </ul>
  </div>
</div>

<div class="modal-overlay" id="einbettungDetail3">
  <div class="modal-box" style="max-width:560px; text-align:left;">
    <button class="modal-close" onclick="closeModal('einbettungDetail3')">&times;</button>
    <h3 style="margin-bottom:16px;">Personalentwicklung</h3>
    <p class="muted">Die Personalentwicklung betrachtet individuelle Stärken und Interessen, entdeckt Potenziale und plant gemeinsam mit Dir die passende Route für die persönliche Entwicklung.</p>
    <p class="muted" style="margin-top:14px;">Als &bdquo;erster Personalentwickler&ldquo; ist die Führungskraft auch erste Ansprechperson für die persönlich-individuelle Entwicklung.</p>
    <p class="muted" style="margin-top:14px;">Diese umfasst sowohl fachliche wie auch persönliche, soziale und methodische Entwicklungsmöglichkeiten und Karrierewege in der SV.</p>
  </div>
</div>

<div class="modal-overlay" id="einbettungDetail4">
  <div class="modal-box" style="max-width:560px; text-align:left;">
    <button class="modal-close" onclick="closeModal('einbettungDetail4')">&times;</button>
    <h3 style="margin-bottom:16px;">Lernmanagement</h3>
    <p class="muted">Wir, die SV Akademie, sind Dein Ansprechpartner für Bildung und Weiterentwicklung.</p>
    <p class="muted" style="margin-top:14px;">Im zentralen Qualifizierungsangebot der SV Akademie erwarten Dich vielfältige Qualifizierungsmaßnahmen. Ob fachliche Expertise, persönliche Weiterentwicklung, methodische Fähigkeiten: unsere abwechslungsreichen Formate unterstützen Dich dabei, Deine Stärken voll zu entfalten und neue Kompetenzen zu entdecken.</p>
    <p class="muted" style="margin-top:14px;">Und hier kannst Du <strong>LEA</strong>, Deinem persönlichen Lernassistenten, alle Fragen rund um Deine Weiterbildung stellen:</p>
    <a href="portal.html" class="btn btn-primary btn-block" style="margin-top:14px;">LEA jetzt fragen &rarr;</a>
  </div>
</div>
'''

TEAM_NAMES = [
    ("Anna Berger", "Personalentwicklung"), ("Jonas Wolf", "Personalentwicklung"),
    ("Lena Hoffmann", "Personalentwicklung"), ("Tim Schröder", "Personalentwicklung"),
    ("Mara Fischer", "Personalentwicklung"), ("David Klein", "Personalentwicklung"),
    ("Sophie Neumann", "Personalentwicklung"), ("Paul Zimmermann", "Personalentwicklung"),
    ("Nina Krüger", "Personalentwicklung"), ("Felix Schwarz", "Personalentwicklung"),
    ("Marie Lange", "Personalentwicklung"), ("Jan Wagner", "Personalentwicklung"),
    ("Laura Becker", "Personalentwicklung"), ("Simon Braun", "Personalentwicklung"),
    ("Julia Hartmann", "Bildungsorganisation"), ("Max Vogel", "Bildungsorganisation"),
    ("Emma Richter", "Bildungsorganisation"), ("Noah Weber", "Bildungsorganisation"),
    ("Lea König", "Bildungsorganisation"), ("Ben Schulze", "Bildungsorganisation"),
    ("Clara Peters", "Bildungsorganisation"), ("Lukas Frank", "Bildungsorganisation"),
    ("Hanna Albrecht", "Bildungsorganisation"), ("Erik Sommer", "Bildungsorganisation"),
    ("Mia Winter", "Bildungsorganisation"), ("Tom Keller", "Bildungsorganisation"),
    ("Frieda Lorenz", "Bildungsorganisation"), ("Nils Baumann", "Bildungsorganisation"),
    ("Ida Franke", "Training &amp; Bildungstransfer"), ("Leon Herrmann", "Training &amp; Bildungstransfer"),
    ("Greta Bauer", "Training &amp; Bildungstransfer"), ("Finn Koch", "Training &amp; Bildungstransfer"),
    ("Paula Voigt", "Training &amp; Bildungstransfer"), ("Lars Meyer", "Training &amp; Bildungstransfer"),
    ("Emilia Roth", "Training &amp; Bildungstransfer"), ("Oskar Jung", "Training &amp; Bildungstransfer"),
    ("Johanna Graf", "Training &amp; Bildungstransfer"), ("Anton Pfeiffer", "Training &amp; Bildungstransfer"),
    ("Luisa Beck", "Training &amp; Bildungstransfer"), ("Moritz Horn", "Training &amp; Bildungstransfer"),
    ("Charlotte Busch", "Training &amp; Bildungstransfer"), ("Elias Otto", "Training &amp; Bildungstransfer"),
]

team_html = []
for name, role in TEAM_NAMES:
    team_html.append('''
      <div class="team-member reveal">
        <div class="team-avatar">''' + ICON_PERSON + '''</div>
        <div class="t-name">''' + name + '''</div>
        <div class="t-role">''' + role + '''</div>
      </div>''')

TEAM = '''
<section class="section">
  <div class="wrap">
    <div class="eyebrow">Die Menschen hinter der SV Akademie</div>
    <h2>Unser Team.</h2>
    <p class="muted" style="max-width:640px;">Hinter jedem Angebot der SV Akademie stehen Menschen, die Entwicklung ernst nehmen &mdash; fachlich fundiert und mit echtem Interesse an Deiner Weiterentwicklung.</p>
    <div class="team-grid">
      ''' + "\n".join(team_html) + '''
    </div>
  </div>
</section>
'''

CTA = '''
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

BODY = PAGEHERO + INTRO + PILLARS + EINBETTUNG + TEAM + CTA

html = page_shell(
    "Über uns — SV Akademie",
    "Unser Selbstverständnis: Wir glauben an die Kraft von Entwicklung und begleiten Mitarbeitende und Vertriebspartner der SV.",
    "ueber-uns.html",
    BODY,
)
with open(os.path.join(SITEDIR, "ueber-uns.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("ueber-uns.html written:", len(html), "chars")
