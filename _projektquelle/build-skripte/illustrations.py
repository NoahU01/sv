# -*- coding: utf-8 -*-
import math

# ---------- Isometric projection helpers ----------
RIGHT = (0.866, 0.5)
LEFT = (-0.866, 0.5)
UP = (0.0, -1.0)

def iso(x, y, z, k=1.0, ox=0.0, oy=0.0):
    px = x*RIGHT[0]*k + y*LEFT[0]*k + z*UP[0]*k + ox
    py = x*RIGHT[1]*k + y*LEFT[1]*k + z*UP[1]*k + oy
    return (round(px,2), round(py,2))

def poly(points, fill, opacity=1.0, stroke="none", stroke_width=0):
    pts = " ".join(f"{p[0]},{p[1]}" for p in points)
    extra = f' stroke="{stroke}" stroke-width="{stroke_width}" stroke-linejoin="round"' if stroke != "none" else ""
    return f'<polygon points="{pts}" fill="{fill}" fill-opacity="{opacity}"{extra}/>'

def box(x0, y0, z0, w, d, h, k, ox, oy, top_c, right_c, left_c, stroke="#00000022"):
    """Iso box: top face (diamond), right face, left face."""
    A  = iso(x0,   y0,   z0+h, k, ox, oy)
    B  = iso(x0+w, y0,   z0+h, k, ox, oy)
    C  = iso(x0+w, y0+d, z0+h, k, ox, oy)
    D  = iso(x0,   y0+d, z0+h, k, ox, oy)
    Bb = iso(x0+w, y0,   z0,   k, ox, oy)
    Cb = iso(x0+w, y0+d, z0,   k, ox, oy)
    Db = iso(x0,   y0+d, z0,   k, ox, oy)
    top = poly([A,B,C,D], top_c, stroke=stroke, stroke_width=1.5)
    right = poly([B,Bb,Cb,C], right_c, stroke=stroke, stroke_width=1.5)
    left = poly([D,C,Cb,Db], left_c, stroke=stroke, stroke_width=1.5)
    return top + right + left

def line3(x0,y0,z0,x1,y1,z1,k,ox,oy,color,width=3,cap="round"):
    p0 = iso(x0,y0,z0,k,ox,oy); p1 = iso(x1,y1,z1,k,ox,oy)
    return f'<line x1="{p0[0]}" y1="{p0[1]}" x2="{p1[0]}" y2="{p1[1]}" stroke="{color}" stroke-width="{width}" stroke-linecap="{cap}"/>'

def rect_on_top(x0,y0,z,w,d,k,ox,oy,color,opacity=1,inset=0.0):
    """Small colored rectangle resting flush on a top face at height z."""
    x0i, y0i = x0+inset, y0+inset
    wi, di = w-2*inset, d-2*inset
    A = iso(x0i, y0i, z, k, ox, oy)
    B = iso(x0i+wi, y0i, z, k, ox, oy)
    C = iso(x0i+wi, y0i+di, z, k, ox, oy)
    D = iso(x0i, y0i+di, z, k, ox, oy)
    return poly([A,B,C,D], color, opacity=opacity)

def ellipse_shadow(cx, cy, rx, ry, opacity=0.12):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#000000" fill-opacity="{opacity}"/>'

# Brand palette for illustrations
ROT = "#EE0000"
ROT_D = "#B30000"
VIOLET = "#9B348E"
GRAU_HELL = "#F0F0F0"
GRAU = "#D9D9D9"
GRAU_D = "#BBBBBB"
DGRAU = "#666666"
WEISS = "#FFFFFF"

K = 1.55  # global scale

