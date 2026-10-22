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
  // Nur waagerecht und senkrecht, Ecken leicht gerundet – wie ein Liniennetzplan.
  // Hauptlinie je Stoßrichtung (Beschriftung darüber), parallele Halte auf Nebenstrecken darunter (Beschriftung darunter).
  // Eine Nebenstrecke zweigt in der Lücke vor ihrem Halt ab und kehrt in der Lücke danach zurück.
  // Endhaltestelle: senkrechter Balken, in den jede beteiligte Linie waagerecht auf ihrer Höhe einläuft.
  // Keine Transparenz: helle Töne sind echte Mischfarben mit Weiß, damit Überlagerungen nicht dunkler werden.
  var ABST = 136, ZH = 72, UEBER = 64, UNTER = 44, LUECKE = 40, EINLAUF = 26, SPALTE = 190;
  function hell(hex, t) {   // Farbe mit Weiß mischen, t = Anteil Weiß
    var n = parseInt(hex.slice(1), 16), r = n >> 16, g = (n >> 8) & 255, b = n & 255;
    function m(c) { return Math.round(c + (255 - c) * t); }
    return "rgb(" + m(r) + "," + m(g) + "," + m(b) + ")";
  }
  function rund(pkte) {     // Polylinie mit gerundeten Ecken
    var R = 10, d = "M" + pkte[0][0] + "," + pkte[0][1];
    for (var i = 1; i < pkte.length - 1; i++) {
      var p0 = pkte[i - 1], p1 = pkte[i], p2 = pkte[i + 1];
      var l1 = Math.hypot(p1[0] - p0[0], p1[1] - p0[1]), l2 = Math.hypot(p2[0] - p1[0], p2[1] - p1[1]);
      var r = Math.min(R, l1 / 2, l2 / 2);
      if (!r) { d += " L" + p1[0] + "," + p1[1]; continue; }
      var a = [p1[0] - (p1[0] - p0[0]) / l1 * r, p1[1] - (p1[1] - p0[1]) / l1 * r];
      var b = [p1[0] + (p2[0] - p1[0]) / l2 * r, p1[1] + (p2[1] - p1[1]) / l2 * r];
      d += " L" + a[0] + "," + a[1] + " Q" + p1[0] + "," + p1[1] + " " + b[0] + "," + b[1];
    }
    var e = pkte[pkte.length - 1];
    return d + " L" + e[0] + "," + e[1];
  }
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
    var verfuegbar = planEl.clientWidth - SPALTE;
    ABST = Math.max(108, Math.min(140, (verfuegbar - EINLAUF - LUECKE * m.i - 200) / lauf));
    function xVon(s) { var k = MS[s.meilenstein].i; return EINLAUF + (bandStart[k] + tiefe[s.id]) * ABST + k * LUECKE + ABST / 2; }
    function xGrenze(k) { return EINLAUF + (bandStart[k] + bandBreite[k]) * ABST + k * LUECKE + LUECKE / 2; }

    var unter = {}, gruppen = {}, tiefsteZeile = {};
    liste.forEach(function (s) {
      var k = s.strang + "|" + s.meilenstein + "|" + tiefe[s.id];
      gruppen[k] = (gruppen[k] || 0); unter[s.id] = gruppen[k]++;
      tiefsteZeile[s.strang] = Math.max(tiefsteZeile[s.strang] || 0, unter[s.id]);
    });
    var bahnen = D.straenge.filter(function (st) { return liste.some(function (s) { return s.strang === st.id; }); });
    var linieY = {}, y0 = m.i > 0 ? 26 : 6;
    bahnen.forEach(function (st) { linieY[st.id] = y0 + UEBER; y0 += UEBER + tiefsteZeile[st.id] * ZH + (tiefsteZeile[st.id] ? UNTER + 34 : UNTER); });
    var hoehe = y0 + 6;
    function yVon(s) { return linieY[s.strang] + unter[s.id] * ZH; }

    // Endhaltestelle: Balken über alle Linien, die einfließen
    var zielX = xGrenze(m.i) + 34;
    var zielBahnen = zustandUI.station ? [] : bahnen.filter(function (st) { return liste.some(function (s) { return s.strang === st.id && fokus[s.id]; }); });
    var breite = zielX + 170;

    var svg = '<svg width="' + breite + '" height="' + hoehe + '" class="ub-svg" aria-hidden="true">';
    var kopf = "", duenn = "", dick = "", quer = "";
    D.meilensteine.forEach(function (x) {
      if (x.i >= m.i) return;
      var gx = xGrenze(x.i);
      svg += '<line x1="' + gx + '" y1="22" x2="' + gx + '" y2="' + (hoehe - 4) + '" class="ub-grenze"/>';
      kopf += '<div class="ub-grenze-name" style="left:' + gx + 'px">Stufe ' + x.nr + " &middot; " + esc(msName(x)) + "</div>";
    });
    function strecke(pkte, farbe, gegangen, schwach) {
      var f = schwach ? hell(farbe, 0.88) : gegangen ? farbe : hell(farbe, 0.55);
      var html = '<path d="' + rund(pkte) + '" stroke="' + f + '" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="' + (gegangen ? 9 : 4) + '"/>';
      if (gegangen) dick += html; else duenn += html;
    }
    // Weg zwischen zwei Halten derselben Linie: Abzweig in der Lücke vor dem Ziel, Rückkehr in der Lücke danach
    function weg(x1, y1, x2, y2, rueck) {
      if (Math.abs(y1 - y2) < 1) return [[x1, y1], [x2, y2]];
      var xs = rueck ? x1 + ABST / 2 : x2 - ABST / 2;
      return [[x1, y1], [xs, y1], [xs, y2], [x2, y2]];
    }
    bahnen.forEach(function (st) {
      var eig = liste.filter(function (s) { return s.strang === st.id; }), y = linieY[st.id];
      // Einlauf aus der Spalte bis zu den ersten Halten
      eig.filter(function (s) { return !(s.braucht || []).some(function (b) { return imPlan[b] && S[b].strang === st.id; }); }).forEach(function (s) {
        strecke(weg(0, y, xVon(s), yVon(s), false), st.farbe, s.status !== "offen", blass(s.id));
      });
      // Auslauf: in die Endhaltestelle, wenn die Linie einfließt – sonst endet sie an der Stufengrenze
      var rein = zielBahnen.indexOf(st) > -1;
      eig.filter(function (s) { return !liste.some(function (n) { return n.strang === st.id && (n.braucht || []).indexOf(s.id) > -1; }); }).forEach(function (s) {
        var ende = rein && fokus[s.id] ? zielX : xGrenze(m.i) - 6;
        strecke(weg(xVon(s), yVon(s), ende, y, true), st.farbe, false, !(rein && fokus[s.id]));
      });
    });
    liste.forEach(function (s) {
      (s.braucht || []).forEach(function (b) {
        if (!imPlan[b]) return;
        var v = S[b], x1 = xVon(v), y1 = yVon(v), x2 = xVon(s), y2 = yVon(s);
        if (v.strang === s.strang) {
          var pk = weg(x1, y1, x2, y2, unter[b] > unter[s.id]);
          // Wo die Hauptlinie ohnehin weiterläuft, zeichnet die Nebenstrecke nur ihren eigenen Abschnitt –
          // doppelt gezeichnete Strecken wirken sonst an den Kanten dunkler
          var nachMain = function (id) { return liste.some(function (n) { return n.strang === s.strang && unter[n.id] === 0 && (n.braucht || []).indexOf(id) > -1; }); };
          var vorMain = function (n) { return (n.braucht || []).some(function (x) { return imPlan[x] && S[x].strang === n.strang && unter[x] === 0; }); };
          if (pk.length === 4 && unter[b] === 0 && unter[s.id] > 0 && nachMain(b)) pk = pk.slice(1);
          else if (pk.length === 4 && unter[b] > 0 && unter[s.id] === 0 && vorMain(s)) pk = pk.slice(0, 3);
          strecke(pk, STR[s.strang].farbe, v.status === "erreicht", blass(s.id) || blass(b));
        } else {
          // Umstieg: senkrecht aus dem Halt, kurz vor der Ziellinie waagerecht, senkrecht in den Halt –
          // läuft nie auf einer Strecke entlang
          var dir = y2 > y1 ? 1 : -1, yk = y2 - dir * 26;
          quer += '<path d="' + rund([[x1, y1], [x1, yk], [x2, yk], [x2, y2]]) + '" stroke="' + (blass(s.id) ? "#dedad4" : "#8a857d") + '" stroke-width="2" fill="none" stroke-dasharray="3 5"/>';
        }
      });
    });
    svg += quer + duenn + dick;
    // Endhaltestelle
    if (zielBahnen.length) {
      var ys = zielBahnen.map(function (st) { return linieY[st.id]; }), oben = Math.min.apply(null, ys) - 16, unten = Math.max.apply(null, ys) + 16;
      svg += '<rect x="' + (zielX - 4) + '" y="' + oben + '" width="30" height="' + (unten - oben) + '" rx="15" fill="#fff" stroke="#111" stroke-width="6"/>';
    }
    // Halte
    var namen = "";
    liste.forEach(function (s) {
      var z = zustand(s), f = STR[s.strang].farbe, cx = xVon(s), cy = yVon(s), schwach = blass(s.id), sel = zustandUI.station === s.id;
      var umstieg = (s.braucht || []).some(function (b) { return imPlan[b] && S[b].strang !== s.strang; });
      // Rangfolge der Aufmerksamkeit: in Arbeit stark, erledigt klein und ruhig, künftig grau
      var r = z === "aktiv" ? 10 : z === "erreicht" ? 6 : (umstieg ? 9 : 7);
      if (sel) r += 2;
      var g = z === "erreicht" ? '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="' + (schwach ? hell(f, 0.8) : f) + '" stroke="#fff" stroke-width="2"/>'
        : z === "aktiv" ? '<circle cx="' + cx + '" cy="' + cy + '" r="' + (r + 6) + '" fill="' + hell(f, schwach ? 0.93 : 0.8) + '"/><circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="#fff" stroke="' + (schwach ? hell(f, 0.8) : f) + '" stroke-width="5"/>'
        : '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="#fff" stroke="' + (schwach ? "#e2ded8" : "#a39e96") + '" stroke-width="' + (umstieg ? 3.5 : 2.5) + '"/>';
      if (s.kritisch) g += '<circle cx="' + (cx + r + 3) + '" cy="' + (cy - r - 3) + '" r="7" fill="' + (schwach ? "#f6c9bf" : "#E8553A") + '"/><text x="' + (cx + r + 3) + '" y="' + (cy - r + 0.6) + '" text-anchor="middle" class="ub-ausruf">!</text>';
      svg += g;
      var vonOben = (s.braucht || []).some(function (b) { return imPlan[b] && S[b].strang !== s.strang && yVon(S[b]) < cy; });
      var obenL = unter[s.id] === 0 && !vonOben;
      namen += '<button type="button" class="ub-name ub-name--' + z + (obenL ? " ub-name--oben" : "") + (schwach ? " ub-name--blass" : "") +
        '" data-station="' + s.id + '" style="left:' + (cx - (ABST - 14) / 2) + "px;top:" + (obenL ? cy - r - 8 : cy + r + 8) + "px;width:" + (ABST - 14) + 'px">' + esc(s.titel) + "</button>";
      namen += '<button type="button" class="ub-treffer" data-station="' + s.id + '" aria-label="' + esc(s.titel) + '" style="left:' + (cx - 16) + "px;top:" + (cy - 16) + 'px"></button>';
    });
    svg += "</svg>";
    if (zielBahnen.length) {
      var my = zielBahnen.reduce(function (a, st) { return a + linieY[st.id]; }, 0) / zielBahnen.length;
      namen += '<div class="ub-endhalt" style="left:' + (zielX + 38) + "px;top:" + my + 'px"><b>' + esc(msName(m)) + "</b><small>" + esc(m.termin) + "</small></div>";
    }
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
    if (sc && !zustandUI.station && sc.scrollWidth > sc.clientWidth) {
      var offen = liste.filter(function (s) { return fokus[s.id] && s.status !== "erreicht"; }).map(xVon);
      sc.scrollLeft = offen.length ? Math.max(0, Math.min.apply(null, offen) - 2 * ABST) : 0;
    }
    ziehen(sc);
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
