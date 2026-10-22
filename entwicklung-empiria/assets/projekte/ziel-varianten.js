/* Zielansichten SV Akademie (Daniel, 22.10.2026)
   Logik: Vom Endergebnis her denken. Jeder Ergebnismeilenstein beschreibt im Präsens den Zustand,
   den wir erreicht haben, und nennt die Ergebnisse, die er unmittelbar braucht (meilensteine[].braucht).
   Was davor einfließt, folgt aus schritte[].braucht – auch über Stoßrichtungen und frühere Meilensteine hinweg.
   Zustand je Schritt: erledigt · jetzt dran (alles davor erledigt) · wartet.
   Drei Darstellungen derselben Daten: Zuflussplan, U-Bahn-Plan, Startfreigabe (body[data-variante]). */
(function () {
  "use strict";
  var D = window.ZIEL_DATEN;
  if (!D) return;
  var VARIANTE = document.body.getAttribute("data-variante") || "zufluss";
  var S = {}, STRANG = {}, MS = {};
  D.schritte.forEach(function (s) { S[s.id] = s; });
  D.straenge.forEach(function (s, i) { s.index = i; STRANG[s.id] = s; });
  D.meilensteine.forEach(function (m, i) { m.index = i; MS[m.id] = m; });

  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function msName(m) { return m.titel || ("Ergebnisstufe " + m.nr); }
  function erledigt(id) { return S[id] && (S[id].status === "erledigt" || S[id].status === "erreicht"); }
  function zustand(id) {
    if (S[id] && S[id].pseudo) return S[id].offen.length ? (S[id].dran.length ? "dran" : "wartet") : "fertig";
    if (erledigt(id)) return "fertig";
    return (S[id].braucht || []).every(erledigt) ? "dran" : "wartet";
  }
  // Alles, was in einen Meilenstein einfließt (transitiv über braucht)
  function zufluss(m) {
    var drin = {}, stapel = (m.braucht || []).slice();
    while (stapel.length) {
      var id = stapel.pop();
      if (drin[id] || !S[id]) continue;
      drin[id] = true;
      (S[id].braucht || []).forEach(function (b) { stapel.push(b); });
    }
    return D.schritte.filter(function (s) { return drin[s.id]; });
  }
  // Tiefe = längster Weg von einem Anfang (für die Spalten)
  function tiefen(liste) {
    var t = {}, ids = {};
    liste.forEach(function (s) { ids[s.id] = s; });   // die Liste kann verdichtet sein – ihre eigenen Abhängigkeiten zählen
    function tiefe(id) {
      if (t[id] != null) return t[id];
      var v = (ids[id].braucht || []).filter(function (b) { return ids[b]; });
      t[id] = v.length ? 1 + Math.max.apply(null, v.map(tiefe)) : 0;
      return t[id];
    }
    liste.forEach(function (s) { tiefe(s.id); });
    return t;
  }
  function wartetAuf(s, liste) {
    return (s.braucht || []).filter(function (b) { return !erledigt(b); }).map(function (b) { return S[b].titel; });
  }

  // Frühere Stufen je Stoßrichtung zu einer Voraussetzung zusammenfassen – sonst wird der Plan
  // bei späteren Meilensteinen unlesbar. Die Abhängigkeit bleibt sichtbar: erst das, dann das.
  function verdichten(liste) {
    var idx = MS[gewaehlt].index, vor = {}, ersatz = {};
    liste.forEach(function (s) {
      if (MS[s.meilenstein].index >= idx) return;
      var k = "vor-" + s.strang;
      if (!vor[k]) vor[k] = { id: k, strang: s.strang, pseudo: true, mitglieder: [], braucht: [], meilenstein: s.meilenstein };
      vor[k].mitglieder.push(s);
      ersatz[s.id] = k;
    });
    var stufen = {};
    Object.keys(vor).forEach(function (k) {
      var v = vor[k], ms = {};
      v.mitglieder.forEach(function (m) { ms[MS[m.meilenstein].nr] = MS[m.meilenstein]; stufen[MS[m.meilenstein].nr] = MS[m.meilenstein]; });
      var nrn = Object.keys(ms).map(Number).sort();
      v.titel = nrn.length === 1 ? "Vorher: " + msName(ms[nrn[0]]) : "Vorher: Stufen " + nrn[0] + "\u2013" + nrn[nrn.length - 1];
      v.offen = v.mitglieder.filter(function (m) { return !erledigt(m.id); });
      v.dran = v.mitglieder.filter(function (m) { return zustand(m.id) === "dran"; });
      v.status = v.offen.length ? "offen" : "erledigt";
      S[k] = v;
    });
    var aktuell = liste.filter(function (s) { return !ersatz[s.id]; }).map(function (s) {
      var b = {}; (s.braucht || []).forEach(function (x) { b[ersatz[x] || x] = true; });
      return Object.assign({}, s, { braucht: Object.keys(b) });
    });
    D.straenge.forEach(function (st) { if (vor["vor-" + st.id]) aktuell.unshift(vor["vor-" + st.id]); });
    return aktuell;
  }
  function vorText(v) {
    if (!v.offen.length) return "erledigt";
    return v.dran.length ? "jetzt dran: " + esc(v.dran.map(function (m) { return m.titel; }).join(", ")) : "wartet";
  }

  /* ---------- Kopf: Zielbild und Auswahl der Ergebnismeilensteine ---------- */
  var gewaehlt = (function () {
    var h = (location.hash || "").replace("#", "");
    return MS[h] ? h : D.meilensteine[0].id;
  })();
  var kopf = document.getElementById("zv-kopf");
  var buehne = document.getElementById("zv-buehne");

  function kopfZeichnen() {
    var m = MS[gewaehlt];
    var h = '<ol class="zv-stufen" role="tablist">';
    D.meilensteine.forEach(function (x) {
      h += '<li><button type="button" role="tab" aria-selected="' + (x.id === gewaehlt) + '" data-ms="' + x.id + '">' +
        '<span class="zv-stufe-nr">' + x.nr + '</span><span class="zv-stufe-text"><b>' + esc(msName(x)) + '</b><small>' + esc(x.termin) + '</small></span></button></li>';
    });
    h += '<li class="zv-stufe-ziel"><span class="zv-stufe-nr">&#9733;</span><span class="zv-stufe-text"><b>' + esc(D.zielbild.kurz || "Zielbild") + '</b><small>Ende des Projekts</small></span></li></ol>';
    h += '<div class="zv-zustand"><p class="zv-zustand-kicker">Wenn wir &bdquo;' + esc(msName(m)) + '&ldquo; erreicht haben</p><ul>' +
      (m.ergebnis || []).map(function (e) { return "<li>" + esc(e) + "</li>"; }).join("") + "</ul></div>";
    kopf.innerHTML = h;
    kopf.querySelectorAll("[data-ms]").forEach(function (b) {
      b.addEventListener("click", function () {
        gewaehlt = b.getAttribute("data-ms");
        history.replaceState(null, "", "#" + gewaehlt);
        kopfZeichnen(); buehneZeichnen();
      });
    });
  }

  /* ---------- Gemeinsame Bausteine ---------- */
  function ausFrueherem(s) { return MS[s.meilenstein] && MS[s.meilenstein].index < MS[gewaehlt].index; }
  function zustandText(z) { return { fertig: "erledigt", dran: "jetzt dran", wartet: "wartet" }[z]; }
  function nichtNoetig(liste) {
    var drin = {}; liste.forEach(function (s) { drin[s.id] = true; });
    var m = MS[gewaehlt];
    // Was zur selben Stufe gehört, aber nicht einfließt – das ist die wichtige Unterscheidung
    return D.schritte.filter(function (s) { return s.meilenstein === m.id && !drin[s.id]; });
  }
  function parallelHinweis(liste) {
    var n = nichtNoetig(liste);
    if (!n.length) return "";
    return '<div class="zv-parallel"><p><b>L&auml;uft parallel &ndash; nicht n&ouml;tig f&uuml;r &bdquo;' + esc(msName(MS[gewaehlt])) + '&ldquo;</b></p><ul>' +
      n.map(function (s) { return '<li><i style="background:' + STRANG[s.strang].farbe + '"></i>' + esc(s.titel) + " <small>" + esc(STRANG[s.strang].label) + "</small></li>"; }).join("") +
      "</ul></div>";
  }
  function legende() {
    return '<p class="zv-legende"><span class="zv-l zv-l--dran">jetzt dran</span><span class="zv-l zv-l--wartet">wartet auf Vorheriges</span>' +
      '<span class="zv-l zv-l--fertig">erledigt</span><span class="zv-l zv-l--frueher">Voraussetzung aus fr&uuml;herer Stufe</span></p>';
  }
  // Raster: Spalte = Tiefe, Zeile = Stoßrichtung (mit Unterzeilen für parallele Schritte)
  function raster(liste) {
    var t = tiefen(liste), spalten = 0, zeilen = [], pos = {};
    liste.forEach(function (s) { spalten = Math.max(spalten, t[s.id] + 1); });
    D.straenge.forEach(function (st) {
      var belegt = {}, unter = 0;
      liste.filter(function (s) { return s.strang === st.id; }).forEach(function (s) {
        var k = t[s.id], u = belegt[k] || 0;
        belegt[k] = u + 1; unter = Math.max(unter, u + 1);
        pos[s.id] = { sp: k, strang: st.id, unter: u };
      });
      if (unter) zeilen.push({ strang: st, unter: unter });
    });
    var y = 0;
    zeilen.forEach(function (z) { z.y = y; y += z.unter; });
    var zeileVon = {}; zeilen.forEach(function (z) { zeileVon[z.strang.id] = z; });
    Object.keys(pos).forEach(function (id) { pos[id].zeile = zeileVon[pos[id].strang].y + pos[id].unter; });
    return { pos: pos, spalten: spalten, zeilen: zeilen, hoehe: y };
  }

  /* ---------- A: Zuflussplan ---------- */
  // Kompakt: Name der Stoßrichtung steht über ihrer Bahn, damit alles bis zum Ergebnis in die Breite passt
  function zuflussplan(liste) {
    var r = raster(liste), B = 142, LUECKE = 30, H = 86, VL = 12, NAME = 30, ZIELB = 150;
    var lanePx = {}, yy = 0;
    r.zeilen.forEach(function (z) { lanePx[z.strang.id] = yy; z.px = yy; z.hpx = NAME + z.unter * (H + VL) + 8; yy += z.hpx + 10; });
    var hoehe = yy;
    var x = function (sp) { return sp * (B + LUECKE); };
    var yVon = function (id) { var p = r.pos[id], z = r.zeilen.filter(function (q) { return q.strang.id === p.strang; })[0]; return z.px + NAME + p.unter * (H + VL); };
    var zielX = x(r.spalten) + 10, breite = zielX + ZIELB;
    var zielY = hoehe / 2;
    var h = '<div class="zv-scroll"><div class="zv-flaeche" style="width:' + breite + 'px;height:' + hoehe + 'px">';
    var svg = '<svg class="zv-linien" width="' + breite + '" height="' + hoehe + '" style="position:absolute;left:0;top:0">';
    r.zeilen.forEach(function (z) {
      h += '<div class="zv-bahn" style="top:' + z.px + 'px;height:' + (z.hpx) + 'px;--f:' + z.strang.farbe + '">' +
        '<span class="zv-bahn-name"><b>' + esc(z.strang.label) + '</b> &middot; ' + esc(z.strang.verantwortung) + "</span></div>";
    });
    liste.forEach(function (s) {
      var p = r.pos[s.id], z = zustand(s.id), fr = !!s.pseudo;
      var px = x(p.sp), py = yVon(s.id);
      h += '<div class="zv-karte zv-karte--' + z + (fr ? " zv-karte--frueher" : "") + '" style="left:' + px + "px;top:" + py + "px;width:" + B + "px;height:" + H + 'px;--f:' + STRANG[s.strang].farbe + '">' +
        '<b>' + esc(s.titel) + "</b><small>" + (s.pseudo ? vorText(s) : zustandText(z)) + "</small></div>";
      var nachfolger = liste.filter(function (n) { return (n.braucht || []).indexOf(s.id) > -1; });
      var x1 = px + B, y1 = py + H / 2;
      if ((MS[gewaehlt].braucht || []).indexOf(s.id) > -1) svg += kurve(x1, y1, zielX, zielY, "#111", false);
      nachfolger.forEach(function (n) {
        var q = r.pos[n.id];
        svg += kurve(x1, y1, x(q.sp), yVon(n.id) + H / 2, n.strang === s.strang ? STRANG[s.strang].farbe : "#9a958d", n.strang !== s.strang);
      });
    });
    svg += "</svg>";
    h += svg;
    h += '<div class="zv-ziel" style="left:' + zielX + "px;top:" + (zielY - 60) + "px;width:" + ZIELB + 'px"><span>Ergebnis</span><b>' + esc(msName(MS[gewaehlt])) + "</b><small>" + esc(MS[gewaehlt].termin) + "</small></div>";
    h += "</div></div>";
    return legende() + h + parallelHinweis(liste);
  }
  function kurve(x1, y1, x2, y2, farbe, gestrichelt) {
    var dx = Math.max(30, (x2 - x1) / 2);
    return '<path d="M' + x1 + "," + y1 + " C" + (x1 + dx) + "," + y1 + " " + (x2 - dx) + "," + y2 + " " + x2 + "," + y2 + '" fill="none" stroke="' + farbe +
      '" stroke-width="' + (gestrichelt ? 1.6 : 2.4) + '"' + (gestrichelt ? ' stroke-dasharray="5 5"' : "") + ' marker-end="url(#zv-pfeil)"/>';
  }

  /* ---------- B: U-Bahn-Plan ---------- */
  // Hauptlinie je Stoßrichtung mit Beschriftung oberhalb, Nebenstrecken darunter (Beschriftung unten).
  // Strecken laufen rechtwinklig: nach unten zuerst senkrecht am Abzweig, nach oben zuerst waagerecht –
  // so kreuzt keine Strecke eine Beschriftung.
  function ubahn(liste) {
    var r = raster(liste), ABST = 140, ZH = 92, OBEN = 92, LINKS = 176, LB = 128;
    var lanePx = {}, yy = 0;
    r.zeilen.forEach(function (z) { z.px = yy + OBEN; yy += OBEN + (z.unter - 1) * ZH + (z.unter > 1 ? 62 : 22); });
    var hoehe = yy + 10;
    var x = function (sp) { return LINKS + sp * ABST; };
    var yVon = function (id) { var p = r.pos[id], z = r.zeilen.filter(function (q) { return q.strang.id === p.strang; })[0]; return z.px + p.unter * ZH; };
    var zielX = x(r.spalten) + 10, zielY = hoehe / 2 - 20, breite = zielX + 60;
    var svg = '<svg class="zv-ubahn" width="' + breite + '" height="' + (hoehe + 60) + '">';
    var labels = "";
    r.zeilen.forEach(function (z) {
      labels += '<div class="zv-linie-name" style="top:' + (z.px - 14) + 'px;--f:' + z.strang.farbe + '"><b>' + esc(z.strang.kurz) + "</b><span>" + esc(z.strang.label) + "</span></div>";
    });
    function weg(x1, y1, x2, y2) {
      if (y1 === y2) return "M" + x1 + "," + y1 + " L" + x2 + "," + y2;
      return y2 > y1 ? "M" + x1 + "," + y1 + " L" + x1 + "," + y2 + " L" + x2 + "," + y2
                     : "M" + x1 + "," + y1 + " L" + x2 + "," + y1 + " L" + x2 + "," + y2;
    }
    var strecken = "", umstiege = "";
    liste.forEach(function (s) {
      var x1 = x(r.pos[s.id].sp), y1 = yVon(s.id);
      liste.filter(function (n) { return (n.braucht || []).indexOf(s.id) > -1; }).forEach(function (n) {
        var d = weg(x1, y1, x(r.pos[n.id].sp), yVon(n.id));
        if (n.strang === s.strang) strecken += '<path d="' + d + '" stroke="' + STRANG[s.strang].farbe + '" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>';
        else {   // Umstieg: senkrecht in der Lücke vor dem Ziel-Halt, damit klar ist, wo er ankommt
          var x2 = x(r.pos[n.id].sp), y2 = yVon(n.id), xm = x2 - ABST / 2;
          umstiege += '<path d="M' + x1 + "," + y1 + " L" + xm + "," + y1 + " L" + xm + "," + y2 + " L" + x2 + "," + y2 + '" stroke="#9a958d" stroke-width="2.5" fill="none" stroke-dasharray="3 6" stroke-linecap="round" stroke-linejoin="round"/>';
        }
      });
      if ((MS[gewaehlt].braucht || []).indexOf(s.id) > -1)
        strecken += '<path d="' + weg(x1, y1, zielX, zielY) + '" stroke="' + STRANG[s.strang].farbe + '" stroke-width="8" fill="none" stroke-linecap="round" stroke-linejoin="round"/>';
    });
    svg += umstiege + strecken;
    liste.forEach(function (s) {
      var p = r.pos[s.id], z = zustand(s.id), fr = !!s.pseudo, umstieg = (s.braucht || []).some(function (b) { return S[b] && S[b].strang !== s.strang; });
      var cx = x(p.sp), cy = yVon(s.id), oben = p.unter === 0;
      svg += '<circle cx="' + cx + '" cy="' + cy + '" r="' + (umstieg ? 12 : 9) + '" fill="' + (z === "fertig" ? "#111" : z === "dran" ? "#ffed00" : "#fff") + '" stroke="#111" stroke-width="' + (umstieg ? 4 : 3) + '"' + (fr ? ' stroke-dasharray="3 3"' : "") + "/>";
      var zusatz = s.pseudo ? (s.dran.length ? "jetzt dran" : s.offen.length ? "" : "erledigt") : z === "dran" ? "jetzt dran" : umstieg ? "Umstieg" : "";
      labels += '<div class="zv-halt zv-halt--' + z + (oben ? " zv-halt--oben" : "") + '" style="left:' + (cx - LB / 2) + "px;top:" + (oben ? cy - 16 : cy + 16) + "px;width:" + LB + 'px"><b>' + esc(s.titel) + "</b>" +
        (zusatz ? "<small>" + zusatz + "</small>" : "") + "</div>";
    });
    svg += '<circle cx="' + zielX + '" cy="' + zielY + '" r="22" fill="#fff" stroke="#111" stroke-width="6"/><circle cx="' + zielX + '" cy="' + zielY + '" r="9" fill="#111"/></svg>';
    labels += '<div class="zv-endhalt" style="left:' + (zielX - 90) + "px;top:" + (zielY - 30) + 'px"><span>Endhaltestelle</span><b>' + esc(msName(MS[gewaehlt])) + "</b><small>" + esc(MS[gewaehlt].termin) + "</small></div>";
    return legende() + '<div class="zv-scroll"><div class="zv-flaeche" style="width:' + breite + "px;height:" + (hoehe + 70) + 'px">' + svg + labels + "</div></div>" + parallelHinweis(liste);
  }
  function pfeilDef() { return '<marker id="zv-pfeil" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#111"/></marker>'; }

  /* ---------- C: Startfreigabe ---------- */
  function startfreigabe(liste) {
    var dran = liste.filter(function (s) { return zustand(s.id) === "dran"; });
    var offen = liste.filter(function (s) { return zustand(s.id) !== "fertig"; });
    var h = '<div class="zv-go ' + (offen.length ? "zv-go--nein" : "zv-go--ja") + '"><span>' + (offen.length ? "Noch kein Go" : "Go") + "</span><b>" +
      (offen.length ? "F&uuml;r &bdquo;" + esc(msName(MS[gewaehlt])) + "&ldquo; fehlt noch, was unten offen ist." : "Alles erledigt &ndash; der Meilenstein kann kommen.") + "</b></div>";
    h += '<section class="zv-jetzt"><h3>Jetzt dran</h3><ul>' + dran.map(function (s) {
      return '<li style="--f:' + STRANG[s.strang].farbe + '"><b>' + esc(s.titel) + "</b><small>" + esc(STRANG[s.strang].label) + " &middot; " + esc(STRANG[s.strang].verantwortung) + "</small></li>";
    }).join("") + "</ul></section>";
    var t = tiefen(liste);
    h += '<div class="zv-spalten">';
    D.straenge.forEach(function (st) {
      var eig = liste.filter(function (s) { return s.strang === st.id; }).sort(function (a, b) { return t[a.id] - t[b.id]; });
      if (!eig.length) return;
      h += '<section class="zv-check" style="--f:' + st.farbe + '"><h3>' + esc(st.label) + "<small>" + esc(st.verantwortung) + "</small></h3><ol>" +
        eig.map(function (s) {
          var z = zustand(s.id), fr = ausFrueherem(s), w = z === "wartet" ? wartetAuf(s) : [];
          return '<li class="zv-check--' + z + '"><span class="zv-haken" aria-hidden="true"></span><span><b>' + esc(s.titel) + "</b><small>" + zustandText(z) +
            (fr ? " &middot; Voraussetzung aus " + esc(msName(MS[s.meilenstein])) : "") +
            (w.length ? " &middot; braucht: " + w.map(esc).join(", ") : "") + "</small></span></li>";
        }).join("") + "</ol></section>";
    });
    h += "</div>";
    return h + parallelHinweis(liste);
  }

  function buehneZeichnen() {
    var liste = zufluss(MS[gewaehlt]);
    var html = VARIANTE === "ubahn" ? ubahn(verdichten(liste)) : VARIANTE === "start" ? startfreigabe(liste) : zuflussplan(verdichten(liste));
    buehne.innerHTML = html;
    var s = buehne.querySelector("svg.zv-linien");
    if (s) s.insertAdjacentHTML("afterbegin", "<defs>" + pfeilDef() + "</defs>");
  }
  kopfZeichnen(); buehneZeichnen();
})();
