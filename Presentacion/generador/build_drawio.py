# -*- coding: utf-8 -*-
"""
Genera los diagramas como archivos .drawio REALES (mxGraph XML), estilo draw.io
clásico/profesional: rectángulos rectos, bordes y flechas negras, rellenos planos
(azul, dorado, verde), flujo vertical. Se renderizan a PNG con draw.io desktop.
"""
import os
from xml.sax.saxutils import escape

OUTDIR = r"C:\Users\Conrado\Desktop\Programacion\UNSTA\app-development\Final\Presentacion\diagramas\drawio"
os.makedirs(OUTDIR, exist_ok=True)

# Paleta clásica (rellenos fuertes, borde siempre negro)
BLUE   = "#CFE2F3"   # clientes / presentación / infra
GOLD   = "#FFD966"   # módulos / microservicios
GOLDST = "#FFC000"   # Prisma ORM / acento
CREAM  = "#FFF2CC"   # contenedores
GREEN  = "#D9EAD3"   # bases de datos
REDN   = "#F4CCCC"   # notas de límite
WHITE  = "#FFFFFF"
GRAY   = "#999999"

class Dio:
    def __init__(self): self.cells=[]; self._id=1
    def _nid(self): self._id+=1; return f"n{self._id}"
    def node(self, x, y, w, h, label, style, parent="1"):
        nid=self._nid(); val=escape(label.replace("\n","<br>"))
        self.cells.append(f'<mxCell id="{nid}" value="{val}" style="{style}" vertex="1" parent="{parent}">'
                          f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return nid
    def edge(self, src, tgt, label="", extra="", exit=None, entry=None):
        nid=self._nid()
        s=("edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;endFill=1;"
           "strokeColor=#000000;strokeWidth=1.5;fontSize=12;fontColor=#000000;"
           "labelBackgroundColor=#FFFFFF;"+extra)
        if exit:  s+=f"exitX={exit[0]};exitY={exit[1]};exitDx=0;exitDy=0;"
        if entry: s+=f"entryX={entry[0]};entryY={entry[1]};entryDx=0;entryDy=0;"
        self.cells.append(f'<mxCell id="{nid}" value="{escape(label)}" style="{s}" edge="1" parent="1" '
                          f'source="{src}" target="{tgt}"><mxGeometry relative="1" as="geometry"/></mxCell>')
        return nid
    def line(self, x, y, w):
        self.cells.append(f'<mxCell id="{self._nid()}" value="" style="line;strokeColor=#CCCCCC;html=1;" '
                          f'vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{w}" height="10" as="geometry"/></mxCell>')
    def xml(self):
        return ('<mxfile host="app.diagrams.net"><diagram name="Arquitectura" id="d1">'
                '<mxGraphModel dx="1400" dy="900" grid="0" guides="1" tooltips="1" connect="1" '
                'arrows="1" fold="1" page="0" math="0" shadow="0"><root>'
                '<mxCell id="0"/><mxCell id="1" parent="0"/>'+ "".join(self.cells)
                +'</root></mxGraphModel></diagram></mxfile>')

def box(fill, extra=""):
    return f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor=#000000;strokeWidth=1;fontSize=14;fontColor=#000000;{extra}"
def container(fill=CREAM, extra=""):
    return f"rounded=0;whiteSpace=wrap;html=1;fillColor={fill};strokeColor=#000000;strokeWidth=1;verticalAlign=top;align=center;fontSize=14;fontStyle=1;fontColor=#000000;spacingTop=10;{extra}"
def db(fill=GREEN):
    return f"shape=cylinder3;whiteSpace=wrap;html=1;boundedLbl=1;backgroundOutline=1;size=12;fillColor={fill};strokeColor=#000000;fontSize=12;fontColor=#000000;verticalAlign=middle;"
def header(d, fase):
    d.node(36, 14, 1000, 20, "TFI – Desarrollo de Aplicaciones Web · TrainerOS", "text;html=1;align=left;fontSize=13;fontColor=#999999;")
    d.line(36, 30, 1180)
    d.node(36, 48, 1100, 28, fase, "text;html=1;align=left;fontSize=19;fontStyle=1;fontColor=#000000;")

def save(name, xml):
    with open(os.path.join(OUTDIR, name), "w", encoding="utf-8") as f: f.write(xml)
    print("->", name)

# ===================================================== FASE 1
def fase1():
    d=Dio(); header(d, "Fase 1 — Monolito Modular en 3 Capas (MVP)")
    cli = d.node(470, 110, 240, 74, "Clientes\n(Entrenador / Alumno)\nNavegador y móvil", box(BLUE))
    pres = d.node(450, 244, 280, 80, "Capa de Presentación\nReact + Next.js (Vercel)\nSSG / SEO en la landing", box(BLUE))
    cont = d.node(120, 392, 840, 250, "MONOLITO MODULAR — API REST · Node.js / Express (Render)", container(CREAM))
    mods = [("Módulo\nAuth (JWT)", 150), ("Módulo\nRutinas", 360), ("Módulo\nCatálogo Ejercicios", 570), ("Módulo\nPagos / Membresías", 760)]
    mids=[]
    for lab,x in mods:
        mids.append(d.node(x, 440, 180, 64, lab, box(GOLD)))
    prisma = d.node(390, 556, 300, 64, "Prisma ORM\n(inyecta tenant_id en cada query)", box(GOLDST, "fontStyle=1;"))
    pg = d.node(450, 700, 280, 96, "PostgreSQL gestionado\n(Neon / Railway)\nMultitenant por trainer_id", db(GREEN))

    d.edge(cli, pres, "HTTPS", exit=(0.5,1), entry=(0.5,0))
    d.edge(pres, cont, "REST / JSON + JWT", exit=(0.5,1), entry=(0.5,0))
    for m in mids:
        d.edge(m, prisma, exit=(0.5,1), entry=(0.5,0))
    d.edge(prisma, pg, "SQL", exit=(0.5,1), entry=(0.5,0))
    save("fase1_monolito_3capas.drawio", d.xml())

# ===================================================== FASE 2A
def fase2a():
    d=Dio(); header(d, "Fase 2 · Paso A — Microservicios Tradicionales (REST síncrono)")
    cli = d.node(660, 110, 240, 60, "Clientes\nWeb · Móvil · B2B", box(BLUE))
    gw = d.node(640, 206, 280, 58, "API Gateway\nruteo · rate limiting · JWT", box(BLUE, "fontStyle=1;"))
    d.edge(cli, gw, exit=(0.5,1), entry=(0.5,0))

    cont = d.node(90, 320, 1380, 280, "MICROSERVICIOS", container(CREAM))
    svcs = [("MS Auth\n& Tenants",), ("MS Rutinas\nnúcleo",), ("MS Catálogo\nlecturas",), ("MS Pagos\nmembresías",), ("MS Notificaciones\npush · email",)]
    n=len(svcs); sw=230; gap=26; x0=90+(1380-(sw*n+gap*(n-1)))//2; sy=372
    for i,(lab,) in enumerate(svcs):
        x=x0+i*(sw+gap)
        s=d.node(x, sy, sw, 66, lab, box(GOLD))
        dbi=d.node(x+sw//2-45, sy+118, 90, 60, "BD\npropia", db(GREEN))
        d.edge(gw, s, exit=(0.5,1), entry=(0.5,0))
        d.edge(s, dbi, exit=(0.5,1), entry=(0.5,0))
    d.node(x0, sy+186, 600, 22, "Patrón Database per Service · una base por microservicio", "text;html=1;align=left;fontSize=12;fontColor=#444444;")
    d.node(90, 624, 1380, 78, "<b>Límite — acoplamiento temporal.</b>  Si Notificaciones está caído, asignar una rutina falla o se demora. Las llamadas en cadena (Rutinas → Catálogo → Notificaciones) suman latencias: la disponibilidad compuesta es el producto de las individuales.", box(REDN, "align=left;spacingLeft=12;verticalAlign=middle;"))
    save("fase2a_microservicios_tradicionales.drawio", d.xml())

# ===================================================== FASE 2B
def fase2b():
    d=Dio(); header(d, "Fase 2 · Paso B — Microservicios Modernos (orientados a eventos)")
    cli=d.node(70, 200, 220, 50, "Clientes", box(BLUE))
    gw=d.node(70, 280, 220, 50, "API Gateway", box(BLUE, "fontStyle=1;"))
    d.edge(cli, gw, exit=(0.5,1), entry=(0.5,0))

    rut=d.node(350, 200, 240, 60, "MS Rutinas\npublica", box(GOLD))
    pag=d.node(350, 330, 240, 60, "MS Pagos\npublica", box(GOLD))
    d.node(430, 274, 80, 44, "BD", db(GREEN))
    d.node(430, 404, 80, 44, "BD", db(GREEN))

    broker=d.node(650, 190, 300, 360, "Message Broker — Google Pub/Sub", container(BLUE))
    for i,ev in enumerate(["rutina.asignada","entrenamiento.completado","pago.confirmado","membresia.por_vencer"]):
        d.node(676, 260+i*66, 248, 48, ev, box(WHITE))

    subs=[("MS Notificaciones\npush · email · WhatsApp",200),("MS Analytics\nmétricas de negocio",310),("MS Query (CQRS)\nvista materializada",420)]
    sids=[d.node(1030, y, 470, 64, lab, box(GOLD)) for lab,y in subs]

    d.edge(rut, broker, "publica", exit=(1,0.5), entry=(0,0.35))
    d.edge(pag, broker, exit=(1,0.5), entry=(0,0.65))
    for s in sids:
        d.edge(broker, s, exit=(1,0.5), entry=(0,0.5))
    d.node(70, 600, 1450, 86, "<b>Desacople temporal + resiliencia.</b>  Una caída de Notificaciones ya no afecta la asignación de rutinas: los eventos se reintentan (at-least-once). El lado de lectura (CQRS) escala por separado del de escritura. Patrones: CQRS · Saga · Circuit Breaker.", box(GREEN, "align=left;spacingLeft=12;verticalAlign=middle;"))
    save("fase2b_microservicios_modernos.drawio", d.xml())

# ===================================================== EVOLUCIÓN
def evolucion():
    d=Dio(); header(d, "La evolución en una mirada — Fases 1 y 2")
    panels=[("FASE 1 — Monolito modular · 3 capas",
             ["Presentación · Aplicación · Datos","Un deploy, una base PostgreSQL","Node.js + Express + Prisma"],"≈ USD 7–16 / mes · MVP"),
            ("FASE 2 · A — Microservicios tradicionales",
             ["API Gateway + 5 microservicios","Database per Service","Comunicación REST síncrona"],"Autonomía de equipos · acopla en el tiempo"),
            ("FASE 2 · B — Microservicios modernos (eventos)",
             ["Message Broker · Pub/Sub","CQRS · Saga · Circuit Breaker","Desacople temporal · resiliencia"],"Escala y tolera fallos · event-driven")]
    pw=440; gap=50; x0=70; py=120; ph=520; pids=[]
    for i,(t,items,foot) in enumerate(panels):
        x=x0+i*(pw+gap)
        p=d.node(x, py, pw, ph, t, container(CREAM, "verticalAlign=top;spacingTop=12;fontSize=15;"))
        pids.append(p)
        for j,it in enumerate(items):
            d.node(x+30, py+70+j*92, pw-60, 70, it, box(BLUE))
        d.node(x+30, py+ph-66, pw-60, 44, foot, box(GOLD, "fontStyle=1;"))
    d.edge(pids[0], pids[1], exit=(1,0.5), entry=(0,0.5))
    d.edge(pids[1], pids[2], exit=(1,0.5), entry=(0,0.5))
    d.node(70, py+ph+24, 1390, 24, "Narrativa de venta al CTO: “empezamos por USD 16/mes y escalamos solo cuando el negocio lo pagó”.", "text;html=1;align=center;fontSize=13;fontStyle=1;fontColor=#444444;")
    save("evolucion_3_arquitecturas.drawio", d.xml())

if __name__=="__main__":
    fase1(); fase2a(); fase2b(); evolucion(); print("Listo.")
