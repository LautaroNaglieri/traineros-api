# -*- coding: utf-8 -*-
"""
Genera archivos .drawio REALES (mxGraph XML) de los diagramas de arquitectura.
Se renderizan a PNG con el draw.io desktop (ver render_drawio.sh).
Estilo nativo draw.io: paleta oficial, formas (cilindro, actor, hexágono, proceso),
sombras y conectores ortogonales con esquinas redondeadas.
"""
import os
from xml.sax.saxutils import escape

OUTDIR = r"C:\Users\Conrado\Desktop\Programacion\UNSTA\app-development\Final\Presentacion\diagramas\drawio"
os.makedirs(OUTDIR, exist_ok=True)

PAL = {
    "blue":   "fillColor=#dae8fc;strokeColor=#6c8ebf",
    "green":  "fillColor=#d5e8d4;strokeColor=#82b366",
    "orange": "fillColor=#ffe6cc;strokeColor=#d79b00",
    "yellow": "fillColor=#fff2cc;strokeColor=#d6b656",
    "purple": "fillColor=#e1d5e7;strokeColor=#9673a6",
    "red":    "fillColor=#f8cecc;strokeColor=#b85450",
    "gray":   "fillColor=#f5f5f5;strokeColor=#666666",
    "teal":   "fillColor=#b0e3e6;strokeColor=#0e8088",
}
STROKE = {k: v.split("strokeColor=")[1] for k, v in PAL.items()}
INK = "#23272E"

class Dio:
    def __init__(self):
        self.cells = []
        self._id = 1

    def _nid(self):
        self._id += 1
        return f"n{self._id}"

    def node(self, x, y, w, h, label, style, parent="1"):
        nid = self._nid()
        val = escape(label.replace("\n", "<br>"))
        self.cells.append(
            f'<mxCell id="{nid}" value="{val}" style="{style}" vertex="1" parent="{parent}">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>'
        )
        return nid

    def edge(self, src, tgt, style="", label="", exit=None, entry=None):
        nid = self._nid()
        s = ("edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=block;endFill=1;"
             "strokeColor=#4D4D4D;strokeWidth=1.6;fontSize=11;fontColor=#6B7280;" + style)
        if exit:  s += f"exitX={exit[0]};exitY={exit[1]};exitDx=0;exitDy=0;"
        if entry: s += f"entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;"
        self.cells.append(
            f'<mxCell id="{nid}" value="{escape(label)}" style="{s}" edge="1" parent="1" '
            f'source="{src}" target="{tgt}"><mxGeometry relative="1" as="geometry"/></mxCell>'
        )
        return nid

    def xml(self, w=1600, h=900):
        body = "".join(self.cells)
        return (
            '<mxfile host="app.diagrams.net">'
            f'<diagram name="Arquitectura" id="d1">'
            f'<mxGraphModel dx="{w}" dy="{h}" grid="0" gridSize="10" guides="1" tooltips="1" '
            f'connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{w}" pageHeight="{h}" '
            f'math="0" shadow="0"><root>'
            '<mxCell id="0"/><mxCell id="1" parent="0"/>'
            f'{body}</root></mxGraphModel></diagram></mxfile>'
        )

