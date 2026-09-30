# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, "/sessions/ecstatic-nice-gauss/mnt/outputs/_work")
from build_common import *

PAGEHERO = '''
<section class="page-hero" style="padding-bottom:190px; text-align:center; background:transparent;">
  <div class="wrap" style="max-width:700px;">
    <div class="eyebrow eyebrow-white" style="justify-content:center; display:flex;">Dein KI-Assistent</div>
    <h1>Frag einfach. Ich antworte.</h1>
    <p class="lead" style="opacity:.9; max-width:600px; margin:0 auto;">Kein Suchen, kein Klicken durch Menüs. Stelle mir direkt Deine Fragen zu unseren Weiterbildungsangeboten und ich liefere Dir zielgenaue Vorschläge.</p>
    <p class="lead" style="opacity:.9; max-width:600px; margin:20px auto 0;">Probier&rsquo;s gleich aus.</p>
  </div>
</section>
'''

# ---- Beispielfragen mit passenden Demo-Antworten (inkl. Rückfrage zur Detaillierung) ----
SUGGESTIONS = [
    ("Zeig mir passende Weiterbildungen zum Thema Digitalisierung.",
     "Ich habe 4 aktuelle Formate zum Thema Digitalisierung für Dich gefunden &mdash; vom kompakten Impuls-Webinar bis zum vertiefenden Zertifikatskurs. Interessiert Dich eher der Einstieg ins Thema, oder suchst Du etwas für ein bestimmtes Anwendungsfeld wie Kundenberatung oder interne Prozesse?"),
    ("Erstelle mir einen Lernplan für die nächsten 4 Wochen.",
     "Gerne erstelle ich Dir einen Lernplan für die nächsten 4 Wochen. Damit er wirklich zu Dir passt: Wie viel Zeit kannst Du pro Woche ungefähr einplanen, und worauf soll der Schwerpunkt liegen?"),
    ("Welche Lernvideos erklären mir am besten das Thema Hausratversicherung?",
     "Zum Thema Hausratversicherung habe ich 3 kurze Erklärvideos gefunden &mdash; zu Grundlagen, Leistungsfällen und Beratungsargumenten. Soll ich Dir gezielt eines dieser Themen zeigen, oder starten wir mit den Grundlagen?"),
    ("Welche Trainings passen zu meiner Rolle als VTA?",
     "Für Vertriebsassistent:innen auf der Geschäftsstelle empfehle ich aktuell Trainings zu Terminvorbereitung, Kundenkommunikation und den gängigen Vertriebstools. Soll ich Dir zeigen, was gerade neu ist, oder interessiert Dich ein bestimmter Bereich davon?"),
    ("Welche Seminare zu Word und Excel finden im September?",
     "Im September bieten wir zwei Seminare an: einen Excel-Grundlagenkurs am 10.09. und ein Word-Kompaktseminar am 22.09., jeweils online. Soll ich Dich direkt für eines der beiden vormerken?"),
]
AI_FALLBACK = "Das ist eine Vorschau des KI-Lernassistenten. In der finalen Version beantworte ich hier Deine Fragen live und zeige Dir passende Trainings, Mediathek-Inhalte und einen individuellen Lernpfad zu unseren Weiterbildungsangeboten."

chips_html = "\n".join([
    '<button type="button" class="suggestion-chip" data-question="' + q + '">' + q + '</button>'
    for q, a in SUGGESTIONS
])

CHATBOT = '''
<section class="section" style="padding:0 0 140px; position:relative; z-index:3;">
  <div class="wrap" style="max-width:760px;">
    <div class="ai-chat-widget reveal" style="margin-top:-140px;">
      <div class="ai-chat-topbar">
        <span class="dot"></span>
        <span style="font-family:var(--font-head); font-weight:700;">SV Akademie Assistent</span>
        <span class="pill pill-grau" style="margin-left:auto;">Vorschau</span>
      </div>
      <div class="ai-chat-body" id="aiChatBody">
        <div class="ai-chat-empty" id="aiChatEmpty">
          <p>Stell eine eigene Frage oder wähle einen Vorschlag:</p>
          <div class="suggestion-chips" id="suggestionChips">
            ''' + chips_html + '''
          </div>
        </div>
      </div>
      <div class="ai-chat-inputrow">
        <input type="text" id="aiChatInput" placeholder="Frag mich etwas zu Deiner Weiterbildung &hellip;" />
        <button type="button" class="ai-chat-send" id="aiChatSend" aria-label="Senden">&rarr;</button>
      </div>
    </div>
  </div>
</section>
'''

BODY = '''
<div style="background: linear-gradient(180deg, var(--rot) 0%, #6a1f66 42%, var(--dunkelgrau2) 100%);">
''' + PAGEHERO + CHATBOT + '''
</div>
'''

ai_responses_js = "{\n" + ",\n".join([
    "  " + repr(q) + ": " + repr(a)
    for q, a in SUGGESTIONS
]) + "\n}"

EXTRA_JS = '''
var AI_RESPONSES = ''' + ai_responses_js + ''';
var AI_FALLBACK = ''' + repr(AI_FALLBACK) + ''';

function aiSend(question){
  question = (question || "").trim();
  if (!question) return;
  var empty = document.getElementById("aiChatEmpty");
  if (empty) empty.remove();
  var body = document.getElementById("aiChatBody");

  var userBubble = document.createElement("div");
  userBubble.className = "ai-chat-bubble user";
  userBubble.textContent = question;
  body.appendChild(userBubble);

  var typing = document.createElement("div");
  typing.className = "ai-chat-bubble assistant";
  typing.id = "aiTypingBubble";
  typing.innerHTML = "<span class=\\"ai-typing\\"><span></span><span></span><span></span></span>";
  body.appendChild(typing);
  body.scrollTop = body.scrollHeight;

  document.getElementById("aiChatInput").value = "";

  setTimeout(function(){
    var answer = AI_RESPONSES[question] || AI_FALLBACK;
    var t = document.getElementById("aiTypingBubble");
    if (t) { t.innerHTML = answer; t.removeAttribute("id"); }
    body.scrollTop = body.scrollHeight;
  }, 700);
}

document.querySelectorAll(".suggestion-chip").forEach(function(chip){
  chip.addEventListener("click", function(){
    aiSend(chip.getAttribute("data-question"));
  });
});

document.getElementById("aiChatSend").addEventListener("click", function(){
  aiSend(document.getElementById("aiChatInput").value);
});
document.getElementById("aiChatInput").addEventListener("keydown", function(e){
  if (e.key === "Enter") { aiSend(this.value); }
});
'''

html = page_shell(
    "KI-Lernassistent (Vorschau) — SV Akademie",
    "Ein erster Einblick in Deinen künftigen KI-Lernassistenten der SV Akademie: zielgenaue Vorschläge für Trainings, Mediathek und Lernfortschritt.",
    "portal.html",
    BODY,
    extra_js=EXTRA_JS,
)
with open(os.path.join(SITEDIR, "portal.html"), "w", encoding="utf-8") as f:
    f.write(html)
print("portal.html written:", len(html), "chars")
