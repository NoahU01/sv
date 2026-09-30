# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_common import *

PAGEHERO = '''
<section class="page-hero">
  <div class="wrap">
    <div class="eyebrow eyebrow-white">Digitaler Community-Austausch</div>
    <h1>Voneinander lernen. Gemeinsam wachsen.</h1>
    <p class="lead" style="opacity:.9; max-width:620px;">Im digitalen Community-Austausch treffen sich Mitarbeitende und Vertriebspartner der SV, um Erfahrungen zu teilen, Praxisfragen zu diskutieren und voneinander zu lernen.</p>
  </div>
</section>
'''

NEXT_EVENT = '''
<section class="section-tight">
  <div class="wrap">
    <div class="two-col reveal" style="align-items:stretch;">
      <div class="card">
        <span class="pill pill-red">Nächster Termin</span>
        <h2 style="margin-top:14px;">Beratung 4.0: Was Kund:innen 2026 wirklich erwarten</h2>
        <p class="muted">Ein offener Austausch über veränderte Erwartungen in der Beratung &mdash; mit kurzem Impuls und viel Raum für Deine Praxisfragen.</p>
        <ul style="padding-left:20px; color:var(--dunkelgrau1); margin-bottom:22px;">
          <li>Donnerstag, 20. August 2026</li>
          <li>16:00 &ndash; 17:00 Uhr</li>
          <li>Online &middot; Videocall</li>
          <li>Kostenfrei für Mitarbeitende &amp; Vertriebspartner der SV</li>
        </ul>
        <a href="#anmeldung" class="btn btn-primary">Jetzt anmelden</a>
      </div>
      <div class="kicker-card">
        <h3>Agenda im Überblick</h3>
        <div class="problem-row"><div class="num-badge" style="width:30px;height:30px;font-size:.85rem;">1</div><div><b>Impuls (10 Min.)</b><p class="muted small" style="margin:0;">Kurzer fachlicher Input zum Thema des Tages.</p></div></div>
        <div class="problem-row"><div class="num-badge" style="width:30px;height:30px;font-size:.85rem;">2</div><div><b>Austausch (35 Min.)</b><p class="muted small" style="margin:0;">Offene Diskussion in kleinen Gruppen &mdash; Deine Praxis im Fokus.</p></div></div>
        <div class="problem-row"><div class="num-badge" style="width:30px;height:30px;font-size:.85rem;">3</div><div><b>Zusammenfassung (15 Min.)</b><p class="muted small" style="margin:0;">Ergebnisse bündeln, nächste Schritte &amp; Materialien.</p></div></div>
      </div>
    </div>
  </div>
</section>
'''

VORSCHAU = '''
<section class="section bg-grau">
  <div class="wrap">
    <div class="eyebrow">Vorschau</div>
    <h2>Was Dich beim Austausch erwartet.</h2>
    <div class="grid grid-3" style="margin-top:32px;">
      <div class="card reveal"><div class="icon-badge">''' + ICON_CONVERSATION + '''</div><h3>Offener Dialog</h3><p class="muted small">Kleine Gruppen, echte Praxisfragen, keine Frontalbeschallung.</p></div>
      <div class="card reveal"><div class="icon-badge">''' + ICON_GRADUATE + '''</div><h3>Erfahrungswissen</h3><p class="muted small">Lerne von Kolleg:innen und Vertriebspartner:innen, die Ähnliches erleben.</p></div>
      <div class="card reveal"><div class="icon-badge">''' + ICON_ELEARNING + '''</div><h3>Direkt nutzbar</h3><p class="muted small">Materialien und Zusammenfassung erhältst Du im Anschluss digital.</p></div>
    </div>
  </div>
</section>
'''

VERGANGEN = '''
<section class="section">
  <div class="wrap">
    <div class="eyebrow">Bereits stattgefunden</div>
    <h2>Frühere Austausch-Termine</h2>
    <table class="simple-table reveal" style="margin-top:24px;">
      <tr><th>Thema</th><th>Datum</th><th>Teilnehmende</th></tr>
      <tr><td>Zukunftsfähig beraten: Digital &amp; persönlich</td><td>18.06.2026</td><td>34</td></tr>
      <tr><td>Einwandbehandlung im Alltag</td><td>14.05.2026</td><td>41</td></tr>
      <tr><td>Neue Produkte souverän erklären</td><td>09.04.2026</td><td>29</td></tr>
    </table>
  </div>
</section>
'''

ANMELDUNG = '''
<section class="section bg-dunkel" id="anmeldung">
  <div class="wrap" style="max-width:560px;">
    <div class="eyebrow">Jetzt sichern</div>
    <h2>Anmeldung zum Community-Austausch</h2>
    <div class="card reveal" style="color:var(--dunkelgrau2); margin-top:20px;">
      <form id="communityForm">
        <div class="form-row">
          <div class="form-field"><label>Vorname</label><input type="text" required /></div>
          <div class="form-field"><label>Nachname</label><input type="text" required /></div>
        </div>
        <div class="form-field"><label>E-Mail</label><input type="email" required /></div>
        <div class="form-field"><label>Rolle</label>
          <select><option>Mitarbeitende:r der SV</option><option>Vertriebspartner:in der SV</option></select>
        </div>
        <button type="submit" class="btn btn-primary btn-block">Verbindlich anmelden</button>
        <p class="small muted" style="margin-top:12px; margin-bottom:0;">Termin: Do., 20. August 2026, 16:00-17:00 Uhr, online.</p>
      </form>
    </div>
  </div>
</section>

<div class="modal-overlay" id="communityModal">
  <div class="modal-box">
    <button class="modal-close" onclick="closeModal('communityModal')">&times;</button>
    <div class="modal-icon">✓</div>
    <h3>Du bist angemeldet!</h3>
    <p class="muted">Wir freuen uns auf Dich am 20. August um 16:00 Uhr. Speichere Dir den Termin direkt in Deinem Kalender.</p>
    <button class="btn btn-primary btn-block" onclick="downloadCommunityIcs()">Termin in Kalender speichern</button>
  </div>
</div>
'''

BODY = PAGEHERO + NEXT_EVENT + VORSCHAU + VERGANGEN + ANMELDUNG

EXTRA_JS = '''
mockSubmit(document.getElementById('communityForm'), 'communityModal');
function downloadCommunityIcs(){
  var d = new Date(Date.UTC(2026,7,20,14,0,0));
  downloadIcs({
    title: 'SV Akademie: Digitaler Community-Austausch',
    description: 'Beratung 4.0: Was Kund:innen 2026 wirklich erwarten. Online-Austausch der SV Akademie.',
    location: 'Online (Videocall)',
    start: d,
    durationMinutes: 60,
    filename: 'sv-akademie-community-austausch'
  });
}
'''

html = page_shell(
    "Community-Austausch — SV Akademie",
    "Melde Dich zum digitalen Community-Austausch der SV Akademie an und lerne von anderen Mitarbeitenden und Vertriebspartnern.",
    "community.html",
    BODY,
    extra_js=EXTRA_JS,
)
with open(os.path.join(SITEDIR, "community.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("community.html written:", len(html), "chars")