# ---- estilos reutilizables ----
def box(c, extra=""):       return f"rounded=1;whiteSpace=wrap;html=1;{PAL[c]};fontSize=14;fontColor={INK};shadow=1;{extra}"
def proc(c, extra=""):      return f"shape=process;whiteSpace=wrap;html=1;{PAL[c]};fontSize=14;fontColor={INK};shadow=1;{extra}"
def db(c, extra=""):        return f"shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=14;{PAL[c]};fontSize=11;fontColor={INK};shadow=1;{extra}"
def actor(c):               return f"shape=actor;whiteSpace=wrap;html=1;{PAL[c]};fontSize=12;fontColor={INK};verticalLabelPosition=bottom;verticalAlign=top;shadow=1;"
def hexa(c, extra=""):      return f"shape=hexagon;perimeter=hexagonPerimeter2;whiteSpace=wrap;html=1;fixedSize=1;{PAL[c]};fontSize=14;fontStyle=1;fontColor={INK};shadow=1;{extra}"
def cluster(label=""):      return "rounded=1;whiteSpace=wrap;html=1;dashed=1;dashPattern=8 6;strokeColor=#9AA3AF;fillColor=none;verticalAlign=top;align=left;spacingLeft=14;spacingTop=10;fontSize=13;fontColor=#4B5563;fontStyle=1;"
def note(c):                return f"rounded=1;whiteSpace=wrap;html=1;{PAL[c]};fontSize=12;fontColor={INK};align=left;spacingLeft=12;spacingTop=8;verticalAlign=top;shadow=0;"
def title(size=26):        return f"text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;fontSize={size};fontStyle=1;fontColor={INK};"
def sub():                  return "text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=top;fontSize=14;fontColor=#6B7280;"
def chip(c):                return f"rounded=1;arcSize=50;whiteSpace=wrap;html=1;{PAL[c]};fontSize=12;fontStyle=1;fontColor={INK};"

def save(name, xml):
    p = os.path.join(OUTDIR, name)
    with open(p, "w", encoding="utf-8") as f:
        f.write(xml)
    print("->", name)

# ===================================================== FASE 1
def fase1():
    d = Dio()
    d.node(40, 24, 220, 26, "FASE 1 · MVP", chip("blue"))
    d.node(40, 58, 1000, 34, "Monolito Modular en 3 Capas", title(26))
    d.node(40, 96, 1100, 24, "TrainerOS — un solo despliegue para 50–100 entrenadores y &lt; 5.000 alumnos", sub())

    # clientes
    cli = [("Panel Entrenador\n(React.js)", "blue", 540),
           ("App Alumno\n(React.js)", "green", 720),
           ("Landing Pública\n(Next.js SSG)", "yellow", 900)]
    cids = []
    for lab, col, x in cli:
        cids.append(d.node(x, 150, 150, 70, lab, actor(col)))

    # contenedor monolito
    mono = d.node(120, 270, 1360, 540, "Monolito (un solo proceso)", cluster())

    def band(y, label, col, host):
        b = d.node(160, y, 1280, 130, "", f"rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor={STROKE[col]};verticalAlign=top;align=left;spacingLeft=46;spacingTop=12;fontSize=15;fontStyle=1;fontColor={INK};shadow=1;")
        d.node(178, y+14, 26, 26, label.split("|")[0], f"ellipse;whiteSpace=wrap;html=1;fillColor={STROKE[col]};strokeColor={STROKE[col]};fontColor=#ffffff;fontSize=13;fontStyle=1;")
        d.node(206, y+12, 700, 28, label.split("|")[1], f"text;html=1;align=left;verticalAlign=middle;fontSize=15;fontStyle=1;fontColor={INK};")
        d.node(1240, y+12, 180, 26, host, chip(col))
        return b, y

    b1, y1 = band(300, "1|Capa de Presentación", "blue", "Vercel")
    d.node(180, y1+52, 600, 56, "Paneles privados (SPA)\nReact.js", box("blue"))
    d.node(810, y1+52, 600, 56, "Landing pública\nNext.js (SSG)", box("blue"))

    b2, y2 = band(450, "2|Capa de Aplicación — API REST · Node.js + Express", "purple", "Render / Railway")
    mods = [("Auth\nGoogle · JWT", 180), ("Rutinas\nConstructor", 500), ("Catálogo\nEjercicios", 820), ("Pagos\nMembresías", 1140)]
    for lab, x in mods:
        d.node(x, y2+54, 280, 60, lab, proc("purple"))

    b3, y3 = band(600, "3|Capa de Datos", "gray", "PostgreSQL")
    dbid = d.node(200, y3+48, 90, 64, "PostgreSQL", db("gray"))
    d.node(310, y3+58, 460, 44, "Modelo relacional único\n(Entrenador · Alumno · Rutina · Membresía)", f"text;html=1;align=left;verticalAlign=middle;fontSize=12;fontColor={INK};")
    d.node(900, y3+52, 520, 50, "Multitenant: cada query inyecta el trainer_id del JWT", note("yellow"))

    # conectores ortogonales entre capas
    d.edge(cids[1], b1, label="HTTPS / REST", exit=(0.5, 1), entry=(0.5, 0))
    d.edge(b1, b2, exit=(0.5, 1), entry=(0.5, 0))
    d.edge(b2, b3, exit=(0.5, 1), entry=(0.5, 0))
    save("fase1_monolito_3capas.drawio", d.xml())