def illustration_onepager():
    ox, oy = 118, 195
    out = '<svg viewBox="0 0 320 250" xmlns="http://www.w3.org/2000/svg">'
    out += ellipse_shadow(ox+10, oy+38, 92, 13)
    # thin document slab
    out += box(-45, -35, 0, 90, 70, 6, K, ox, oy, WEISS, GRAU, "#EDEDED")
    # text lines on top face of the document
    for i, yy in enumerate([-20, -8, 4, 16]):
        w = 60 if i < 3 else 38
        out += rect_on_top(-38, yy, 6, w, 4, K, ox, oy, GRAU_D if i%2==0 else GRAU, 0.9)
    # small red accent block (headline bar) top-left of document
    out += rect_on_top(-38, -34, 6, 26, 6, K, ox, oy, ROT, 1)
    # speech circles (people talking) - simple flat 2D accent, offset to the right of the iso slab
    heads_cx = ox + 118
    out += f'''
      <g>
        <circle cx="{heads_cx}" cy="{oy-58}" r="17" fill="{VIOLET}" fill-opacity="0.16"/>
        <circle cx="{heads_cx}" cy="{oy-58}" r="17" fill="none" stroke="{VIOLET}" stroke-width="4"/>
        <circle cx="{heads_cx+32}" cy="{oy-32}" r="13" fill="{ROT}" fill-opacity="0.14"/>
        <circle cx="{heads_cx+32}" cy="{oy-32}" r="13" fill="none" stroke="{ROT}" stroke-width="4"/>
        <path d="M{heads_cx+8},{oy-50} q13,9 16,14" fill="none" stroke="{DGRAU}" stroke-width="3" stroke-linecap="round" stroke-dasharray="1 7"/>
      </g>
    '''
    out += '</svg>'
    return out

def illustration_macbook():
    ox, oy = 158, 205
    out = '<svg viewBox="0 0 320 250" xmlns="http://www.w3.org/2000/svg">'
    out += ellipse_shadow(150, 228, 100, 14)
    # base / keyboard slab
    out += box(-55, -30, 0, 110, 55, 5, K, ox, oy, "#E4E4E4", GRAU_D, "#CFCFCF")
    # screen as thin upright box at the back edge
    out += box(-50, -30, 5, 100, 4, 62, K, ox, oy, "#2b2b2b", "#1c1c1c", "#141414")
    # screen inner "portal" surface (front-left face, lightly inset) -- approximate with a rect_on_top-like panel using the left face plane
    # draw portal UI as small colored bars projected onto the screen front face
    sx0, sy0, sz0 = -50, -30, 5
    sw, sh = 100, 62
    # corners of screen front-left face (x0,y0+d ... ) reuse left face plane (x const spans, y0+d fixed)
    def screen_pt(u, v):
        # u in [0,1] across width (x-axis), v in [0,1] up the height (z-axis)
        x = sx0 + sw*u
        y = sy0 + 4
        z = sz0 + 4 + (sh-8)*v
        return iso(x, y, z, K, ox, oy)
    p_tl = screen_pt(0.08, 0.85); p_tr = screen_pt(0.92, 0.85)
    p_bl = screen_pt(0.08, 0.08); p_br = screen_pt(0.92, 0.08)
    out += poly([p_tl,p_tr,p_br,p_bl], WEISS, opacity=0.96)
    # dashboard bars inside screen
    def bar(u0,u1,v0,v1,color):
        a=screen_pt(u0,v1); b=screen_pt(u1,v1); c=screen_pt(u1,v0); d=screen_pt(u0,v0)
        return poly([a,b,c,d], color)
    out += bar(0.14,0.42,0.62,0.75, ROT)
    out += bar(0.14,0.62,0.44,0.56, GRAU_D)
    out += bar(0.14,0.50,0.28,0.40, GRAU)
    out += bar(0.66,0.86,0.30,0.75, VIOLET)
    out += '</svg>'
    return out

