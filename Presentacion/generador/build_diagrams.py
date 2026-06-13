# -*- coding: utf-8 -*-
"""
Diagramas de arquitectura (Fases 1 y 2) en estilo draw.io / formal:
paleta oficial de draw.io, íconos de servicios, conectores ORTOGONALES y clusters.
Salida: Presentacion/diagramas/*.png  (16:9, 3200x1800). Sin navegador ni Office.
"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = r"C:\Users\Conrado\Desktop\Programacion\UNSTA\app-development\Final\Presentacion\diagramas"
os.makedirs(OUT, exist_ok=True)

S = 2.0
W, H = int(1600 * S), int(900 * S)
FD = r"C:\Windows\Fonts"

# ---- Paleta oficial draw.io (fill / stroke) ----
DRAW = {
    "blue":   ("#DAE8FC", "#6C8EBF"),
    "green":  ("#D5E8D4", "#82B366"),
    "orange": ("#FFE6CC", "#D79B00"),
    "yellow": ("#FFF2CC", "#D6B656"),
    "purple": ("#E1D5E7", "#9673A6"),
    "red":    ("#F8CECC", "#B85450"),
    "gray":   ("#F5F5F5", "#666666"),
    "teal":   ("#B0E3E6", "#0E8088"),
}
INK   = "#23272E"
MUTE  = "#6B7280"
LINE  = "#4D4D4D"
CANVAS = "#FFFFFF"

_fc = {}
def F(kind, size):
    files = {"r": "segoeui.ttf", "b": "segoeuib.ttf", "sb": "seguisb.ttf", "l": "segoeuil.ttf"}
    k = (kind, size)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(os.path.join(FD, files[kind]), int(size * S))
    return _fc[k]

def px(v): return int(round(v * S))
def canvas(bg=CANVAS): img = Image.new("RGB", (W, H), bg); return img, ImageDraw.Draw(img)

def rrect(d, x, y, w, h, r=10, fill=None, outline=None, width=1.6):
    d.rounded_rectangle([px(x), px(y), px(x + w), px(y + h)], radius=px(r),
                        fill=fill, outline=outline, width=max(1, px(width)))
def rect(d, x, y, w, h, fill=None, outline=None, width=1.6):
    d.rectangle([px(x), px(y), px(x + w), px(y + h)], fill=fill, outline=outline, width=max(1, px(width)))

def dashed_rrect(d, x, y, w, h, r=14, outline="#9AA3AF", width=1.6, dash=14, gap=9):
    # contorno discontinuo (cluster)
    pts = []
    # top & bottom
    xx = x + r
    while xx < x + w - r:
        d.line([px(xx), px(y), px(min(xx + dash, x + w - r)), px(y)], fill=outline, width=max(1, px(width)))
        d.line([px(xx), px(y + h), px(min(xx + dash, x + w - r)), px(y + h)], fill=outline, width=max(1, px(width)))
        xx += dash + gap
    yy = y + r
    while yy < y + h - r:
        d.line([px(x), px(yy), px(x), px(min(yy + dash, y + h - r))], fill=outline, width=max(1, px(width)))
        d.line([px(x + w), px(yy), px(x + w), px(min(yy + dash, y + h - r))], fill=outline, width=max(1, px(width)))
        yy += dash + gap
    # esquinas (arcos)
    for (cx, cy, a0, a1) in [(x + r, y + r, 180, 270), (x + w - r, y + r, 270, 360),
                             (x + w - r, y + h - r, 0, 90), (x + r, y + h - r, 90, 180)]:
        d.arc([px(cx - r), px(cy - r), px(cx + r), px(cy + r)], a0, a1, fill=outline, width=max(1, px(width)))

def text(d, x, y, s, font, fill, anchor="la"):
    d.text((px(x), px(y)), s, font=font, fill=fill, anchor=anchor)
def textc(d, cx, cy, s, font, fill):
    d.text((px(cx), px(cy)), s, font=font, fill=fill, anchor="mm")
def measure(d, s, font):
    b = d.textbbox((0, 0), s, font=font); return (b[2] - b[0]) / S, (b[3] - b[1]) / S
def wrap(d, s, font, maxw):
    out, cur = [], ""
    for w_ in s.split():
        t = (cur + " " + w_).strip()
        if measure(d, t, font)[0] <= maxw: cur = t
        else:
            if cur: out.append(cur)
            cur = w_
    if cur: out.append(cur)
    return out
def paragraph(d, x, y, s, font, fill, maxw, lh=1.3):
    asc = font.size / S
    for i, ln in enumerate(wrap(d, s, font, maxw)):
        text(d, x, y + i * asc * lh, ln, font, fill)

# ---------- conectores ortogonales (estilo draw.io) ----------
def _arrowhead(d, x, y, ang, color, size=11):
    p = [(x, y),
         (x - size * math.cos(ang - 0.4), y - size * math.sin(ang - 0.4)),
         (x - size * math.cos(ang + 0.4), y - size * math.sin(ang + 0.4))]
    d.polygon([(px(a), px(b)) for a, b in p], fill=color)

def _poly(d, pts, color, w):
    for i in range(len(pts) - 1):
        d.line([px(pts[i][0]), px(pts[i][1]), px(pts[i + 1][0]), px(pts[i + 1][1])],
               fill=color, width=max(1, px(w)))

def conn_vh(d, x1, y1, x2, y2, color=LINE, w=2.0, busY=None, label=None, lfont=None, dash=False):
    """Sale hacia abajo, viaja por un 'bus' horizontal, baja al destino (arriba->abajo)."""
    if busY is None: busY = (y1 + y2) / 2
    pts = [(x1, y1), (x1, busY), (x2, busY), (x2, y2)]
    if dash:
        _poly_dashed(d, pts, color, w)
    else:
        _poly(d, pts, color, w)
    _arrowhead(d, x2, y2, math.pi / 2, color)
    if label:
        textc(d, (x1 + x2) / 2, busY - 9, label, lfont or F("sb", 10), MUTE)

def conn_hv(d, x1, y1, x2, y2, color=LINE, w=2.0, busX=None, label=None, lfont=None, end_dir="right"):
    """Sale horizontal, baja/sube, llega horizontal (izq->der)."""
    if busX is None: busX = (x1 + x2) / 2
    pts = [(x1, y1), (busX, y1), (busX, y2), (x2, y2)]
    _poly(d, pts, color, w)
    _arrowhead(d, x2, y2, 0 if end_dir == "right" else math.pi, color)
    if label:
        textc(d, busX, (y1 + y2) / 2 - 9, label, lfont or F("sb", 10), MUTE)

def conn_straight(d, x1, y1, x2, y2, color=LINE, w=2.0, arrow=True, dash=False, ang=None):
    if dash: _poly_dashed(d, [(x1, y1), (x2, y2)], color, w)
    else: d.line([px(x1), px(y1), px(x2), px(y2)], fill=color, width=max(1, px(w)))
    if arrow:
        a = ang if ang is not None else math.atan2(y2 - y1, x2 - x1)
        _arrowhead(d, x2, y2, a, color)

def _poly_dashed(d, pts, color, w, dash=12, gap=8):
    for i in range(len(pts) - 1):
        x1, y1 = pts[i]; x2, y2 = pts[i + 1]
        dist = math.hypot(x2 - x1, y2 - y1); n = max(1, int(dist / (dash + gap)))
        for k in range(n + 1):
            t0 = (k * (dash + gap)) / dist if dist else 0
            t1 = min(1, (k * (dash + gap) + dash) / dist) if dist else 0
            if t0 >= 1: break
            d.line([px(x1 + (x2 - x1) * t0), px(y1 + (y2 - y1) * t0),
                    px(x1 + (x2 - x1) * t1), px(y1 + (y2 - y1) * t1)], fill=color, width=max(1, px(w)))

# ---------- íconos de servicios ----------
def ic_monitor(d, cx, cy, col):
    rrect(d, cx - 13, cy - 10, 26, 18, r=3, fill="#FFFFFF", outline=col, width=2)
    d.line([px(cx - 6), px(cy + 12), px(cx + 6), px(cy + 12)], fill=col, width=max(1, px(2)))
    d.line([px(cx), px(cy + 8), px(cx), px(cy + 12)], fill=col, width=max(1, px(2)))

def ic_phone(d, cx, cy, col):
    rrect(d, cx - 8, cy - 13, 16, 26, r=4, fill="#FFFFFF", outline=col, width=2)
    d.line([px(cx - 3), px(cy + 9), px(cx + 3), px(cy + 9)], fill=col, width=max(1, px(2)))

def ic_globe(d, cx, cy, col, rr=12):
    d.ellipse([px(cx - rr), px(cy - rr), px(cx + rr), px(cy + rr)], outline=col, width=max(1, px(2)))
    d.ellipse([px(cx - rr * 0.45), px(cy - rr), px(cx + rr * 0.45), px(cy + rr)], outline=col, width=max(1, px(1.5)))
    d.line([px(cx - rr), px(cy), px(cx + rr), px(cy)], fill=col, width=max(1, px(1.5)))

def ic_gateway(d, cx, cy, col):
    # "puerta" / gateway: dos pilares + arco + flecha
    rrect(d, cx - 14, cy - 12, 28, 24, r=4, fill="#FFFFFF", outline=col, width=2)
    d.line([px(cx - 14), px(cy - 3), px(cx + 14), px(cy - 3)], fill=col, width=max(1, px(1.6)))
    for ox in (-7, 0, 7):
        d.line([px(cx + ox), px(cy - 3), px(cx + ox), px(cy + 12)], fill=col, width=max(1, px(1.4)))

def ic_cog(d, cx, cy, col, r=10):
    # engranaje (microservicio)
    for k in range(8):
        a = k * math.pi / 4
        x0, y0 = cx + (r) * math.cos(a), cy + (r) * math.sin(a)
        x1, y1 = cx + (r + 4) * math.cos(a), cy + (r + 4) * math.sin(a)
        d.line([px(x0), px(y0), px(x1), px(y1)], fill=col, width=max(1, px(3)))
    d.ellipse([px(cx - r), px(cy - r), px(cx + r), px(cy + r)], outline=col, width=max(1, px(2.4)), fill="#FFFFFF")
    d.ellipse([px(cx - 3.5), px(cy - 3.5), px(cx + 3.5), px(cy + 3.5)], outline=col, width=max(1, px(2)))

def ic_db(d, cx, cy, col, w=22, h=26):
    x, y = cx - w / 2, cy - h / 2
    ew = h * 0.30
    d.ellipse([px(x), px(y + h - ew), px(x + w), px(y + h)], fill="#FFFFFF", outline=col, width=max(1, px(2)))
    d.rectangle([px(x), px(y + ew / 2), px(x + w), px(y + h - ew / 2)], fill="#FFFFFF")
    d.line([px(x), px(y + ew / 2), px(x), px(y + h - ew / 2)], fill=col, width=max(1, px(2)))
    d.line([px(x + w), px(y + ew / 2), px(x + w), px(y + h - ew / 2)], fill=col, width=max(1, px(2)))
    for k in range(3):
        d.arc([px(x), px(y + k * (ew * 0.7)), px(x + w), px(y + ew + k * (ew * 0.7))], 0, 180, fill=col, width=max(1, px(1.6)))
    d.ellipse([px(x), px(y), px(x + w), px(y + ew)], fill="#FFFFFF", outline=col, width=max(1, px(2)))

def ic_broker(d, cx, cy, col):
    # cola de mensajes: sobres apilados
    for k, off in enumerate((6, 0, -6)):
        x, y = cx - 14, cy - 10 + off + 4
        rrect(d, x, y, 28, 14, r=2, fill="#FFFFFF", outline=col, width=1.8)
    d.line([px(cx - 14), px(cy - 6 + 4), px(cx), px(cy + 1 + 4)], fill=col, width=max(1, px(1.4)))
    d.line([px(cx + 14), px(cy - 6 + 4), px(cx), px(cy + 1 + 4)], fill=col, width=max(1, px(1.4)))

# ---------- nodos ----------
def node(d, x, y, w, h, key, title, sub=None, icon=None, r=10, tfont=14, title_col=None):
    fill, stroke = DRAW[key]
    rrect(d, x, y, w, h, r=r, fill=fill, outline=stroke, width=2)
    tx = x + 14
    if icon:
        icon(d, x + 24, y + h / 2, stroke); tx = x + 46
    tcol = title_col or INK
    if sub:
        text(d, tx, y + h / 2 - (tfont * 0.78), title, F("sb", tfont), tcol)
        text(d, tx, y + h / 2 + 3, sub, F("r", tfont - 3.5), MUTE)
    else:
        for j, ln in enumerate(wrap(d, title, F("sb", tfont), w - (tx - x) - 12)):
            n = len(wrap(d, title, F("sb", tfont), w - (tx - x) - 12))
            textc(d, (tx + x + w - 12) / 2, y + h / 2 - (n - 1) * (tfont * 0.62) + j * (tfont * 1.24), ln, F("sb", tfont), tcol)
    return (x, y, w, h)

def title_block(d, tag, key, title, subtitle):
    fill, stroke = DRAW[key]
    rrect(d, 40, 30, 8, 132, r=4, fill=stroke)
    # chip
    cw = measure(d, tag, F("b", 12.5))[0] + 26
    rrect(d, 60, 34, cw, 30, r=15, fill=fill, outline=stroke, width=1.6)
    textc(d, 60 + cw / 2, 49, tag, F("b", 12.5), INK)
    text(d, 60, 74, title, F("b", 29), INK)
    text(d, 60, 118, subtitle, F("r", 14.5), MUTE)

def save(img, name): img.save(os.path.join(OUT, name), "PNG"); print("->", name)

# ============================================================ FASE 1
def fase1():
    img, d = canvas()
    title_block(d, "FASE 1 · MVP", "blue", "Monolito Modular en 3 Capas",
                "TrainerOS — un solo despliegue para 50–100 entrenadores y < 5.000 alumnos")

    # Clientes (fila de íconos arriba)
    clients = [("Panel Entrenador", "React.js", ic_monitor, "blue"),
               ("App Alumno", "React.js", ic_phone, "green"),
               ("Landing Pública", "Next.js SSG", ic_globe, "yellow")]
    cw, cy, ch = 300, 180, 64
    gap = 60; x0 = (1600 - (cw * 3 + gap * 2)) / 2
    cxs = []
    for i, (t, s, ic, k) in enumerate(clients):
        x = x0 + i * (cw + gap); cxs.append(x + cw / 2)
        node(d, x, cy, cw, ch, k, t, s, icon=ic)

    # Contenedor del monolito
    mx, my, mw, mh = 110, 300, 1380, 520
    dashed_rrect(d, mx, my, mw, mh, r=16, outline="#9AA3AF", width=1.8)
    rrect(d, mx + 18, my + 14, 250, 30, r=6, fill="#EEF1F5", outline="#9AA3AF", width=1.2)
    text(d, mx + 30, my + 20, "Monolito (un solo proceso)", F("sb", 12.5), "#4B5563")

    # flecha clientes -> monolito (al borde superior)
    conn_vh(d, cxs[1], cy + ch, cxs[1], my, color=LINE, w=2.2, busY=my - 26, label="HTTPS / REST", lfont=F("sb", 11))

    def layer_band(y, h, num, name, key, host):
        fill, stroke = DRAW[key]
        rrect(d, mx + 40, y, mw - 80, h, r=10, fill="#FFFFFF", outline=stroke, width=1.8)
        rrect(d, mx + 40, y, 8, h, r=4, fill=stroke)
        d.ellipse([px(mx + 66), px(y + 14), px(mx + 92), px(y + 40)], fill=stroke)
        textc(d, mx + 79, y + 27, str(num), F("b", 13), "#FFFFFF")
        text(d, mx + 104, y + 15, name, F("b", 15), INK)
        cwd = measure(d, host, F("sb", 11))[0] + 24
        rrect(d, mx + mw - 80 - cwd - 16, y + 13, cwd, 28, r=14, fill=fill, outline=stroke, width=1.2)
        textc(d, mx + mw - 80 - cwd - 16 + cwd / 2, y + 27, host, F("sb", 11), INK)

    # Capa 1 Presentación
    ly = 360; lh = 116
    layer_band(ly, lh, 1, "Capa de Presentación", "blue", "Vercel")
    for (t, s, xx) in [("Paneles privados (SPA)", "React.js", mx + 70), ("Landing pública", "Next.js (SSG)", mx + 760)]:
        node(d, xx, ly + 50, 600, 50, "blue", t, s, r=8, tfont=13)
    # Capa 2 Aplicación
    ay = ly + lh + 24; ah = 150
    layer_band(ay, ah, 2, "Capa de Aplicación — API REST · Node.js + Express", "purple", "Render / Railway")
    mods = [("Auth", "Google · JWT"), ("Rutinas", "Constructor"), ("Catálogo", "Ejercicios"), ("Pagos", "Membresías")]
    mw2 = 290; mg = 18; mx0 = mx + 70
    for i, (t, s) in enumerate(mods):
        node(d, mx0 + i * (mw2 + mg), ay + 52, mw2, 72, "purple", t, s, icon=ic_cog, r=8, tfont=14)
    text(d, mx0, ay + 130, "Prisma ORM como capa de abstracción de datos", F("sb", 11.5), MUTE)
    # Capa 3 Datos
    dy = ay + ah + 24; dh = 116
    layer_band(dy, dh, 3, "Capa de Datos", "gray", "PostgreSQL")
    node(d, mx + 70, dy + 48, 560, 52, "gray", "PostgreSQL · modelo relacional único", icon=ic_db, r=8, tfont=13)
    rrect(d, mx + 760, dy + 48, 540, 52, r=8, fill=DRAW["yellow"][0], outline=DRAW["yellow"][1], width=1.8)
    text(d, mx + 778, dy + 62, "Multitenant: cada query inyecta el trainer_id del JWT", F("sb", 12), "#7A5B00")

    # conectores ortogonales entre capas (centro)
    midx = mx + mw / 2
    conn_straight(d, midx, ly + lh, midx, ay, color=LINE, w=2.2)
    conn_straight(d, midx, ay + ah, midx, dy, color=LINE, w=2.2)

    save(img, "fase1_monolito_3capas.png")

# ============================================================ FASE 2A
def fase2a():
    img, d = canvas()
    title_block(d, "FASE 2 · PASO A", "teal", "Microservicios Tradicionales — REST síncrono",
                "El monolito se descompone por capacidades de negocio detrás de un API Gateway")

    # Clientes
    node(d, 660, 180, 280, 58, "blue", "Clientes", "Web · Móvil · B2B", icon=ic_monitor)
    # Gateway
    node(d, 580, 286, 440, 66, "orange", "API Gateway", "ruteo · rate limiting · JWT", icon=ic_gateway, tfont=15)
    conn_straight(d, 800, 238, 800, 286, color=LINE, w=2.2)

    # Cluster microservicios
    cx0, cy0, cw0, ch0 = 70, 400, 1460, 300
    dashed_rrect(d, cx0, cy0, cw0, ch0, r=16, outline="#9AA3AF", width=1.8)
    rrect(d, cx0 + 18, cy0 + 14, 230, 30, r=6, fill="#EEF1F5", outline="#9AA3AF", width=1.2)
    text(d, cx0 + 30, cy0 + 20, "Microservicios", F("sb", 12.5), "#4B5563")

    svcs = [("MS Auth", "& Tenants", "blue"), ("MS Rutinas", "núcleo", "purple"),
            ("MS Catálogo", "lecturas", "green"), ("MS Pagos", "membresías", "orange"),
            ("MS Notificaciones", "push/email", "red")]
    sw, sg = 256, 24; sx0 = cx0 + (cw0 - (sw * 5 + sg * 4)) / 2; sy = cy0 + 64; sh = 84
    cxs = []
    for i, (t, s, k) in enumerate(svcs):
        x = sx0 + i * (sw + sg); cxs.append(x + sw / 2)
        node(d, x, sy, sw, sh, k, t, s, icon=ic_cog, r=8, tfont=14)
        ic_db(d, x + sw / 2, sy + sh + 46, DRAW[k][1])
        textc(d, x + sw / 2, sy + sh + 74, "BD propia", F("sb", 10.5), MUTE)
        conn_straight(d, x + sw / 2, sy + sh, x + sw / 2, sy + sh + 30, color=LINE, w=1.8)
    # gateway -> servicios (ortogonal, bus horizontal)
    for cx in cxs:
        conn_vh(d, 800, 352, cx, sy, color=LINE, w=1.8, busY=380)
    textc(d, cx0 + cw0 / 2, sy + sh + 92, "Patrón Database per Service · una base por microservicio", F("sb", 11), MUTE)

    # nota de límite
    rrect(d, 70, 726, 1460, 88, r=12, fill=DRAW["red"][0], outline=DRAW["red"][1], width=1.8)
    text(d, 96, 742, "Límite — acoplamiento temporal", F("b", 14), "#B85450")
    paragraph(d, 96, 770, "Si Notificaciones está caído, asignar una rutina falla o se demora. Las llamadas en cadena "
              "(Rutinas → Catálogo → Notificaciones) suman latencias: la disponibilidad compuesta es el producto de las individuales.",
              F("r", 12.5), INK, 1400, 1.25)
    save(img, "fase2a_microservicios_tradicionales.png")

# ============================================================ FASE 2B
def fase2b():
    img, d = canvas()
    title_block(d, "FASE 2 · PASO B", "green", "Microservicios Modernos — Orientados a eventos",
                "Los servicios publican hechos de negocio en un Message Broker (desacople temporal)")

    node(d, 70, 250, 230, 56, "blue", "Clientes", icon=ic_monitor, tfont=13)
    node(d, 70, 330, 230, 56, "orange", "API Gateway", icon=ic_gateway, tfont=13)
    conn_straight(d, 185, 306, 185, 330, color=LINE, w=2.0)

    # Publicadores
    pubs = [("MS Rutinas", "publica", "purple", 250), ("MS Pagos", "publica", "orange", 380)]
    for (t, s, k, y) in pubs:
        node(d, 360, y, 250, 70, k, t, s, icon=ic_cog, r=8, tfont=14)
        ic_db(d, 485, y + 92, DRAW[k][1], w=18, h=20)
        conn_straight(d, 485, y + 70, 485, y + 82, color=LINE, w=1.6)

    # Broker (centro)
    bx, by, bw, bh = 660, 250, 300, 360
    rrect(d, bx, by, bw, bh, r=14, fill=DRAW["teal"][0], outline=DRAW["teal"][1], width=2.2)
    ic_broker(d, bx + bw / 2, by + 44, DRAW["teal"][1])
    textc(d, bx + bw / 2, by + 78, "Message Broker", F("b", 15), INK)
    textc(d, bx + bw / 2, by + 100, "Google Pub/Sub", F("sb", 12), MUTE)
    events = ["rutina.asignada", "entrenamiento.completado", "pago.confirmado", "membresia.por_vencer"]
    for i, ev in enumerate(events):
        ey = by + 128 + i * 56
        rrect(d, bx + 26, ey, bw - 52, 44, r=8, fill="#FFFFFF", outline=DRAW["teal"][1], width=1.5)
        textc(d, bx + bw / 2, ey + 22, ev, F("sb", 11.5), "#0E8088")

    # Suscriptores
    subs = [("MS Notificaciones", "push · email · WhatsApp", "purple", 250),
            ("MS Analytics", "métricas de negocio", "teal", 360),
            ("MS Query (CQRS)", "vista materializada", "green", 470)]
    for (t, s, k, y) in subs:
        node(d, 1020, y, 510, 78, k, t, s, icon=ic_cog, r=8, tfont=14)

    # conectores: publicadores -> broker, broker -> suscriptores (ortogonales)
    conn_hv(d, 610, 285, bx, by + 150, color=LINE, w=2.0, busX=635, label="publish")
    conn_hv(d, 610, 415, bx, by + 200, color=LINE, w=2.0, busX=635)
    for (_, _, _, y) in subs:
        conn_hv(d, bx + bw, by + bh / 2, 1020, y + 39, color=LINE, w=1.9, busX=990, label=None)

    rrect(d, 70, 720, 1460, 92, r=12, fill=DRAW["green"][0], outline=DRAW["green"][1], width=1.8)
    text(d, 96, 738, "Desacople temporal + resiliencia", F("b", 14), "#5A8A3C")
    paragraph(d, 96, 766, "Una caída de Notificaciones ya no afecta la asignación de rutinas: los eventos se reintentan "
              "(at-least-once). El lado de lectura (CQRS) escala por separado del de escritura. Patrones: CQRS · Saga · Circuit Breaker.",
              F("r", 12.5), INK, 1400, 1.25)
    save(img, "fase2b_microservicios_modernos.png")

# ============================================================ EVOLUCIÓN (3 arquitecturas)
def evolucion():
    img, d = canvas("#FFFFFF")
    rect(d, 0, 0, 1600, 8, fill=DRAW["blue"][1])
    text(d, 50, 34, "La evolución en una mirada — Fases 1 y 2", F("b", 28), INK)
    text(d, 50, 76, "Misma idea de negocio, tres arquitecturas. Cada salto lo paga una necesidad real del negocio.",
         F("r", 14.5), MUTE)

    panels = [("FASE 1", "blue", "Monolito modular · 3 capas", ic_monitor,
               ["Presentación · Aplicación · Datos", "Un deploy, una base PostgreSQL", "Node.js + Express + Prisma"],
               "≈ USD 7–16 / mes · MVP"),
              ("FASE 2 · A", "teal", "Microservicios tradicionales", ic_gateway,
               ["API Gateway + 5 microservicios", "Database per Service", "Comunicación REST síncrona"],
               "Autonomía de equipos · acopla en el tiempo"),
              ("FASE 2 · B", "green", "Microservicios modernos (eventos)", ic_broker,
               ["Message Broker · Pub/Sub", "CQRS · Saga · Circuit Breaker", "Desacople temporal · resiliencia"],
               "Escala y tolera fallos · event-driven")]
    pw = 466; gap = 40; x0 = (1600 - (pw * 3 + gap * 2)) / 2; py = 140; ph = 590
    for i, (tag, key, title, icon, items, foot) in enumerate(panels):
        fill, stroke = DRAW[key]
        x = x0 + i * (pw + gap)
        rrect(d, x, py, pw, ph, r=14, fill="#FFFFFF", outline=stroke, width=2)
        rrect(d, x, py, pw, 8, r=4, fill=stroke)
        cwc = measure(d, tag, F("b", 13))[0] + 24
        rrect(d, x + 28, py + 28, cwc, 30, r=15, fill=fill, outline=stroke, width=1.4)
        textc(d, x + 28 + cwc / 2, py + 43, tag, F("b", 13), INK)
        icon(d, x + pw - 50, py + 44, stroke)
        for j, ln in enumerate(wrap(d, title, F("b", 17), pw - 56)):
            text(d, x + 28, py + 80 + j * 26, ln, F("b", 17), INK)
        yy = py + 156
        for it in items:
            rrect(d, x + 28, yy, pw - 56, 72, r=10, fill=fill, outline=stroke, width=1.3)
            for j, ln in enumerate(wrap(d, it, F("sb", 12.5), pw - 96)):
                n = len(wrap(d, it, F("sb", 12.5), pw - 96))
                textc(d, x + pw / 2, yy + 36 - (n - 1) * 9 + j * 18, ln, F("sb", 12.5), INK)
            yy += 84
        rrect(d, x + 28, py + ph - 60, pw - 56, 42, r=10, fill="#F8FAFC", outline=stroke, width=1.3)
        textc(d, x + pw / 2, py + ph - 39, foot, F("sb", 11.5), stroke if key != "yellow" else INK)
    for i in range(2):
        xa = x0 + (i + 1) * pw + i * gap
        conn_straight(d, xa + 6, py + ph / 2, xa + gap - 6, py + ph / 2, color=DRAW["green"][1], w=3.0)
    textc(d, 800, 770, "Narrativa de venta al CTO:  “empezamos por USD 16/mes y escalamos solo cuando el negocio lo pagó”.",
          F("sb", 13.5), MUTE)
    save(img, "evolucion_3_arquitecturas.png")

if __name__ == "__main__":
    fase1(); fase2a(); fase2b(); evolucion(); print("Listo.")
