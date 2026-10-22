/* Sicht 1.2 – näher am U-Bahn-Plan aus Sicht 2 (Daniel, 22.10.2026)
   Alle Linien gleich dick. Hellgrau = noch nicht gefahren, Linienfarbe = gefahren bis zum laufenden Halt.
   Halte weiß, Zustand über den Rand. Steuerung (Stufen als Kästen, Legende) in eigener Karte über dem Plan.
   ---
   Sicht 1.1 – vereinfachte Weiterentwicklung von Sicht 1 (Daniel, 22.10.2026)
   Dick ist der Weg bis zu allem, was erledigt ist oder läuft; dünn der Rest. Ergebnisstufen-Balken liegen
   immer oben. Halte ohne Hof. Sonst wie Sicht 1.
   ---
   U-Bahn-Plan „Vom Ergebnis her gedacht“ – SV Akademie (Daniel, 22.10.2026)
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
  function msName(m) { return m.titel || "Ergebnislevel " + m.nr; }
  function stufeErreicht(mid) { return (MS[mid].braucht || []).every(function (b) { return S[b] && S[b].status === "erreicht"; }); }
  function fertig(id) { return MS[id] ? stufeErreicht(id) : S[id] && S[id].status === "erreicht"; }
  function zustand(s) {
    if (s.status === "erreicht") return "erreicht";
    if (s.status === "aktiv") return "aktiv";
    return (s.braucht || []).every(fertig) ? "frei" : "wartet";
  }
  var ZTEXT = { erreicht: "erledigt", aktiv: "in Arbeit", frei: "kann starten", wartet: "wartet auf Vorarbeit" };
  function vorlauf(ids) {               // alles, was in diese Schritte einfließt – inklusive der Schritte selbst
    var drin = {}, st = ids.slice();
    while (st.length) {
      var id = st.pop();
      if (MS[id]) { (MS[id].braucht || []).forEach(function (b) { st.push(b); }); continue; }   // Stufe als Voraussetzung
      if (drin[id] || !S[id]) continue; drin[id] = true; (S[id].braucht || []).forEach(function (b) { st.push(b); });
    }
    return drin;
  }

  // „ziel“ = Gesamtplan: alle Stufen bis zum Zielbild, nichts wird blass
  var ZIEL = { id: "ziel", i: D.meilensteine.length - 1, nr: "", titel: D.zielbild.kurz || "Zielbild", termin: "Ende des Projekts", braucht: null, gesamt: true };
  function msVon(id) { return id === "ziel" ? ZIEL : MS[id]; }
  var zustandUI = { ms: (function () { var h = location.hash.replace("#", ""); return MS[h] || h === "ziel" ? h : D.meilensteine[0].id; })(), station: null };
  var stufenEl = document.getElementById("ub-stufen"), planEl = document.getElementById("ub-plan"), detailEl = document.getElementById("ub-detail");

  /* ---------- Ergebnisstufen als Reiter, Erklärung und Legende als kleines Fenster ---------- */
  // Ergebnisstufen als Kästen: oben „Stufe n · Datum“, darunter Titel oder Kern des Ergebnisses (höchstens zwei Zeilen).
  // Ein Klick auf den Kasten wechselt die Stufe; das ⓘ im Kasten öffnet „Erreicht, wenn …“ direkt darunter.
  function kastenText(x) { return x.titel || ((x.ergebnis || [])[0] || "Level " + x.nr).split(":")[0].replace(/\.$/, ""); }
  function stufen() {
    var h = '<div class="ub-kaesten" role="tablist">';
    D.meilensteine.forEach(function (x) {
      h += '<div role="tab" tabindex="0" class="ub-kasten" data-ms="' + x.id + '" aria-selected="' + (x.id === zustandUI.ms) + '">' +
        '<small>Level ' + x.nr + " &middot; " + esc(x.termin) + "</small><b>" + esc(kastenText(x)) + "</b>" +
        '<button type="button" class="ub-kasten-info" data-info-ms="' + x.id + '" aria-label="Erreicht, wenn …">+</button></div>';
    });
    h += '<div role="tab" tabindex="0" class="ub-kasten ub-kasten--ziel" data-ms="ziel" aria-selected="' + (zustandUI.ms === "ziel") + '">' +
      "<small>Ziel &middot; alle Level</small><b>Gesamtplan</b>" +
      '<button type="button" class="ub-kasten-info" data-info-ms="ziel" aria-label="Zielbild">+</button></div></div>';
    stufenEl.innerHTML = h;
    stufenEl.querySelectorAll("[data-ms]").forEach(function (k) {
      function waehlen() {
        zustandUI.ms = k.getAttribute("data-ms"); zustandUI.station = null;
        history.replaceState(null, "", "#" + zustandUI.ms);
        infoZu(); stufen(); plan(); detail();
      }
      k.addEventListener("click", waehlen);
      k.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); waehlen(); } });
    });
    stufenEl.querySelectorAll("[data-info-ms]").forEach(function (b) {
      b.addEventListener("click", function (e) {
        e.stopPropagation();
        var id = b.getAttribute("data-info-ms"), offen = infoPop && infoPop.getAttribute("data-fuer") === id;
        infoZu();
        if (offen) return;
        var kasten = b.closest(".ub-kasten");
        infoPop = document.createElement("div");
        infoPop.className = "ub-pop ub-pop--info";
        infoPop.setAttribute("data-fuer", id);
        infoPop.innerHTML = infoInhalt(id);
        stufenEl.appendChild(infoPop);
        infoPop.style.left = Math.min(kasten.offsetLeft, stufenEl.offsetWidth - infoPop.offsetWidth) + "px";
        infoPop.style.top = (kasten.offsetTop + kasten.offsetHeight + 8) + "px";
        b.setAttribute("aria-expanded", "true");
      });
    });
  }
  function infoInhalt(id) {
    if (id === "ziel") {
      var zb = D.zielbild.text && D.zielbild.text.indexOf("Platzhalter") < 0 ? D.zielbild.text : "";
      return '<p class="ub-pop-titel">' + esc(ZIEL.titel) + '</p><p class="ub-pop-meta">Zielbild</p><p>' + (zb ? esc(zb) : "Das Zielbild wird noch beschrieben.") + "</p>";
    }
    var m = MS[id];
    return '<p class="ub-pop-titel">' + esc(msName(m)) + '</p><p class="ub-pop-meta">Level ' + m.nr + " &middot; " + esc(m.termin) + " &middot; erreicht, wenn</p><ul>" +
      (m.ergebnis || []).map(function (e) { return "<li>" + esc(e) + "</li>"; }).join("") + "</ul>";
  }
  var infoPop = null;
  function infoZu() {
    if (infoPop) { infoPop.remove(); infoPop = null; }
    document.querySelectorAll(".ub-kasten-info").forEach(function (b) { b.setAttribute("aria-expanded", "false"); });
  }

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
    // Ausschnitt: eine Stufe zeigt nur ihre eigenen Halte; der Gesamtplan zeigt alle
    var stufenImBlick = D.meilensteine.filter(function (x) { return m.gesamt || x.id === m.id; });
    var imBlick = {}; stufenImBlick.forEach(function (x) { imBlick[x.id] = true; });
    var liste = D.schritte.filter(function (s) { return imBlick[s.meilenstein]; });
    var imPlan = {}; liste.forEach(function (s) { imPlan[s.id] = true; });
    var vorStufe = m.gesamt ? null : D.meilensteine[m.i - 1] || null;   // Starthalt: die Stufe davor
    var fokus = zustandUI.station ? vorlauf([zustandUI.station]) : m.gesamt ? imPlan : vorlauf(m.braucht || []);
    function blass(id) { return !fokus[id]; }

    var tiefe = {};
    function t(id) {
      if (tiefe[id] != null) return tiefe[id];
      var s = S[id], v = (s.braucht || []).filter(function (b) { return imPlan[b] && S[b].meilenstein === s.meilenstein; });
      return (tiefe[id] = v.length ? 1 + Math.max.apply(null, v.map(t)) : 0);
    }
    liste.forEach(function (s) { t(s.id); });
    var bandStart = {}, bandBreite = {}, lauf = 0, nr = 0, bandNr = {};
    stufenImBlick.forEach(function (x) {
      var w = 1; liste.forEach(function (s) { if (s.meilenstein === x.id) w = Math.max(w, tiefe[s.id] + 1); });
      bandStart[x.id] = lauf; bandBreite[x.id] = w; bandNr[x.id] = nr++; lauf += w;
    });
    var HALT = 64;                               // Platz für einen Stufenhalt zwischen zwei Bändern
    var START = vorStufe ? 70 : EINLAUF;         // links: Starthalt der Stufe davor
    var verfuegbar = planEl.clientWidth - SPALTE;
    ABST = Math.max(108, Math.min(140, (verfuegbar - START - HALT * (nr - 1) - 190) / lauf));
    function xVon(s) { var x = MS[s.meilenstein]; return START + (bandStart[x.id] + tiefe[s.id]) * ABST + bandNr[x.id] * HALT + ABST / 2; }
    function xHalt(mid) { return START + (bandStart[mid] + bandBreite[mid]) * ABST + bandNr[mid] * HALT + 14; }   // Stufenhalt nach dem Band

    var unter = {}, gruppen = {}, tiefsteZeile = {};
    liste.forEach(function (s) {
      var k = s.strang + "|" + s.meilenstein + "|" + tiefe[s.id];
      gruppen[k] = (gruppen[k] || 0); unter[s.id] = gruppen[k]++;
      tiefsteZeile[s.strang] = Math.max(tiefsteZeile[s.strang] || 0, unter[s.id]);
    });
    var bahnen = D.straenge.filter(function (st) { return liste.some(function (s) { return s.strang === st.id; }); });
    var linieY = {}, y0 = nr > 1 ? 46 : 8;   // oben eine Zeile für die Namen der Stufenhalte (nur im Gesamtplan)
    bahnen.forEach(function (st) { linieY[st.id] = y0 + UEBER; y0 += UEBER + tiefsteZeile[st.id] * ZH + (tiefsteZeile[st.id] ? UNTER + 34 : UNTER); });
    var hoehe = y0 + 6 + (vorStufe ? 22 : 0);   // unten Platz für „Voraussetzung: …“
    function yVon(s) { return linieY[s.strang] + unter[s.id] * ZH; }
    var letzte = stufenImBlick[stufenImBlick.length - 1];
    var breite = xHalt(letzte.id) + 190;
    var obenAlle = Math.min.apply(null, bahnen.map(function (st) { return linieY[st.id]; })) - 18;
    var untenAlle = Math.max.apply(null, bahnen.map(function (st) { return linieY[st.id]; })) + 18;

    var svg = '<svg width="' + breite + '" height="' + hoehe + '" class="ub-svg" aria-hidden="true">';
    var duenn = "", dick = "", quer = "", halte = "", namen = "", durch = "";
    function strecke(pkte, farbe, gegangen, schwach) {
      // gleiche Dicke: gefahren in Linienfarbe, noch nicht gefahren hellgrau (blass: noch heller)
      var f = gegangen ? (schwach ? hell(farbe, 0.8) : farbe) : (schwach ? "#f0ede9" : "#dedad4");
      var html = '<path d="' + rund(pkte) + '" stroke="' + f + '" fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="8"/>';
      if (gegangen) dick += html; else duenn += html;
    }
    function weg(x1, y1, x2, y2, rueck) {
      if (Math.abs(y1 - y2) < 1) return [[x1, y1], [x2, y2]];
      var xs = rueck ? x1 + ABST / 2 : x2 - ABST / 2;
      return [[x1, y1], [xs, y1], [xs, y2], [x2, y2]];
    }
    function freiStart(v) {   // ohne Zuführung: keine Stufe, keine frühere Vorarbeit, kein Vorgänger auf der eigenen Linie
      return !(v.braucht || []).some(function (b) { return MS[b] || !imPlan[b] || S[b].strang === v.strang; });
    }
    // Woher kommt eine Strecke in den Halt? aus der eigenen Linie, aus einem Stufenhalt – oder frei
    liste.forEach(function (s) {
      var f = STR[s.strang].farbe, x2 = xVon(s), y2 = yVon(s), linieRein = false;
      (s.braucht || []).forEach(function (b) {
        if (MS[b]) {                                             // startet, sobald eine Stufe erreicht ist
          var hx = imBlick[b] ? xHalt(b) + 13 : vorStufe ? 34 : 0;   // aus dem Stufenhalt – nie links daran vorbei
          strecke(weg(hx, linieY[s.strang], x2, y2, false), f, s.status !== "offen", blass(s.id)); linieRein = true; return;
        }
        if (!imPlan[b]) {                                        // Vorarbeit aus einer früheren Stufe: kommt aus dem Starthalt
          if (!linieRein) strecke(weg(vorStufe ? 34 : 0, linieY[s.strang], x2, y2, false), f, s.status !== "offen", blass(s.id));
          linieRein = true; return;
        }
        var v = S[b], x1 = xVon(v), y1 = yVon(v);
        if (v.strang === s.strang) {
          // frei beginnender Strang auf einer Nebenstrecke bleibt auf seiner Strecke und mündet erst kurz vor dem Halt ein
          var pk = weg(x1, y1, x2, y2, unter[b] > unter[s.id] && !freiStart(v));
          var nachMain = function (id) { return liste.some(function (n) { return n.strang === s.strang && unter[n.id] === 0 && (n.braucht || []).indexOf(id) > -1; }); };
          var vorMain = function (n) { return (n.braucht || []).some(function (x) { return imPlan[x] && S[x].strang === n.strang && unter[x] === 0; }); };
          if (pk.length === 4 && unter[b] === 0 && unter[s.id] > 0 && nachMain(b)) pk = pk.slice(1);
          else if (pk.length === 4 && unter[b] > 0 && unter[s.id] === 0 && vorMain(s)) pk = pk.slice(0, 3);
          // läuft über eine Stufengrenze hinweg: direkte Verbindung – wird über dem Stufenhalt gezeichnet
          strecke(pk, f, s.status !== "offen", blass(s.id) || blass(b));
          linieRein = true;
        } else {
          var dir = y2 > y1 ? 1 : -1, yk = y2 - dir * 26;
          quer += '<path d="' + rund([[x1, y1], [x1, yk], [x2, yk], [x2, y2]]) + '" stroke="' + (blass(s.id) ? "#dedad4" : "#8a857d") + '" stroke-width="2" fill="none" stroke-dasharray="3 5"/>';
        }
      });
      // frei startend: eigene kurze Strecke mit Kopfbahnhof (Querstrich) – „kann sofort los“
      if (!linieRein) {
        var xa = x2 - ABST * 0.42, geg = s.status !== "offen";
        strecke([[xa, y2], [x2, y2]], f, geg, blass(s.id));
        strecke([[xa, y2 - 9], [xa, y2 + 9]], f, geg, blass(s.id));
      }
      // Auslauf: Halt ohne Nachfolger auf der eigenen Linie endet im Stufenhalt seiner Stufe, wenn er einfließt
      var weiter = D.schritte.some(function (n) { return n.strang === s.strang && imPlan[n.id] && (n.braucht || []).indexOf(s.id) > -1; });
      if (!weiter) {
        var ms = MS[s.meilenstein], rein = fokus[s.id] && vorlauf(ms.braucht || [])[s.id] && !zustandUI.station;
        var ende = rein ? xHalt(ms.id) : xVon(s) + ABST / 2;
        strecke(weg(x2, y2, ende, linieY[s.strang], true), f, false, !rein && blass(s.id));
      }
    });
    // Stufenhalte: Balken über alle Linien; der gewählte bzw. letzte kräftig, Zwischenhalte etwas schmaler
    function balken(x, stark, grau) {
      return '<rect x="' + x + '" y="' + obenAlle + '" width="26" height="' + (untenAlle - obenAlle) + '" rx="13" fill="#fff" stroke="' + (grau ? "#a39e96" : "#111") + '" stroke-width="' + (stark ? 6 : 4) + '"/>';
    }
    stufenImBlick.forEach(function (x) {
      var hx = xHalt(x.id), letzter = x.id === letzte.id;
      halte += balken(hx, letzter, false);
      namen += '<div class="ub-halt-name' + (letzter ? " ub-halt-name--ende" : "") + '" style="left:' + (letzter ? hx + 36 : hx + 13) + "px;top:" + (letzter ? (obenAlle + untenAlle) / 2 : 4) + 'px"><b>' +
        esc(msName(x)) + "</b><small>" + (stufeErreicht(x.id) ? "erreicht" : "Level " + x.nr + " &middot; " + esc(x.termin)) + "</small></div>";
    });
    if (vorStufe) {
      halte += balken(8, false, true);
      namen += '<div class="ub-halt-name ub-halt-name--start" style="left:8px;top:' + (untenAlle + 8) + 'px"><small>Voraussetzung: ' + esc(msName(vorStufe)) + (stufeErreicht(vorStufe.id) ? " (erreicht)" : " (noch offen)") + "</small></div>";
    }
    svg += quer + duenn + dick;
    var punkte = "";   // Halte zuletzt, damit keine Linie sie überdeckt
    liste.forEach(function (s) {
      var z = zustand(s), f = STR[s.strang].farbe, cx = xVon(s), cy = yVon(s), schwach = blass(s.id), sel = zustandUI.station === s.id;
      var umstieg = (s.braucht || []).some(function (b) { return imPlan[b] && S[b].strang !== s.strang; });
      var r = z === "aktiv" ? 11 : z === "erreicht" ? 6 : (umstieg ? 10 : 8);
      if (sel) r += 2;
      // Halte weiß wie im Liniennetzplan: erledigt klein mit Rand in Linienfarbe, in Arbeit groß mit schwarzem Rand, kommt noch grau
      punkte += z === "erreicht" ? '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="#fff" stroke="' + (schwach ? hell(f, 0.8) : f) + '" stroke-width="2.5"/>'
        : z === "aktiv" ? '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="#fff" stroke="' + (schwach ? "#c9c5bf" : "#111") + '" stroke-width="4.5"/>'
        : '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="#fff" stroke="' + (schwach ? "#e8e5e0" : "#a39e96") + '" stroke-width="' + (umstieg ? 3.5 : 3) + '"/>';
      if (s.kritisch) punkte += '<circle cx="' + (cx + r + 3) + '" cy="' + (cy - r - 3) + '" r="7" fill="' + (schwach ? "#f6c9bf" : "#E8553A") + '"/><text x="' + (cx + r + 3) + '" y="' + (cy - r + 0.6) + '" text-anchor="middle" class="ub-ausruf">!</text>';
      var vonOben = (s.braucht || []).some(function (b) { return imPlan[b] && S[b].strang !== s.strang && yVon(S[b]) < cy; });
      var obenL = unter[s.id] === 0 && !vonOben;
      namen += '<button type="button" class="ub-name ub-name--' + z + (obenL ? " ub-name--oben" : "") + (schwach ? " ub-name--blass" : "") +
        '" data-station="' + s.id + '" style="left:' + (cx - (ABST - 14) / 2) + "px;top:" + (obenL ? cy - r - 8 : cy + r + 8) + "px;width:" + (ABST - 14) + 'px">' + esc(s.titel) + "</button>";
      namen += '<button type="button" class="ub-treffer" data-station="' + s.id + '" aria-label="' + esc(s.titel) + '" style="left:' + (cx - 16) + "px;top:" + (cy - 16) + 'px"></button>';
    });
    svg += halte + durch + punkte + "</svg>";
    var spalte = bahnen.map(function (st) {
      return '<div class="ub-bahn" style="top:' + (linieY[st.id] - 15) + 'px"><span class="ub-linie" style="background:' + st.farbe + '">' + esc(st.kurz) + "</span><div><b>" + esc(st.label) + "</b><small>" + esc(st.verantwortung) + "</small></div></div>";
    }).join("");
    planEl.innerHTML = '<div class="ub-rahmen"><div class="ub-spalte" style="height:' + hoehe + 'px">' + spalte + '</div><div class="ub-scroll"><div class="ub-flaeche" style="width:' + breite + "px;height:" + hoehe + 'px">' + svg + namen + "</div></div></div>";
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
    // Position wählen, die keinen Halt auf dem Weg dorthin verdeckt (Reihenfolge: rechts, unten, oben, links)
    var W = pop.offsetWidth, H = pop.offsetHeight, FW = flaeche.offsetWidth, FH = flaeche.offsetHeight;
    var weg = vorlauf([id]), halte = [];
    planEl.querySelectorAll(".ub-treffer").forEach(function (t) {
      if (t.getAttribute("data-station") === id) return;
      halte.push({ x: parseFloat(t.style.left) + 16, y: parseFloat(t.style.top) + 16, wichtig: !!weg[t.getAttribute("data-station")] });
    });
    var kandidaten = [[px + 70, py - 24], [px - W / 2, py + 64], [px - W / 2, py - H - 64], [px - 70 - W, py - 24]];
    var best = null;
    kandidaten.forEach(function (k, i) {
      var x = Math.min(Math.max(4, k[0]), FW - W - 4), y = Math.min(Math.max(4, k[1]), FH - H - 4), wert = i * 0.1;
      halte.forEach(function (h) {   // Halt samt Namen: etwas Rand um den Punkt
        if (h.x > x - 50 && h.x < x + W + 50 && h.y > y - 50 && h.y < y + H + 40) wert += h.wichtig ? 10 : 1;
      });
      if (!best || wert < best.w) best = { x: x, y: y, w: wert };
    });
    pop.style.left = best.x + "px";
    pop.style.top = best.y + "px";
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