def illustration_videocall():
    ox, oy = 158, 200
    out = '<svg viewBox="0 0 320 250" xmlns="http://www.w3.org/2000/svg">'
    out += ellipse_shadow(ox, oy+42, 88, 12)
    # monitor stand (centered at x=0,y=0)
    out += box(-16, -4, 0, 32, 8, 6, K, ox, oy, GRAU_D, GRAU, "#CFCFCF")
    out += box(-6, -6, 6, 12, 12, 10, K, ox, oy, GRAU_D, GRAU, "#CFCFCF")
    # monitor screen (upright box), centered at x=0, thin depth around y=0
    out += box(-46, -2, 16, 92, 4, 56, K, ox, oy, "#2b2b2b", "#1c1c1c", "#141414")
    sx0, sy0, sz0 = -46, -2, 16
    sw, sh = 92, 56
    def screen_pt(u, v):
        x = sx0 + sw*u
        y = sy0 + 4
        z = sz0 + 4 + (sh-8)*v
        return iso(x, y, z, K, ox, oy)
    p_tl = screen_pt(0.06, 0.88); p_tr = screen_pt(0.94, 0.88)
    p_bl = screen_pt(0.06, 0.10); p_br = screen_pt(0.94, 0.10)
    out += poly([p_tl,p_tr,p_br,p_bl], "#1a1a1a", opacity=1)
    # 2x2 video tiles
    tiles = [(0.10,0.52,0.50,0.86, ROT),(0.54,0.94,0.50,0.86, VIOLET),
             (0.10,0.52,0.12,0.46, "#8a8a8a"),(0.54,0.94,0.12,0.46, "#5f5f5f")]
    for u0,u1,v0,v1,color in tiles:
        a=screen_pt(u0,v1); b=screen_pt(u1,v1); c=screen_pt(u1,v0); d=screen_pt(u0,v0)
        out += poly([a,b,c,d], color)
        # tiny head dot in each tile
        cx = (a[0]+c[0])/2; cy = (a[1]+c[1])/2
        out += f'<circle cx="{cx}" cy="{cy-3}" r="5" fill="#ffffff" fill-opacity="0.85"/>'
    out += '</svg>'
    return out

def cycle_ring():
    """A true circle (dashed, brand red) with 3 small arrowheads suggesting clockwise rotation.
    Uses a square viewBox with default preserveAspectRatio so it always renders as a real circle,
    centered within its container regardless of the container's actual (dynamic) width/height."""
    cx, cy, r = 250, 250, 210
    def point_on_circle(deg):
        rad = math.radians(deg)
        return (cx + r*math.cos(rad), cy + r*math.sin(rad))
    # arrowheads at roughly 340deg (top, between A and B), 80deg (right-bottom, between B and C),
    # 200deg (left-bottom, between C and A) -- angle 0 = right, going clockwise (screen y grows downward)
    heads = []
    for deg in (340, 80, 200):
        px, py = point_on_circle(deg)
        # tangent direction for clockwise motion at this point
        trad = math.radians(deg + 90)
        tx, ty = math.cos(trad), math.sin(trad)
        p1 = (px - tx*14 - (-ty)*8, py - ty*14 - (tx)*8)
        p2 = (px + tx*2, py + ty*2)
        p3 = (px - tx*14 + (-ty)*8, py - ty*14 + (ty)*8)
        heads.append(f'<path d="M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} L{p3[0]:.1f},{p3[1]:.1f} Z" fill="#EE0000"/>')
    return (f'<svg viewBox="0 0 500 500" xmlns="http://www.w3.org/2000/svg">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#EE0000" stroke-opacity="0.35" '
            f'stroke-width="3" stroke-dasharray="3 13" stroke-linecap="round"/>'
            + "".join(heads) +
            '</svg>')

ICON_LUPE = '''<svg viewBox="0 0 250 250" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="14"><circle cx="105" cy="105" r="70"/><path d="M156 156l70 70"/></g></svg>'''

ICON_CHECKLIST = '''<svg viewBox="0 0 250 250" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="12"><rect x="45" y="30" width="160" height="190" rx="14"/><path d="M75 95l20 20 45-50"/><path d="M75 155h90"/><path d="M75 180h60"/></g></svg>'''

