#!/usr/bin/env python3
"""Misst je Seite, wie viel Platz unter dem letzten Element frei bleibt.

Negativ heisst: Der Inhalt laeuft unten aus der Seite und wird im Druck
abgeschnitten. Unter etwa 8 mm wird es eng - dann sitzt der Text auf der
Fusszeile.
"""
import json, pathlib, subprocess, sys, tempfile

HERE = pathlib.Path(__file__).resolve().parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

JS = """
<script>Promise.all([document.fonts.ready,new Promise(function(r){window.addEventListener('load',r)})]).then(function(){
var mm=96/25.4,out=[];
document.querySelectorAll('.page').forEach(function(pg,i){
  var r=pg.getBoundingClientRect(),unten=0,ueber=[];
  pg.querySelectorAll('*').forEach(function(e){
    if(e.classList.contains('fuss')||e.closest('.fuss'))return;
    var b=e.getBoundingClientRect();
    if(b.height>0)unten=Math.max(unten,b.bottom-r.top);
    if(b.right-r.left>r.width+1)ueber.push(e.className||e.tagName);
  });
  var f=pg.querySelector('.fuss').getBoundingClientRect();
  out.push({seite:i+1,frei:+(((f.top-r.top)-unten)/mm).toFixed(1),
            ueber:ueber.slice(0,3)});
});
document.title='MESS'+JSON.stringify(out);});</script>
"""

for fassung in ("moderation", "kompakt"):
    src = HERE / "_build" / f"_src_{fassung}.html"
    t = src.read_text(encoding="utf-8").replace("</body>", JS + "</body>")
    tmp = src.with_name(f"_mess_{fassung}.html")
    tmp.write_text(t, encoding="utf-8")
    r = subprocess.run([CHROME, "--headless=new", "--disable-gpu",
                        "--window-size=900,1200", "--virtual-time-budget=5000",
                        "--dump-dom", "file://" + str(tmp)],
                       capture_output=True, text=True, timeout=120).stdout
    i = r.index("<title>MESS") + 11
    daten = json.loads(r[i:r.index("</title>", i)].replace("&quot;", '"'))
    print(f"\n{fassung}:")
    for d in daten:
        warn = "  << LAEUFT UEBER" if d["frei"] < 0 else ("  < eng" if d["frei"] < 8 else "")
        ue = f"  Breite-Ueberlauf: {d['ueber']}" if d["ueber"] else ""
        print(f"  Seite {d['seite']}: {d['frei']:>7.1f} mm frei{warn}{ue}")
    tmp.unlink()
