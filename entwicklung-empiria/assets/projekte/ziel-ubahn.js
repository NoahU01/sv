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

  /* ---------- Ergebnisstufen als Reiter, Erklärung und Legende als kleines Fenster ---------- */
  function stufen() {
    var h = '<div class="ub-reiter" role="tablist">';
    D.meilensteine.forEach(function (x) {
      h += '<button type="button" role="tab" data-ms="' + x.id + '" aria-selected="' + (x.id === zustandUI.ms) + '"><b>' + (x.titel ? x.nr + " &middot; " + esc(x.titel) : "Stufe " + x.nr) + "</b><small>" + esc(x.termin) + "</small></button>";
    });
    h += '<button type="button" role="tab" data-ms="ziel" aria-selected="' + (zustandUI.ms === "ziel") + '"><b>Gesamtplan</b><small>bis zum Zielbild</small></button></div>';
    stufenEl.innerHTML = h;
    stufenEl.querySelectorAll("[data-ms]").forEach(function (b) {
      b.addEventListener("click", function () {
        zustandUI.ms = b.getAttribute("data-ms"); zustandUI.station = null;
        history.replaceState(null, "", "#" + zustandUI.ms);
        infoZu(); stufen(); plan(); detail();
      });
    });
  }
  function infoInhalt(art) {
    var m = msVon(zustandUI.ms);
    if (art === "legende") {
      var k = function (svg, t) { return "<li>" + svg + "<span>" + t + "</span></li>"; };
      return '<p class="ub-pop-titel">Legende</p><ul class="ub-legende">' +
        k('<svg width="22" height="22"><circle cx="11" cy="11" r="7.5" fill="#111" stroke="#fff" stroke-width="3"/><circle cx="11" cy="11" r="9" fill="none" stroke="#111" stroke-width="1.5"/></svg>', "erledigt") +
        k('<svg width="22" height="22"><circle cx="11" cy="11" r="7" fill="#fff" stroke="#111" stroke-width="4.5"/></svg>', "in Arbeit") +
        k('<svg width="22" height="22"><circle cx="11" cy="11" r="7" fill="#fff" stroke="#111" stroke-width="3"/></svg>', "offen") +
        k('<svg width="34" height="12"><line x1="5" y1="6" x2="29" y2="6" stroke="#111" stroke-width="10" stroke-linecap="round"/></svg>', "gegangener Weg") +
        k('<svg width="34" height="12"><line x1="5" y1="6" x2="29" y2="6" stroke="#111" stroke-opacity=".5" stroke-width="5" stroke-linecap="round"/></svg>', "noch offen") +
        k('<svg width="34" height="12"><line x1="2" y1="6" x2="32" y2="6" stroke="#8a857d" stroke-width="2" stroke-dasharray="3 5"/></svg>', "Umstieg: braucht eine andere Linie") +
        k('<svg width="22" height="22"><circle cx="11" cy="11" r="8" fill="#111" opacity=".2"/></svg>', "blass: f&uuml;r diese Stufe nicht n&ouml;tig") + "</ul>";
    }
    if (m.gesamt) return '<p class="ub-pop-titel">' + esc(ZIEL.titel) + '</p><p class="ub-pop-meta">Das Zielbild wird noch beschrieben.</p>';
    return '<p class="ub-pop-titel">' + esc(msName(m)) + '</p><p class="ub-pop-meta">Stufe ' + m.nr + " &middot; " + esc(m.termin) + "</p><ul>" +
      (m.ergebnis || []).map(function (e) { return "<li>" + esc(e) + "</li>"; }).join("") + "</ul>";
  }
  var infoPop = null;
  function infoZu() {
    if (infoPop) { infoPop.remove(); infoPop = null; }
    document.querySelectorAll(".ub-info").forEach(function (b) { b.setAttribute("aria-expanded", "false"); });
  }
  document.querySelectorAll(".ub-info").forEach(function (b) {
    b.addEventListener("click", function (e) {
      e.stopPropagation();
      var offen = b.getAttribute("aria-expanded") === "true";
      infoZu();
      if (offen) return;
      infoPop = document.createElement("div");
      infoPop.className = "ub-pop ub-pop--info";
      infoPop.innerHTML = infoInhalt(b.getAttribute("data-info"));
      b.parentNode.appendChild(infoPop);
      b.setAttribute("aria-expanded", "true");
    });
  });

  /* ---------- Plan: U-Bahn ---------- */
  // Hauptlinie je Stoßrichtung, Beschriftung darüber; parallele Halte auf Nebenstrecken darunter (Beschriftung darunter).
  // Streckenführung wie im Liniennetz: waagerecht, 45°-Knick, waagerecht. Eine Nebenstrecke zweigt erst kurz vor
  // ihrem Halt ab und kehrt gleich danach zurück – so laufen keine Linien über lange Strecken auseinander.
  var ABST = 136, ZH = 72, UEBER = 64, UNTER = 44, LUECKE = 40, EINLAUF = 26, SPALTE = 190;
  function plan() {
    var m = msVon(zustandUI.ms);
    var liste = D.schritte.filter(function (s) { return MS[s.meilenstein].i <= m.i; });
    var imPlan = {}; liste.forEach(function (s) { imPlan[s.id] = true; });
    var fokus = zustandUI.station ? vorlauf([zustandUI.station]) : m.gesamt ? imPlan : vorlauf(m.braucht || []);
    function blass(id) { return !fokus[id]; }

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
      var w = 1; liste.forEach(function (s) { if (s.meilenstein === x.id) w = Math.max(w, tiefe[s.id] + 1); });
      bandStart[x.i] = lauf; bandBreite[x.i] = w; lauf += w;
    });
    // Abstand an die Fensterbreite anpassen, damit die gewählte Stufe samt Endhaltestelle ins Bild passt
    var verfuegbar = planEl.clientWidth - SPALTE;
    ABST = Math.max(108, Math.min(140, (verfuegbar - EINLAUF - LUECKE * m.i - 230) / lauf));
    function xVon(s) { var k = MS[s.meilenstein].i; return EINLAUF + (bandStart[k] + tiefe[s.id]) * ABST + k * LUECKE + ABST / 2; }
    function xGrenze(k) { return EINLAUF + (bandStart[k] + bandBreite[k]) * ABST + k * LUECKE + LUECKE / 2; }

    // Zeilen: erster Halt einer Spalte auf der Hauptlinie, weitere darunter
    var unter = {}, gruppen = {}, tiefsteZeile = {};
    liste.forEach(function (s) {
      var k = s.strang + "|" + s.meilenstein + "|" + tiefe[s.id];
      gruppen[k] = (gruppen[k] || 0); unter[s.id] = gruppen[k]++;
      tiefsteZeile[s.strang] = Math.max(tiefsteZeile[s.strang] || 0, unter[s.id]);
    });
    var bahnen = D.straenge.filter(function (st) { return liste.some(function (s) { return s.strang === st.id; }); });
    var linieY = {}, y0 = m.i > 0 ? 26 : 6;   // oben nur Platz, wenn frühere Stufen beschriftet sind
    bahnen.forEach(function (st) { linieY[st.id] = y0 + UEBER; y0 += UEBER + tiefsteZeile[st.id] * ZH + (tiefsteZeile[st.id] ? UNTER + 34 : UNTER); });   // Nebenstrecke: Platz für ihre Beschriftung darunter
    var hoehe = y0 + 6;
    function yVon(s) { return linieY[s.strang] + unter[s.id] * ZH; }

    // Endhaltestelle: rechts, auf Höhe der Mitte der beteiligten Linien
    var zielX = xGrenze(m.i) + 70;
    var zielBahnen = bahnen.filter(function (st) { return liste.some(function (s) { return s.strang === st.id && fokus[s.id]; }); });
    var zielY = zielBahnen.length ? zielBahnen.reduce(function (a, st) { return a + linieY[st.id]; }, 0) / zielBahnen.length : hoehe / 2;
    var breite = zielX + 160;

    function weg(x1, y1, x2, y2, frueh) {     // waagerecht – 45° – waagerecht
      if (Math.abs(y1 - y2) < 1) return "M" + x1 + "," + y1 + " L" + x2 + "," + y2;
      var d = Math.abs(y2 - y1), r = 14;
      var a = frueh ? x1 + r : Math.max(x1 + r, x2 - r - d);
      var b = a + d;
      return "M" + x1 + "," + y1 + " L" + a + "," + y1 + " L" + b + "," + y2 + " L" + x2 + "," + y2;
    }
    var svg = '<svg width="' + breite + '" height="' + hoehe + '" class="ub-svg" aria-hidden="true">';
    var kopf = "", linien = "", offenL = "", quer = "";
    // frühere Stufen als Haltepunkt-Markierung
    D.meilensteine.forEach(function (x) {
      if (x.i >= m.i || x.i > m.i) return;
      var gx = xGrenze(x.i);
      svg += '<line x1="' + gx + '" y1="22" x2="' + gx + '" y2="' + (hoehe - 4) + '" class="ub-grenze"/>';
      kopf += '<div class="ub-grenze-name" style="left:' + gx + 'px">Stufe ' + x.nr + " &middot; " + esc(msName(x)) + "</div>";
    });
    function strecke(d, farbe, gegangen, schwach) {
      var html = '<path d="' + d + '" stroke="' + farbe + '" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="' + (gegangen ? 10 : 5) + '"' +
        (schwach ? ' opacity="0.14"' : gegangen ? "" : ' opacity="0.5"') + "/>";
      if (gegangen) linien += html; else offenL += html;
    }
    bahnen.forEach(function (st) {
      var eig = liste.filter(function (s) { return s.strang === st.id; });
      // Einlauf aus der Spalte
      eig.filter(function (s) { return !(s.braucht || []).some(function (b) { return imPlan[b] && S[b].strang === st.id; }); }).forEach(function (s) {
        strecke(weg(0, linieY[st.id], xVon(s), yVon(s)), st.farbe, s.status !== "offen", blass(s.id));
      });
      // Auslauf: ins Ziel, wenn die Linie einfließt – sonst endet sie an der Stufengrenze
      eig.filter(function (s) { return !liste.some(function (n) { return n.strang === st.id && (n.braucht || []).indexOf(s.id) > -1; }); }).forEach(function (s) {
        var insZiel = fokus[s.id] && !zustandUI.station;
        strecke(insZiel ? weg(xVon(s), yVon(s), zielX, zielY, unter[s.id] > 0) : weg(xVon(s), yVon(s), xGrenze(m.i), linieY[st.id], true), st.farbe, false, !insZiel && blass(s.id));
      });
    });
    liste.forEach(function (s) {
      (s.braucht || []).forEach(function (b) {
        if (!imPlan[b]) return;
        var v = S[b];
        if (v.strang === s.strang) {
          // zurück auf die Hauptlinie gleich nach dem Halt, auf die Nebenstrecke erst kurz vor dem Halt
          strecke(weg(xVon(v), yVon(v), xVon(s), yVon(s), unter[b] > unter[s.id]), STR[s.strang].farbe, v.status === "erreicht", blass(s.id) || blass(b));
        } else {   // Umstieg: senkrecht in der Lücke vor dem Ziel-Halt
          var x1 = xVon(v), y1 = yVon(v), x2 = xVon(s), y2 = yVon(s), dx = Math.max(0, x2 - x1), dir = y2 > y1 ? 1 : -1;
          var knick = Math.abs(y2 - y1) > dx ? y2 - dir * dx : y1;
          quer += '<path d="M' + x1 + "," + y1 + " L" + x1 + "," + knick + " L" + x2 + "," + y2 + '" stroke="#8a857d" stroke-width="2" fill="none" stroke-dasharray="3 5" stroke-linejoin="round"' + (blass(s.id) ? ' opacity="0.2"' : "") + "/>";
        }
      });
    });
    svg += quer + offenL + linien;
    // Halte
    var namen = "";
    liste.forEach(function (s) {
      var z = zustand(s), f = STR[s.strang].farbe, cx = xVon(s), cy = yVon(s), schwach = blass(s.id), sel = zustandUI.station === s.id;
      var umstieg = (s.braucht || []).some(function (b) { return S[b] && S[b].strang !== s.strang; });
      var r = (umstieg ? 12 : 9) + (sel ? 2 : 0);
      var g = '<g' + (schwach ? ' opacity="0.25"' : "") + ">";
      g += z === "erreicht" ? '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="' + f + '" stroke="#fff" stroke-width="3"/><circle cx="' + cx + '" cy="' + cy + '" r="' + (r + 1.5) + '" fill="none" stroke="' + f + '" stroke-width="1.5"/>'
        : z === "aktiv" ? '<circle cx="' + cx + '" cy="' + cy + '" r="' + (r + 6) + '" fill="' + f + '" opacity="0.18"/><circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="#fff" stroke="' + f + '" stroke-width="5"/>'
        : '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="#fff" stroke="#111" stroke-width="' + (umstieg ? 4 : 3) + '"/>';
      if (s.kritisch) g += '<circle cx="' + (cx + r + 3) + '" cy="' + (cy - r - 3) + '" r="7" fill="#E8553A"/><text x="' + (cx + r + 3) + '" y="' + (cy - r + 0.6) + '" text-anchor="middle" class="ub-ausruf">!</text>';
      svg += g + "</g>";
      var vonOben = (s.braucht || []).some(function (b) { return imPlan[b] && S[b].strang !== s.strang && yVon(S[b]) < cy; });
      var oben = unter[s.id] === 0 && !vonOben;
      namen += '<button type="button" class="ub-name ub-name--' + z + (oben ? " ub-name--oben" : "") + (schwach ? " ub-name--blass" : "") + (sel ? " ub-name--gewaehlt" : "") +
        '" data-station="' + s.id + '" style="left:' + (cx - (ABST - 14) / 2) + "px;top:" + (oben ? cy - r - 8 : cy + r + 8) + "px;width:" + (ABST - 14) + 'px">' +
        esc(s.titel) + "</button>";
      namen += '<button type="button" class="ub-treffer" data-station="' + s.id + '" aria-label="' + esc(s.titel) + '" style="left:' + (cx - 16) + "px;top:" + (cy - 16) + 'px"></button>';
    });
    // Endhaltestelle
    svg += '<circle cx="' + zielX + '" cy="' + zielY + '" r="24" fill="#fff" stroke="#111" stroke-width="7"/><circle cx="' + zielX + '" cy="' + zielY + '" r="10" fill="#111"/>';
    svg += "</svg>";
    namen += '<div class="ub-endhalt" style="left:' + (zielX + 34) + "px;top:" + zielY + 'px"><b>' + esc(msName(m)) + "</b><small>" + esc(m.termin) + "</small></div>";
    var spalte = bahnen.map(function (st) {
      return '<div class="ub-bahn" style="top:' + (linieY[st.id] - 15) + 'px"><span class="ub-linie" style="background:' + st.farbe + '">' + esc(st.kurz) + "</span><div><b>" + esc(st.label) + "</b><small>" + esc(st.verantwortung) + "</small></div></div>";
    }).join("");
    planEl.innerHTML = '<div class="ub-rahmen"><div class="ub-spalte" style="height:' + hoehe + 'px">' + spalte + '</div><div class="ub-scroll"><div class="ub-flaeche" style="width:' + breite + "px;height:" + hoehe + 'px">' + svg + kopf + namen + "</div></div></div>";
    planEl.querySelectorAll("[data-station]").forEach(function (b) {
      b.addEventListener("click", function () {
        var id = b.getAttribute("data-station");
        zustandUI.station = zustandUI.station === id ? null : id;
        plan(); detail();
      });
    });
    var sc = planEl.querySelector(".ub-scroll");
    // Öffnen dort, wo der Weg gerade frei ist
    if (sc && !zustandUI.station && sc.scrollWidth > sc.clientWidth) {
      var offen = liste.filter(function (s) { return fokus[s.id] && s.status !== "erreicht"; }).map(xVon);
      sc.scrollLeft = offen.length ? Math.max(0, Math.min.apply(null, offen) - 2 * ABST) : 0;
    }
    ziehen(sc);
    var hinweis = null;
    if (hinweis) hinweis.textContent = zustandUI.station
      ? "Hervorgehoben: alles, was vor „" + S[zustandUI.station].titel + "“ erledigt sein muss. Noch einmal klicken hebt die Auswahl auf."
      : m.gesamt ? "Gesamtplan: alle Stufen bis zum Zielbild. Eine Stufe oben wählen, um den Weg dorthin hervorzuheben."
      : "Hervorgehoben: der Weg zur Endhaltestelle „" + msName(m) + "“. Blass: läuft parallel, für diese Stufe nicht nötig.";
  }

  // Plan mit gedrückter Maus nach links und rechts ziehen (Touch scrollt ohnehin)
  var zug = { sc: null, start: null, bewegt: false };
  window.addEventListener("mousemove", function (e) {
    if (!zug.start || !zug.sc) return;
    var dx = e.clientX - zug.start.x;
    if (Math.abs(dx) > 4) { zug.bewegt = true; zug.sc.classList.add("ub-zieht"); }
    zug.sc.scrollLeft = zug.start.l - dx;
  });
  window.addEventListener("mouseup", function () { zug.start = null; if (zug.sc) zug.sc.classList.remove("ub-zieht"); });
  function ziehen(sc) {
    if (!sc) return;
    zug.sc = sc;
    sc.addEventListener("mousedown", function (e) { if (e.button !== 0) return; zug.start = { x: e.clientX, l: sc.scrollLeft }; zug.bewegt = false; });
    sc.addEventListener("click", function (e) { if (zug.bewegt) { e.stopPropagation(); e.preventDefault(); zug.bewegt = false; } }, true);
  }

  /* ---------- Fenster an der Station: knapp, eine Schrift, zwei Größen, zwei Farben ---------- */
  function detail() {
    var alt = planEl.querySelector(".ub-pop"); if (alt) alt.remove();
    var id = zustandUI.station;
    if (!id) return;
    var s = S[id], st = STR[s.strang], z = zustand(s);
    var punkt = planEl.querySelector('.ub-treffer[data-station="' + id + '"]'), flaeche = planEl.querySelector(".ub-flaeche");
    if (!punkt || !flaeche) return;
    var vor = (s.braucht || []).filter(function (b) { return S[b] && S[b].status !== "erreicht"; }).map(function (b) { return S[b].titel; });
    var meta = [st.verantwortung + (s.wer ? " (" + s.wer + ")" : ""), ZTEXT[z]].concat(s.termin ? [s.termin] : []);
    var h = '<p class="ub-pop-titel">' + esc(s.titel) + '</p><p class="ub-pop-meta">' + meta.map(esc).join(" &middot; ") + "</p>";
    if (s.ergebnis) h += "<p>" + esc(s.ergebnis) + "</p>";
    if (s.kritisch) h += "<p>Kritisch: " + esc(s.kritisch.grund) + "</p>";
    if (vor.length) h += '<p class="ub-pop-meta">Braucht vorher: ' + vor.map(esc).join(", ") + "</p>";
    var pop = document.createElement("div");
    pop.className = "ub-pop"; pop.innerHTML = h;
    flaeche.appendChild(pop);
    var px = parseFloat(punkt.style.left) + 16, py = parseFloat(punkt.style.top) + 16;
    var links = Math.min(Math.max(8, px - 150), flaeche.offsetWidth - 308);
    var unten = py + 34 + pop.offsetHeight < flaeche.offsetHeight || py < pop.offsetHeight + 40;
    pop.style.left = links + "px";
    pop.style.top = (unten ? py + 34 : py - 34 - pop.offsetHeight) + "px";
  }
  // Klick irgendwo daneben löst die Auswahl
  document.addEventListener("click", function (e) {
    if (infoPop && !e.target.closest(".ub-pop--info")) infoZu();
    if (!zustandUI.station) return;
    if (e.target.closest(".ub-name, .ub-treffer, .ub-pop")) return;
    zustandUI.station = null; plan(); detail();
  });

  stufen(); plan(); detail();
})();