ICON_SYNC = '''<svg viewBox="0 0 250 250" xmlns="http://www.w3.org/2000/svg"><g fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="14"><path d="M55 125a70 70 0 0 1 115-53"/><path d="M195 125a70 70 0 0 1 -115 53"/><path d="M158 55l12 17-19 8"/><path d="M92 195l-12-17 19-8"/></g></svg>'''

if __name__ == "__main__":
    print(len(illustration_onepager()), len(illustration_macbook()), len(illustration_videocall()))

# =====================================================================
# Flat-character illustrations (Stil: sparkassenversicherung.de "Unsere
# Vorteile" -- flache Personen-Illustrationen, rote Möbel/Akzente,
# weicher grauer Wolken-Hintergrund). Ersetzt den isometrischen Stil.
# =====================================================================

SKIN = "#D9A679"
SKIN2 = "#C68F63"
HAAR_DUNKEL = "#33302E"
HAAR_ROT = "#7A2E1E"
ANZUG = "#2E2E38"
BLUSE = "#F4F1EC"
GRAU_BLOB = "#E7E7E7"
GRAU_BLOB2 = "#EFEFEF"

def blob(cx, cy, s=1.0, color=GRAU_BLOB, rot=0):
    d = ("M -95,10 C -110,-55 -55,-95 5,-92 C 70,-90 100,-55 95,0 "
         "C 90,55 55,95 -5,92 C -65,90 -80,60 -95,10 Z")
    return f'<g transform="translate({cx},{cy}) rotate({rot}) scale({s})"><path d="{d}" fill="{color}"/></g>'

def chair(cx, cy, s=1.0, color=ROT):
    """Simple flat lounge chair, seat facing right, legs at bottom."""
    return f'''<g transform="translate({cx},{cy}) scale({s})">
      <path d="M -30,-55 C -46,-55 -46,-15 -34,0 L 34,0 C 44,-15 40,-55 20,-58 C 5,-60 -15,-60 -30,-55 Z" fill="{color}"/>
      <rect x="-34" y="-2" width="70" height="14" rx="7" fill="{color}"/>
      <line x1="-26" y1="12" x2="-30" y2="30" stroke="{DGRAU}" stroke-width="4" stroke-linecap="round"/>
      <line x1="28" y1="12" x2="32" y2="30" stroke="{DGRAU}" stroke-width="4" stroke-linecap="round"/>
    </g>'''

def person_sit(cx, cy, s=1.0, shirt=ANZUG, hair=HAAR_DUNKEL, flip=False):
    fx = -1 if flip else 1
    return f'''<g transform="translate({cx},{cy}) scale({s*fx},{s})">
      <path d="M -20,10 C -22,45 -18,70 -14,72 L 14,72 C 18,70 22,45 20,10 C 20,-6 -20,-6 -20,10 Z" fill="{shirt}"/>
      <path d="M -14,68 C -16,80 -14,88 -8,88 L 2,88 C 4,84 2,70 -2,66 Z" fill="{shirt}" opacity="0.9"/>
      <path d="M 4,66 C 10,72 22,78 30,78 C 32,74 30,70 26,68 C 18,64 10,60 6,58 Z" fill="{SKIN}"/>
      <circle cx="0" cy="-18" r="17" fill="{SKIN}"/>
      <path d="M -17,-22 C -19,-34 -8,-40 2,-39 C 13,-38 18,-30 16,-20 C 10,-26 -6,-30 -17,-22 Z" fill="{hair}"/>
      <path d="M -16,4 C -22,10 -24,20 -22,26 C -18,24 -14,16 -12,6 Z" fill="{shirt}"/>
    </g>'''

def laptop(cx, cy, s=1.0, screen_content=""):
    return f'''<g transform="translate({cx},{cy}) scale({s})">
      <path d="M -38,10 L 38,10 L 44,22 L -44,22 Z" fill="{GRAU_D}"/>
      <rect x="-34" y="-32" width="68" height="42" rx="3" fill="#2b2b2b"/>
      <rect x="-30" y="-28" width="60" height="34" rx="1" fill="#ffffff"/>
      {screen_content}
    </g>'''

