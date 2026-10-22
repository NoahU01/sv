/* U-Bahn-Plan „Vom Ergebnis her gedacht“ – SV Akademie (Daniel, 22.10.2026)
   Maßstab: die feine Darstellung des Meilensteinplans.
   - Gegangener Weg dick, offener Weg dünn – man sieht sofort, wo die nächsten freien Punkte sind.
   - Ergebnisstufe wählen: gezeigt wird der Weg bis dorthin; was nicht einfließt, wird blass.
   - Station anklicken: Inhalte, Ergebnis, kritischer Punkt – und rückwärts gedacht nur die Linien,
     die zu dieser Station führen.
   Daten: window.ZIEL_DATEN (ziel-daten.js, aus entwicklung_strategie.json). */
(function () {
  "use strict";
  var D = window.ZIEL_DATEN;
  if (!D) return;
  var S = {}, STR = {}, MS = {};
  D.schritte.forEach(function (s) { S[s.id] = s; });
  D.straenge.forEach(function (s, i) { s.i = i; STR[s.id] = s; });
  D.meilensteine.forEach(function (m, i) { m.i = i; MS[m.id] = m; });

  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function msName(m) { return m.titel || "Ergebnisstufe " + m.nr; }
  function fertig(id) { return S[id] && S[id].status === "erreicht"; }
  function zustand(s) {
    if (s.status === "erreicht") return "erreicht";
    if (s.status === "aktiv") return "aktiv";
    return (s.braucht || []).every(fertig) ? "frei" : "wartet";
  }
  var ZTEXT = { erreicht: "erledigt", aktiv: "in Arbeit", frei: "kann starten", wartet: "wartet auf Vorarbeit" };
  function vorlauf(ids) {               // alles, was in diese Schritte einfließt – inklusive der Schritte selbst
    var drin = {}, st = ids.slice();
    while (st.length) { var id = st.pop(); if (drin[id] || !S[id]) continue; drin[id] = true; (S[id].braucht || []).forEach(function (b) { st.push(b); }); }
    return drin;
  }

  // „ziel“ = Gesamtplan: alle Stufen bis zum Zielbild, nichts wird blass
  var ZIEL = { id: "ziel", i: D.meilensteine.length - 1, nr: "", titel: D.zielbild.kurz || "Zielbild", termin: "Ende des Projekts", braucht: null, gesamt: true };
  function msVon(id) { return id === "ziel" ? ZIEL : MS[id]; }
  var zustandUI = { ms: (function () { var h = location.hash.replace("#", ""); return MS[h] || h === "ziel" ? h : D.meilensteine[0].id; })(), station: null };
  var stufenEl = document.getElementById("ub-stufen"), planEl = document.getElementById("ub-plan"), detailEl = document.getElementById("ub-detail");

  /* ---------- Ergebnisstufen ---------- */
  function stufen() {
    var m = msVon(zustandUI.ms);
    var h = '<ol class="ub-leiste">';
    D.meilensteine.forEach(function (x) {
      h += '<li><button type="button" data-ms="' + x.id + '" aria-pressed="' + (x.id === zustandUI.ms) + '"><span class="ub-leiste-punkt"></span>' +
        '<span class="ub-leiste-nr">Stufe ' + x.nr + '</span><b>' + esc(msName(x)) + '</b><small>' + esc(x.termin) + "</small></button></li>";
    });
    h += '<li class="ub-leiste-ziel"><button type="button" data-ms="ziel" aria-pressed="' + (zustandUI.ms === "ziel") + '"><span class="ub-leiste-punkt"></span><span class="ub-leiste-nr">Ziel &middot; Gesamtplan</span><b>' + esc(ZIEL.titel) + "</b><small>Ende des Projekts</small></button></li></ol>";
    if (m.gesamt) {
      var zb = D.zielbild.text && D.zielbild.text.indexOf("Platzhalter") < 0 ? D.zielbild.text : "";
      h += '<div class="ub-stufe"><div class="ub-stufe-kopf"><span>Gesamtplan &middot; alle Stufen</span><h3>' + esc(ZIEL.titel) + '</h3></div>' +
        '<div class="ub-stufe-text"><p class="ub-klein">Zielbild</p>' + (zb ? "<p>" + esc(zb) + "</p>" : '<p class="ub-offen">Das Zielbild wird noch beschrieben.</p>') + "</div></div>";
    } else {
      h += '<div class="ub-stufe"><div class="ub-stufe-kopf"><span>Stufe ' + m.nr + " &middot; " + esc(m.termin) + '</span><h3>' + esc(msName(m)) + '</h3></div>' +
        '<div class="ub-stufe-text"><p class="ub-klein">Erreicht, wenn</p><ul>' + (m.ergebnis || []).map(function (e) { return "<li>" + esc(e) + "</li>"; }).join("") + "</ul></div></div>";
    }
    stufenEl.innerHTML = h;
    stufenEl.querySelectorAll("[data-ms]").forEach(function (b) {
      b.addEventListener("click", function () {
        zustandUI.ms = b.getAttribute("data-ms"); zustandUI.station = null;
        history.replaceState(null, "", "#" + zustandUI.ms);
        stufen(); plan(); detail();
      });
    });
  }

  /* ---------- Plan ---------- */
  var ABST = 128, LINKS = 24, ZH = 60, BAHN = 150, OBEN = 70, LUECKE = 34;
  function plan() {
    var m = msVon(zustandUI.ms);
    var liste = D.schritte.filter(function (s) { return MS[s.meilenstein].i <= m.i; });
    var imPlan = {}; liste.forEach(function (s) { imPlan[s.id] = true; });
    var fokus = zustandUI.station ? vorlauf([zustandUI.station]) : m.gesamt ? imPlan : vorlauf(m.braucht || []);

    // Spalten: je Stufe ein Band, darin die Tiefe innerhalb der Stufe
    var tiefe = {};
    function t(id) {
      if (tiefe[id] != null) return tiefe[id];
      var s = S[id], v = (s.braucht || []).filter(function (b) { return imPlan[b] && S[b].meilenstein === s.meilenstein; });
      return (tiefe[id] = v.length ? 1 + Math.max.apply(null, v.map(t)) : 0);
    }
    liste.forEach(function (s) { t(s.id); });
    var bandStart = [], bandBreite = [], lauf = 0;
    D.meilensteine.forEach(function (x) {
      if (x.i > m.i) return;
      var w = 0; liste.forEach(function (s) { if (s.meilenstein === x.id) w = Math.max(w, tiefe[s.id] + 1); });
      bandStart[x.i] = lauf; bandBreite[x.i] = w; lauf += w;
    });
    function xVon(s) { var k = MS[s.meilenstein].i; return LINKS + (bandStart[k] + tiefe[s.id]) * ABST + k * LUECKE + ABST / 2; }
    function xGrenze(k) { return LINKS + (bandStart[k] + bandBreite[k]) * ABST + k * LUECKE + LUECKE / 2; }
    // Zeilen: parallele Halte (gleiche Stoßrichtung, Stufe und Tiefe) liegen über und unter der Linie
    var gruppen = {};
    liste.forEach(function (s) { var k = s.strang + "|" + s.meilenstein + "|" + tiefe[s.id]; (gruppen[k] = gruppen[k] || []).push(s); });
    var versatz = {};
    Object.keys(gruppen).forEach(function (k) { var g = gruppen[k]; g.forEach(function (s, i) { versatz[s.id] = (i - (g.length - 1) / 2) * ZH; }); });
    var bahnen = D.straenge.filter(function (st) { return liste.some(function (s) { return s.strang === st.id; }); });
    var bahnY = {}; bahnen.forEach(function (st, i) { bahnY[st.id] = OBEN + i * BAHN + BAHN / 2; });
    function yVon(s) { return bahnY[s.strang] + versatz[s.id]; }
    var breite = xGrenze(m.i) + 110, hoehe = OBEN + bahnen.length * BAHN + 10;

    var svg = '<svg width="' + breite + '" height="' + hoehe + '" class="ub-svg" aria-hidden="true">';
    // Stufengrenzen
    var kopf = "";
    D.meilensteine.forEach(function (x) {
      if (x.i > m.i) return;
      var gx = xGrenze(x.i), sel = x.id === m.id || (m.gesamt && x.i === m.i);
      svg += '<line x1="' + gx + '" y1="' + (OBEN - 18) + '" x2="' + gx + '" y2="' + (hoehe - 6) + '" class="ub-grenze' + (sel ? " ub-grenze--ziel" : "") + '"/>';
      kopf += '<div class="ub-grenze-name' + (sel ? " ub-grenze-name--ziel" : "") + '" style="left:' + gx + 'px"><span>Stufe ' + x.nr + " &middot; " + esc(x.termin) + "</span><b>" + esc(msName(x)) + "</b></div>";
    });
    // Strecken
    var dick = "", duenn = "", quer = "";
    function blass(id) { return !fokus[id]; }
    function strecke(x1, y1, x2, y2) {
      if (Math.abs(y1 - y2) < 1) return "M" + x1 + "," + y1 + " L" + x2 + "," + y2;
      var mx = (x1 + x2) / 2;
      return "M" + x1 + "," + y1 + " C" + mx + "," + y1 + " " + mx + "," + y2 + " " + x2 + "," + y2;
    }
    // Abhängigkeit zwischen Stoßrichtungen: erst entlang der Linie, dann senkrecht in den Ziel-Halt –
    // so kreuzt sie keine Beschriftung
    function querweg(x1, y1, x2, y2) {
      return "M" + x1 + "," + y1 + " C" + (x2 - 10) + "," + y1 + " " + x2 + "," + (y1 + (y2 - y1) * 0.35) + " " + x2 + "," + y2;
    }
    function zeichne(d, farbe, gegangen, schwach) {
      var o = schwach ? ' opacity="0.16"' : "";
      if (gegangen) dick += '<path d="' + d + '" stroke="' + farbe + '" stroke-width="7" fill="none" stroke-linecap="round"' + o + "/>";
      else duenn += '<path d="' + d + '" stroke="' + farbe + '" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-opacity="' + (schwach ? 0.12 : 0.55) + '"/>';
    }
    bahnen.forEach(function (st) {
      var eig = liste.filter(function (s) { return s.strang === st.id; });
      // Einlauf bis zu den ersten Halten
      eig.filter(function (s) { return !(s.braucht || []).some(function (b) { return imPlan[b] && S[b].strang === st.id; }); }).forEach(function (s) {
        zeichne(strecke(LINKS - 6, bahnY[st.id], xVon(s), yVon(s)), st.farbe, s.status !== "offen", blass(s.id));
      });
      // Auslauf der letzten Halte bis zur gewählten Stufe
      eig.filter(function (s) { return !liste.some(function (n) { return n.strang === st.id && (n.braucht || []).indexOf(s.id) > -1; }); }).forEach(function (s) {
        zeichne(strecke(xVon(s), yVon(s), xGrenze(m.i), bahnY[st.id]), st.farbe, false, blass(s.id));
      });
    });
    liste.forEach(function (s) {
      (s.braucht || []).forEach(function (b) {
        if (!imPlan[b]) return;
        var v = S[b], d = strecke(xVon(v), yVon(v), xVon(s), yVon(s));
        if (v.strang === s.strang) zeichne(d, STR[s.strang].farbe, v.status === "erreicht", blass(s.id) || blass(b));
        else quer += '<path d="' + querweg(xVon(v), yVon(v), xVon(s), yVon(s)) + '" stroke="#8a857d" stroke-width="1.6" stroke-dasharray="4 5" fill="none"' + (blass(s.id) ? ' opacity="0.2"' : "") + "/>";
      });
    });
    svg += quer + duenn + dick;
    // Halte
    var namen = "";
    liste.forEach(function (s) {
      var z = zustand(s), f = STR[s.strang].farbe, cx = xVon(s), cy = yVon(s), schwach = blass(s.id), sel = zustandUI.station === s.id;
      var g = '<g class="ub-halt' + (schwach ? " ub-halt--blass" : "") + '">';
      if (sel) g += '<circle cx="' + cx + '" cy="' + cy + '" r="17" fill="none" stroke="#111" stroke-width="1.5"/>';
      if (z === "aktiv") g += '<circle cx="' + cx + '" cy="' + cy + '" r="14" fill="' + f + '" opacity="0.16"/>';
      g += z === "erreicht" ? '<circle cx="' + cx + '" cy="' + cy + '" r="8" fill="' + f + '"/>'
        : z === "aktiv" ? '<circle cx="' + cx + '" cy="' + cy + '" r="8" fill="#fff" stroke="' + f + '" stroke-width="4"/>'
        : z === "frei" ? '<circle cx="' + cx + '" cy="' + cy + '" r="7.5" fill="#fff" stroke="' + f + '" stroke-width="2.5"/>'
        : '<circle cx="' + cx + '" cy="' + cy + '" r="7" fill="#fff" stroke="#c4bfb7" stroke-width="2"/>';
      if (s.kritisch) g += '<circle cx="' + (cx + 10) + '" cy="' + (cy - 11) + '" r="6.5" fill="#E8553A"/><text x="' + (cx + 10) + '" y="' + (cy - 7.6) + '" text-anchor="middle" class="ub-ausruf">!</text>';
      svg += g + "</g>";
      var oben = versatz[s.id] < 0;
      namen += '<button type="button" class="ub-name ub-name--' + z + (oben ? " ub-name--oben" : "") + (schwach ? " ub-name--blass" : "") + (sel ? " ub-name--gewaehlt" : "") +
        '" data-station="' + s.id + '" style="left:' + (cx - (ABST - 10) / 2) + "px;top:" + (oben ? cy - 16 : cy + 15) + "px;width:" + (ABST - 10) + 'px">' +
        "<b>" + esc(s.titel) + "</b>" + (s.termin ? '<small class="ub-termin">' + esc(s.termin) + "</small>" : "") + (s.wer ? '<small class="ub-wer">' + esc(s.wer) + "</small>" : "") + "</button>";
      // unsichtbare Fläche auf dem Punkt, damit auch der Halt selbst klickbar ist
      namen += '<button type="button" class="ub-treffer" data-station="' + s.id + '" aria-label="' + esc(s.titel) + '" style="left:' + (cx - 16) + "px;top:" + (cy - 16) + 'px"></button>';
    });
    svg += "</svg>";
    var spalte = bahnen.map(function (st) {
      return '<div class="ub-bahn" style="top:' + (bahnY[st.id] - 40) + 'px"><i style="background:' + st.farbe + '"></i><b>' + esc(st.label) + "</b>" +
        (st.frage ? "<small>" + esc(st.frage) + "</small>" : "") + "<em>" + esc(st.verantwortung) + "</em></div>";
    }).join("");
    planEl.innerHTML = '<div class="ub-rahmen"><div class="ub-spalte" style="height:' + hoehe + 'px">' + spalte + '</div><div class="ub-scroll"><div class="ub-flaeche" style="width:' + breite + "px;height:" + hoehe + 'px">' + svg + kopf + namen + "</div></div></div>";
    planEl.querySelectorAll("[data-station]").forEach(function (b) {
      b.addEventListener("click", function () {
        var id = b.getAttribute("data-station");
        zustandUI.station = zustandUI.station === id ? null : id;
        plan(); detail();
        if (zustandUI.station) detailEl.scrollIntoView({ behavior: "smooth", block: "nearest" });
      });
    });
    var sc = planEl.querySelector(".ub-scroll");
    // Öffnen dort, wo der Weg gerade frei ist: der erste noch nicht erledigte Halt im Fokus steht links im Blick
    if (sc && !zustandUI.station && sc.scrollWidth > sc.clientWidth) {
      var offen = liste.filter(function (s) { return fokus[s.id] && s.status !== "erreicht"; }).map(xVon);
      sc.scrollLeft = offen.length ? Math.max(0, Math.min.apply(null, offen) - 2 * ABST) : 0;
    }   // die gewählte Stufe steht im Blick
    ziehen(sc);
    var hinweis = document.getElementById("ub-hinweis");
    if (hinweis) hinweis.textContent = zustandUI.station
      ? "Hervorgehoben: alles, was vor „" + S[zustandUI.station].titel + "“ erledigt sein muss. Noch einmal klicken hebt die Auswahl auf."
      : m.gesamt ? "Gesamtplan: alle Stufen bis zum Zielbild. Eine Stufe oben wählen, um den Weg dorthin hervorzuheben."
      : "Hervorgehoben: der Weg zu „" + msName(m) + "“. Blass: läuft parallel, für diese Stufe nicht nötig.";
  }

  // Plan mit gedrückter Maus nach links und rechts ziehen (Touch scrollt ohnehin)
  function ziehen(sc) {
    if (!sc) return;
    var start = null, bewegt = false;
    sc.addEventListener("mousedown", function (e) { if (e.button !== 0) return; start = { x: e.clientX, l: sc.scrollLeft }; bewegt = false; });
    window.addEventListener("mousemove", function (e) {
      if (!start) return;
      var dx = e.clientX - start.x;
      if (Math.abs(dx) > 4) { bewegt = true; sc.classList.add("ub-zieht"); }
      sc.scrollLeft = start.l - dx;
    });
    window.addEventListener("mouseup", function () { start = null; setTimeout(function () { sc.classList.remove("ub-zieht"); }, 0); });
    sc.addEventListener("click", function (e) { if (bewegt) { e.stopPropagation(); e.preventDefault(); bewegt = false; } }, true);
  }

  /* ---------- Detail einer Station ---------- */
  function detail() {
    var id = zustandUI.station;
    if (!id) { detailEl.hidden = true; detailEl.innerHTML = ""; return; }
    var s = S[id], st = STR[s.strang], z = zustand(s);
    var vor = (s.braucht || []).map(function (b) { return S[b]; });
    var h = '<div class="ub-detail-kopf"><span class="ub-chip" style="--f:' + st.farbe + '">' + esc(st.label) + '</span><span class="ub-zustand ub-zustand--' + z + '">' + ZTEXT[z] + "</span>" +
      '<button type="button" class="ub-zu" aria-label="Schließen">&times;</button></div>' +
      "<h3>" + esc(s.titel) + "</h3><p class=\"ub-wer-zeile\">" + esc(st.verantwortung) + (s.wer ? " &middot; " + esc(s.wer) : "") + "</p><div class=\"ub-detail-raster\">";
    if ((s.details || []).length) h += '<div><p class="ub-klein">Inhalte</p><ul>' + s.details.map(function (d) { return "<li>" + esc(d) + "</li>"; }).join("") + "</ul></div>";
    if (s.ergebnis) h += '<div><p class="ub-klein">Ergebnis</p><p>' + esc(s.ergebnis) + "</p></div>";
    if (vor.length) h += '<div><p class="ub-klein">Braucht vorher</p><ul>' + vor.map(function (v) { return "<li>" + esc(v.titel) + ' <small>' + ZTEXT[zustand(v)] + "</small></li>"; }).join("") + "</ul></div>";
    h += "</div>";
    if (s.kritisch) h += '<div class="ub-kritisch"><p class="ub-klein">Kritischer Punkt</p><p>' + esc(s.kritisch.grund) + "</p><p>" + esc(s.kritisch.blockiert) + "</p></div>";
    detailEl.innerHTML = h; detailEl.hidden = false;
    detailEl.querySelector(".ub-zu").addEventListener("click", function () { zustandUI.station = null; plan(); detail(); });
  }

  stufen(); plan(); detail();
})();