# ===================================================== FASE 2A
def fase2a():
    d = Dio()
    d.node(40, 24, 240, 26, "FASE 2 · PASO A", chip("teal"))
    d.node(40, 58, 1100, 34, "Microservicios Tradicionales — REST síncrono", title(26))
    d.node(40, 96, 1200, 24, "El monolito se descompone por capacidades de negocio detrás de un API Gateway", sub())

    cli = d.node(700, 150, 200, 60, "Clientes\nWeb · Móvil · B2B", box("blue"))
    gw = d.node(640, 250, 320, 60, "API Gateway\nruteo · rate limiting · JWT", hexa("orange"))
    d.edge(cli, gw, exit=(0.5, 1), entry=(0.5, 0))

    clu = d.node(80, 360, 1440, 320, "Microservicios", cluster())
    svcs = [("MS Auth\n& Tenants", "blue"), ("MS Rutinas\nnúcleo", "purple"),
            ("MS Catálogo\nlecturas", "green"), ("MS Pagos\nmembresías", "orange"),
            ("MS Notificaciones\npush · email", "red")]
    n = len(svcs); sw = 250; gap = 26
    x0 = 80 + (1440 - (sw*n + gap*(n-1)))/2
    sy = 420
    for i, (lab, col) in enumerate(svcs):
        x = x0 + i*(sw+gap)
        s = d.node(x, sy, sw, 70, lab, proc(col))
        dbi = d.node(x + sw/2 - 40, sy+120, 80, 56, "BD propia", db(col))
        d.edge(gw, s, exit=(0.5, 1), entry=(0.5, 0))
        d.edge(s, dbi, exit=(0.5, 1), entry=(0.5, 0))
    d.node(x0, sy+186, 600, 24, "Patrón Database per Service · una base por microservicio", f"text;html=1;align=left;fontSize=12;fontColor=#6B7280;")

    d.node(80, 700, 1440, 86, "<b>Límite — acoplamiento temporal.</b>  Si Notificaciones está caído, asignar una rutina falla o se demora. Las llamadas en cadena (Rutinas → Catálogo → Notificaciones) suman latencias: la disponibilidad compuesta es el producto de las individuales.", note("red"))
    save("fase2a_microservicios_tradicionales.drawio", d.xml())

# ===================================================== FASE 2B
def fase2b():
    d = Dio()
    d.node(40, 24, 240, 26, "FASE 2 · PASO B", chip("green"))
    d.node(40, 58, 1150, 34, "Microservicios Modernos — Orientados a eventos", title(26))
    d.node(40, 96, 1250, 24, "Los servicios publican hechos de negocio en un Message Broker (desacople temporal)", sub())

    cli = d.node(70, 250, 220, 50, "Clientes", box("blue"))
    gw = d.node(70, 330, 220, 50, "API Gateway", hexa("orange"))
    d.edge(cli, gw, exit=(0.5, 1), entry=(0.5, 0))

    rut = d.node(360, 250, 240, 64, "MS Rutinas\npublica", proc("purple"))
    pag = d.node(360, 380, 240, 64, "MS Pagos\npublica", proc("orange"))
    d.node(440, 326, 80, 46, "BD", db("purple"))
    d.node(440, 456, 80, 46, "BD", db("orange"))

    broker = d.node(660, 240, 300, 380, "Message Broker\nGoogle Pub/Sub", f"rounded=1;whiteSpace=wrap;html=1;{PAL['teal']};verticalAlign=top;align=center;spacingTop=14;fontSize=15;fontStyle=1;fontColor={INK};shadow=1;")
    events = ["rutina.asignada", "entrenamiento.completado", "pago.confirmado", "membresia.por_vencer"]
    for i, ev in enumerate(events):
        d.node(686, 320 + i*64, 248, 46, ev, f"rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#0e8088;fontSize=12;fontColor=#0e8088;")

    subs = [("MS Notificaciones\npush · email · WhatsApp", "purple", 250),
            ("MS Analytics\nmétricas de negocio", "teal", 360),
            ("MS Query (CQRS)\nvista materializada", "green", 470)]
    sids = []
    for lab, col, y in subs:
        sids.append(d.node(1040, y, 480, 70, lab, proc(col)))

    d.edge(rut, broker, label="publish", exit=(1, 0.5), entry=(0, 0.4))
    d.edge(pag, broker, exit=(1, 0.5), entry=(0, 0.6))
    for sid in sids:
        d.edge(broker, sid, exit=(1, 0.5), entry=(0, 0.5))

    d.node(70, 700, 1450, 90, "<b>Desacople temporal + resiliencia.</b>  Una caída de Notificaciones ya no afecta la asignación de rutinas: los eventos se reintentan (at-least-once). El lado de lectura (CQRS) escala por separado del de escritura. Patrones: CQRS · Saga · Circuit Breaker.", note("green"))
    save("fase2b_microservicios_modernos.drawio", d.xml())