def speech_dots(cx, cy, s=1.0):
    return f'''<g transform="translate({cx},{cy}) scale({s})">
      <path d="M -40,-30 C -40,-46 -26,-58 -8,-58 C 10,-58 24,-46 24,-30 C 24,-14 10,-2 -8,-2 C -14,-2 -19,-3 -24,-6 L -40,4 L -35,-10 C -38,-15 -40,-22 -40,-30 Z" fill="#ffffff" stroke="{GRAU3}" stroke-width="2"/>
      <circle cx="-22" cy="-30" r="3.5" fill="{ROT}"/>
      <circle cx="-8" cy="-30" r="3.5" fill="{GRAU_D}"/>
      <circle cx="6" cy="-30" r="3.5" fill="{GRAU_D}"/>
    </g>'''

GRAU3 = "#D9D9D9"

def illustration_quickcheck_flat():
    out = '<svg viewBox="0 0 320 250" xmlns="http://www.w3.org/2000/svg">'
    out += blob(160, 130, 1.35)
    out += ellipse_shadow(160, 228, 92, 11)
    out += chair(108, 205, 0.95, ROT)
    out += chair(212, 205, 0.95, ROT_D)
    out += person_sit(108, 155, 0.85, shirt=ANZUG, hair=HAAR_DUNKEL, flip=False)
    out += person_sit(212, 155, 0.85, shirt=BLUSE, hair=HAAR_ROT, flip=True)
    out += speech_dots(160, 95, 0.8)
    out += '</svg>'
    return out

def illustration_portal_flat():
    out = '<svg viewBox="0 0 320 250" xmlns="http://www.w3.org/2000/svg">'
    out += blob(160, 130, 1.35)
    out += ellipse_shadow(160, 228, 92, 11)
    screen = (f'<rect x="-26" y="-24" width="24" height="8" fill="{ROT}"/>'
              f'<rect x="-26" y="-13" width="40" height="6" fill="{GRAU_D}"/>'
              f'<rect x="-26" y="-4" width="30" height="6" fill="{GRAU3}"/>'
              f'<circle cx="20" cy="-15" r="9" fill="{VIOLET}" fill-opacity="0.85"/>')
    out += person_sit(160, 128, 0.85, shirt=ANZUG, hair=HAAR_DUNKEL)
    out += laptop(160, 205, 1.15, screen)
    out += '</svg>'
    return out

def illustration_community_flat():
    out = '<svg viewBox="0 0 320 250" xmlns="http://www.w3.org/2000/svg">'
    out += blob(160, 130, 1.35)
    out += ellipse_shadow(160, 228, 92, 11)
    tiles = (f'<rect x="-29" y="-27" width="27" height="17" fill="{ROT}"/>'
             f'<circle cx="-15.5" cy="-20" r="4" fill="#fff" fill-opacity="0.9"/>'
             f'<rect x="1" y="-27" width="27" height="17" fill="{VIOLET}"/>'
             f'<circle cx="14.5" cy="-20" r="4" fill="#fff" fill-opacity="0.9"/>'
             f'<rect x="-29" y="-9" width="27" height="17" fill="#8a8a8a"/>'
             f'<circle cx="-15.5" cy="-2" r="4" fill="#fff" fill-opacity="0.9"/>'
             f'<rect x="1" y="-9" width="27" height="17" fill="#5f5f5f"/>'
             f'<circle cx="14.5" cy="-2" r="4" fill="#fff" fill-opacity="0.9"/>')
    out += person_sit(160, 128, 0.85, shirt=BLUSE, hair=HAAR_DUNKEL)
    out += laptop(160, 205, 1.15, tiles)
    out += '</svg>'
    return out

