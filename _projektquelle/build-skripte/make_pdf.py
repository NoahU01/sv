# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import io, base64, json, os

WORKDIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(WORKDIR, "assets_b64.json")) as f:
    B64 = json.load(f)

ROT = HexColor("#EE0000")
DGRAU = HexColor("#444444")
GRAU = HexColor("#666666")
HELLGRAU = HexColor("#F0F0F0")

buf = io.BytesIO()
c = canvas.Canvas(buf, pagesize=A4)
W, H = A4

# Header bar
c.setFillColor(ROT)
c.rect(0, H-30*mm, W, 30*mm, fill=1, stroke=0)

logo_bytes = base64.b64decode(B64['logo_white'])
logo_img = ImageReader(io.BytesIO(logo_bytes))
iw, ih = logo_img.getSize()
disp_h = 12*mm
disp_w = disp_h * iw / ih
c.drawImage(logo_img, 20*mm, H-21*mm, width=disp_w, height=disp_h, mask='auto')

c.setFillColor(HexColor("#FFFFFF"))
c.setFont("Helvetica-Bold", 16)
c.drawRightString(W-20*mm, H-17*mm, "Quick-Check Bedarfsklärung")
c.setFont("Helvetica", 10)
c.drawRightString(W-20*mm, H-23*mm, "Vorbereitungs-Leitfaden")

y = H - 42*mm
c.setFillColor(DGRAU)
c.setFont("Helvetica-Bold", 13)
c.drawString(20*mm, y, "So bereiten Sie sich in 5 Minuten vor")
y -= 9*mm
c.setFont("Helvetica", 10)
c.setFillColor(GRAU)
intro = ("Der Quick-Check hilft uns, Ihren Entwicklungsbedarf schnell und passgenau einzuordnen. "
         "Damit unser gemeinsames Gespräch möglichst wirksam wird, laden wir Sie ein, sich vorab kurz "
         "mit den folgenden Leitfragen auseinanderzusetzen.")
from reportlab.lib.utils import simpleSplit
lines = simpleSplit(intro, "Helvetica", 10, W-40*mm)
for ln in lines:
    c.drawString(20*mm, y, ln); y -= 5*mm

y -= 6*mm

sections = [
    ("1. Ausgangslage", [
        "Welche fachlichen oder persönlichen Anforderungen beschäftigen Sie aktuell am meisten?",
        "Wo merken Sie im Alltag, dass Wissen oder Routine an ihre Grenzen stoßen?",
    ]),
    ("2. Zielbild", [
        "Wie sieht für Sie eine gelungene Entwicklung in den nächsten 6-12 Monaten aus?",
        "Was soll sich für Sie, Ihr Team oder Ihre Vertriebseinheit spürbar verändern?",
    ]),
    ("3. Rahmenbedingungen", [
        "Wie viel Zeit können Sie realistisch pro Monat für Ihre Entwicklung einplanen?",
        "Bevorzugen Sie digitale Formate, Präsenztermine oder eine Mischung aus beidem?",
    ]),
]

for title, qs in sections:
    c.setFillColor(ROT)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(20*mm, y, title)
    y -= 6.5*mm
    c.setFont("Helvetica", 10)
    c.setFillColor(DGRAU)
    for q in qs:
        c.drawString(24*mm, y, u"• " + q)
        y -= 5.5*mm
    y -= 3*mm

y -= 4*mm
c.setFillColor(HELLGRAU)
c.roundRect(20*mm, y-24*mm, W-40*mm, 22*mm, 3*mm, fill=1, stroke=0)
c.setFillColor(DGRAU)
c.setFont("Helvetica-Bold", 10)
c.drawString(25*mm, y-9*mm, "Gut zu wissen:")
c.setFont("Helvetica", 9.5)
c.drawString(25*mm, y-15*mm, "Der Quick-Check dauert rund 20 Minuten und ist für Mitarbeitende und")
c.drawString(25*mm, y-20*mm, "Vertriebspartner der SV im Rahmen ihrer Tätigkeit kostenfrei.")

# Footer
c.setFillColor(GRAU)
c.setFont("Helvetica", 8)
c.drawString(20*mm, 15*mm, "SV Akademie — Bilden. Entwickeln. Begeistern.")
c.drawRightString(W-20*mm, 15*mm, "Strategie-Mock-up · nicht produktiv im Einsatz")

c.showPage()
c.save()
pdf_bytes = buf.getvalue()

out_path = os.path.join(WORKDIR, "quickcheck_leitfaden.pdf")
with open(out_path, "wb") as f:
    f.write(pdf_bytes)

B64['leitfaden_pdf'] = base64.b64encode(pdf_bytes).decode('ascii')
with open(os.path.join(WORKDIR, "assets_b64.json"), "w") as f:
    json.dump(B64, f)

print("PDF written:", out_path, len(pdf_bytes), "bytes")