# ===================================================== EVOLUCIÓN
def evolucion():
    d = Dio()
    d.node(40, 30, 1000, 34, "La evolución en una mirada — Fases 1 y 2", title(26))
    d.node(40, 70, 1300, 24, "Misma idea de negocio, tres arquitecturas. Cada salto lo paga una necesidad real del negocio.", sub())
    panels = [("FASE 1", "blue", "Monolito modular · 3 capas",
               ["Presentación · Aplicación · Datos", "Un deploy, una base PostgreSQL", "Node.js + Express + Prisma"], "≈ USD 7–16 / mes · MVP"),
              ("FASE 2 · A", "teal", "Microservicios tradicionales",
               ["API Gateway + 5 microservicios", "Database per Service", "Comunicación REST síncrona"], "Autonomía de equipos · acopla en el tiempo"),
              ("FASE 2 · B", "green", "Microservicios modernos (eventos)",
               ["Message Broker · Pub/Sub", "CQRS · Saga · Circuit Breaker", "Desacople temporal · resiliencia"], "Escala y tolera fallos · event-driven")]
    pw, gap, x0, py, ph = 460, 50, 60, 140, 590
    pids = []
    for i, (tag, col, t, items, foot) in enumerate(panels):
        x = x0 + i*(pw+gap)
        p = d.node(x, py, pw, ph, "", f"rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor={STROKE[col]};verticalAlign=top;shadow=1;")
        pids.append(p)
        d.node(x+28, py+26, 130, 28, tag, chip(col))
        d.node(x+28, py+72, pw-56, 30, t, f"text;html=1;align=left;fontSize=17;fontStyle=1;fontColor={INK};")
        for j, it in enumerate(items):
            d.node(x+28, py+130 + j*82, pw-56, 64, it, box(col))
        d.node(x+28, py+ph-58, pw-56, 40, foot, f"rounded=1;whiteSpace=wrap;html=1;fillColor=#f8fafc;strokeColor={STROKE[col]};fontSize=12;fontStyle=1;fontColor={STROKE[col]};")
    d.edge(pids[0], pids[1], style="endArrow=block;strokeColor=#82b366;strokeWidth=3;", exit=(1, 0.5), entry=(0, 0.5))
    d.edge(pids[1], pids[2], style="endArrow=block;strokeColor=#82b366;strokeWidth=3;", exit=(1, 0.5), entry=(0, 0.5))
    d.node(60, 760, 1400, 24, "Narrativa de venta al CTO: “empezamos por USD 16/mes y escalamos solo cuando el negocio lo pagó”.", f"text;html=1;align=center;fontSize=13;fontStyle=1;fontColor=#6B7280;")
    save("evolucion_3_arquitecturas.drawio", d.xml())

if __name__ == "__main__":
    fase1(); fase2a(); fase2b(); evolucion(); print("Listo.")