def _wrap_text_center(lines, cx, y_start, line_height, font_size=14.5, color="#666666", weight="400", family="'Sparkasse Lt', Arial, sans-serif"):
    out = f'<text x="{cx}" y="{y_start}" text-anchor="middle" font-family="{family}" font-size="{font_size}" font-weight="{weight}" fill="{color}">'
    for i, ln in enumerate(lines):
        dy = 0 if i == 0 else line_height
        out += f'<tspan x="{cx}" dy="{dy}">{ln}</tspan>'
    out += '</text>'
    return out

def _icon_glyph(kind, cx, cy, s=1.0, color="#EE0000"):
    """Small standalone icon (lupe / checklist / sync) drawn with plain path/shape primitives, centered at cx,cy."""
    if kind == "lupe":
        return f'''<g transform="translate({cx},{cy}) scale({s})" fill="none" stroke="{color}" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="-4" cy="-4" r="13"/><line x1="6" y1="6" x2="16" y2="16"/></g>'''
    if kind == "checklist":
        return f'''<g transform="translate({cx},{cy}) scale({s})" fill="none" stroke="{color}" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round">
          <rect x="-13" y="-16" width="26" height="32" rx="4"/>
          <path d="M-7,-6 l4,4 l9,-10"/><line x1="-7" y1="6" x2="7" y2="6"/><line x1="-7" y1="12" x2="3" y2="12"/></g>'''
    if kind == "sync":
        return f'''<g transform="translate({cx},{cy}) scale({s})" fill="none" stroke="{color}" stroke-width="4.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M-13,-2a13,13 0 0 1 22,-9.5"/><path d="M13,2a13,13 0 0 1 -22,9.5"/>
          <path d="M6,-16l3,4.5l-5,2"/><path d="M-6,16l-3,-4.5l5,-2"/></g>'''
    return ""

def cycle_static():
    """Complete cycle diagram (ring + 3 icon nodes + all text) baked into ONE static SVG.
    Used as a plain <img> so it can never be affected by page CSS/overlap issues."""
    cx0, cy0, r = 300, 250, 175
    def pt(deg):
        rad = math.radians(deg)
        return (cx0 + r*math.cos(rad), cy0 + r*math.sin(rad))
    heads = []
    for deg in (340, 80, 200):
        px, py = pt(deg)
        trad = math.radians(deg + 90)
        tx, ty = math.cos(trad), math.sin(trad)
        p1 = (px - tx*13 - (-ty)*7, py - ty*13 - (tx)*7)
        p2 = (px + tx*2, py + ty*2)
        p3 = (px - tx*13 + (-ty)*7, py - ty*13 + (ty)*7)
        heads.append(f'<path d="M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} L{p3[0]:.1f},{p3[1]:.1f} Z" fill="#EE0000" fill-opacity="0.55"/>')
    ring = (f'<circle cx="{cx0}" cy="{cy0}" r="{r}" fill="none" stroke="#EE0000" stroke-opacity="0.32" '
            f'stroke-width="2.5" stroke-dasharray="3 12" stroke-linecap="round"/>' + "".join(heads))

    out = '<svg viewBox="0 0 600 460" xmlns="http://www.w3.org/2000/svg">'
    out += ring
    # Node A - top-left
    out += _icon_glyph("lupe", 118, 95, 1.35)
    out += _wrap_text_center(["Regelmäßige Analyse der", "zukünftigen Anforderungen an", "Mitarbeitende der SV."], 118, 138, 19)
    # Node B - top-right
    out += _icon_glyph("checklist", 482, 95, 1.35)
    out += _wrap_text_center(["Ableitung notwendiger Skills", "&amp; zugehöriger", "Weiterbildungsbedarf."], 482, 138, 19)
    # Node C - bottom-center
    out += _icon_glyph("sync", 300, 350, 1.35)
    out += _wrap_text_center(["Abgleich mit Weiterbildungsangebot", "&amp; Vorschlag zur Anpassung."], 300, 393, 19)
    out += '</svg>'
    return out
