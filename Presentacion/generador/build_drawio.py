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
    cli = d.node(720, 96, 240, 56, "Clientes\nWeb · Móvil · B2B", box(BLUE))
    gw  = d.node(690, 182, 300, 58, "API Gateway\nruteo · rate limiting · JWT", box(BLUE, "fontStyle=1;"))
    d.edge(cli, gw, exit=(0.5,1), entry=(0.5,0))

    cont = d.node(60, 300, 1560, 300, "MICROSERVICIOS", container(CREAM))
    # Orden pensado para que las llamadas REST queden entre cajas ADYACENTES (sin cruces):
    # Notificaciones queda al centro-derecha, llamado por Rutinas (izq) y Pagos (der).
    svcs = [
        ("MS Auth\n& Tenants",                       "BD Auth\nusuarios · tenants",                          100, 100),
        ("MS Catálogo\nlecturas",                    "BD Catálogo\nejercicios",                              410, 100),
        ("MS Rutinas\nnúcleo",                       "BD Rutinas\nrutinas · asignaciones",                   720, 100),
        ("MS Notificaciones\npush · email · WhatsApp","BD Notif.\nlog envíos · plantillas\nprefs · idempotencia", 1030, 150),
        ("MS Pagos\nmembresías",                     "BD Pagos\nmembresías · facturas",                     1340, 100),
    ]
    ids={}
    for i,(lab,dblab,x,dbw) in enumerate(svcs):
        s=d.node(x, 356, 240, 66, lab, box(GOLD))
        cx=x+120
        dbi=d.node(cx-dbw//2, 504, dbw, 80, dblab, db(GREEN))
        d.edge(s, dbi, exit=(0.5,1), entry=(0.5,0))
        ids[i]=s
    # Gateway -> servicios client-facing (Notificaciones NO es client-facing)
    for i in (0,1,2,4):
        d.edge(gw, ids[i], exit=(0.5,1), entry=(0.5,0))
    # Llamadas REST síncronas entre servicios (rojo punteado) — todas entre adyacentes
    red="strokeColor=#CC0000;fontColor=#CC0000;dashed=1;dashPattern=6 4;"
    d.edge(ids[2], ids[1], "REST", extra=red, exit=(0,0.5), entry=(1,0.5))   # Rutinas -> Catálogo (valida ejercicios)
    d.edge(ids[2], ids[3], "REST", extra=red, exit=(1,0.5), entry=(0,0.5))   # Rutinas -> Notificaciones (avisa al alumno)
    d.edge(ids[4], ids[3], "REST", extra=red, exit=(0,0.5), entry=(1,0.5))   # Pagos   -> Notificaciones (aviso de pago)
    d.node(100, 612, 900, 22, "Flechas rojas punteadas = llamadas REST síncronas entre servicios (acoplamiento).", "text;html=1;align=left;fontSize=12;fontColor=#CC0000;")
    d.node(100, 634, 900, 22, "Patrón Database per Service · cada microservicio es dueño de su propia base.", "text;html=1;align=left;fontSize=12;fontColor=#444444;")
    d.node(60, 668, 1560, 80, "<b>Límite — acoplamiento temporal.</b>  Las llamadas entre servicios son síncronas: si Notificaciones está caído, asignar una rutina (Rutinas → Notificaciones) falla o se demora, aunque el alumno no necesite el aviso al instante. Las cadenas REST suman latencias y multiplican los puntos de fallo: la disponibilidad compuesta es el producto de las individuales.", box(REDN, "align=left;spacingLeft=12;verticalAlign=middle;"))
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
    # El Gateway rutea los comandos del cliente al lado de escritura (Rutinas / Pagos)
    d.edge(gw, rut, "comandos REST", exit=(1,0.5), entry=(0,0.5))
    d.edge(gw, pag, extra="", exit=(1,0.5), entry=(0,0.5))

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

# ===================================================== FASE 3
def fase3():
    d=Dio(); header(d, "Fase 3 — Robustez y Escalabilidad (caché · read replicas · LB · auto-scaling)")
    cli = d.node(700, 96, 240, 50, "Clientes\nWeb · Móvil · B2B", box(BLUE))
    cdn = d.node(120, 174, 250, 56, "CDN\nassets · videos de técnica (edge)", box(BLUE))
    lb  = d.node(680, 174, 300, 58, "Cloud Load Balancer\nHTTPS · termina TLS · multi-zona", box(BLUE, "fontStyle=1;"))
    gw  = d.node(680, 266, 300, 52, "API Gateway ×N (réplicas)", box(BLUE, "fontStyle=1;"))
    d.edge(cli, cdn, "estáticos", exit=(0,0.5), entry=(0.5,0))
    d.edge(cli, lb, exit=(0.5,1), entry=(0.5,0))
    d.edge(lb, gw, exit=(0.5,1), entry=(0.5,0))

    cont = d.node(120, 360, 1440, 170, "MICROSERVICIOS · HPA (escalan por CPU / RPS) · mínimo 2 réplicas en zonas distintas", container(CREAM, "fontSize=13;"))
    msx = ["MS Auth\n×N", "MS Rutinas\n×N", "MS Catálogo\n×N", "MS Pagos\n×N", "MS Notif.\n×N"]
    n=len(msx); sw=240; gap=30; x0=120+(1440-(sw*n+gap*(n-1)))//2
    for i,lab in enumerate(msx):
        d.node(x0+i*(sw+gap), 412, sw, 70, lab, box(GOLD))
    d.edge(gw, cont, exit=(0.5,1), entry=(0.5,0))

    redis  = d.node(130, 600, 380, 128, "Redis · Memorystore (cache-aside)\n• Catálogo — TTL 24 h\n• Rutina del día — TTL 1 h\n• Sesiones · rate limiting", box(GREEN, "align=left;spacingLeft=12;verticalAlign=middle;"))
    sqlp   = d.node(620, 600, 360, 64, "Cloud SQL — Primaria\nHA multi-zona · failover automático", db(GREEN))
    rr1    = d.node(630, 706, 165, 56, "Read replica", db(GREEN))
    rr2    = d.node(815, 706, 165, 56, "Read replica", db(GREEN))
    pubsub = d.node(1090, 600, 400, 128, "Pub/Sub — backbone de eventos\ntópicos + DLQ\nentrega at-least-once · reintentos", box(BLUE, "align=left;spacingLeft=12;verticalAlign=middle;"))
    d.edge(cont, redis,  "lecturas cacheadas", exit=(0.22,1), entry=(0.5,0))
    d.edge(cont, sqlp,   "escrituras",          exit=(0.5,1),  entry=(0.5,0))
    d.edge(cont, pubsub, "eventos",             exit=(0.78,1), entry=(0.5,0))
    d.edge(sqlp, rr1, "replica", exit=(0.4,1), entry=(0.5,0))
    d.edge(sqlp, rr2, "async",   exit=(0.6,1), entry=(0.5,0))
    d.node(615, 766, 380, 22, "Lecturas analíticas · dashboards · CQRS → réplicas", "text;html=1;align=center;fontSize=11;fontColor=#444444;")
    d.node(120, 812, 1440, 64, "<b>Tolerancia a fallos:</b> PodDisruptionBudgets · circuit breakers + reintentos con backoff exponencial · dead-letter queues · idempotencia (Pub/Sub at-least-once). Cluster Autoscaler agrega o quita nodos del cluster según la demanda agregada.", box(GREEN, "align=left;spacingLeft=12;verticalAlign=middle;"))
    save("fase3_arquitectura_escalada.drawio", d.xml())

# ===================================================== FASE 5
def fase5():
    d=Dio(); header(d, "Fase 5 — Integración con IA (Opción A: APIs de LLM) · flujo asíncrono")
    # --- fila superior: pedido -> encola -> worker -> LLM ---
    cli   = d.node(60, 232, 150, 66, "Cliente", box(BLUE))
    gw    = d.node(250, 232, 150, 66, "API Gateway", box(BLUE, "fontStyle=1;"))
    asist = d.node(440, 232, 215, 66, "MS Asistente IA\nresponde 202 + job_id", box(GOLD))
    jobs  = d.node(705, 232, 185, 66, "Pub/Sub · ia.jobs\n(cola de trabajos)", box(BLUE))
    work  = d.node(940, 232, 215, 66, "Workers IA · GKE\nHPA por profundidad de cola", box(GOLD))
    llm   = d.node(1210, 222, 270, 86, "API LLM externa\nAnthropic Claude / OpenAI\nfuera de la arquitectura", box(WHITE, "dashed=1;strokeWidth=2;fontStyle=2;"))
    d.edge(cli, gw,    "① pedido", exit=(1,0.5), entry=(0,0.5))
    d.edge(gw, asist,  "②",        exit=(1,0.5), entry=(0,0.5))
    d.edge(asist, jobs,"③ encola", exit=(1,0.5), entry=(0,0.5))
    d.edge(jobs, work, "④ consume",exit=(1,0.5), entry=(0,0.5))
    d.edge(work, llm,  "⑤ prompt + contexto", exit=(1,0.4), entry=(0,0.4))
    d.edge(llm, work,  "respuesta", extra="dashed=1;", exit=(0,0.7), entry=(1,0.7))
    # --- fila inferior: persiste -> publica terminado -> notifica -> push ---
    bd    = d.node(975, 430, 150, 56, "BD resultados", db(GREEN))
    done  = d.node(705, 424, 185, 66, "Pub/Sub · ia.job.terminado", box(BLUE))
    notif = d.node(440, 424, 215, 66, "MS Notificaciones", box(GOLD))
    d.edge(work, bd,    "⑥ persiste", exit=(0.5,1), entry=(0.5,0))
    d.edge(work, done,  "⑦ publica",  exit=(0.2,1), entry=(1,0.5))
    d.edge(done, notif, "consume",    exit=(0,0.5), entry=(1,0.5))
    d.edge(notif, cli,  "push / websocket", exit=(0,0.5), entry=(0.5,1))
    # --- polling de respaldo (cliente consulta estado) ---
    d.edge(cli, asist, "GET /ai/jobs/{id} · polling de respaldo", extra="dashed=1;strokeColor=#666666;fontColor=#666666;", exit=(0.5,1), entry=(0.5,1))
    # --- notas ---
    d.node(60, 560, 870, 70, "<b>Resiliencia:</b> timeout 60 s · reintentos con backoff + jitter (máx. 3) · circuit breaker con fallback a un 2º proveedor o degradación elegante · idempotencia por job_id · dead-letter queue.", box(GREEN, "align=left;spacingLeft=12;verticalAlign=middle;"))
    d.node(950, 560, 530, 70, "<b>Costos y datos:</b> presupuesto de tokens por tenant · caché de respuestas para prompts repetidos · anonimización de los datos del alumno antes de salir a la API externa.", box(CREAM, "align=left;spacingLeft=12;verticalAlign=middle;"))
    save("fase5_integracion_ia.drawio", d.xml())

# ===================================================== FASE 5 · OPCION B (RAG)
def fase5b():
    d=Dio(); header(d, "Fase 5 · Opción B — RAG (Retrieval-Augmented Generation)")
    d.node(70, 96, 360, 22, "INGESTA (offline · indexación)", "text;html=1;align=left;fontSize=13;fontStyle=1;fontColor=#666666;")
    d.node(70, 372, 360, 22, "CONSULTA (online · en cada pedido)", "text;html=1;align=left;fontSize=13;fontStyle=1;fontColor=#666666;")
    vector = d.node(720, 246, 280, 96, "Base vectorial\nPinecone / Milvus / Chroma", db(GREEN))
    # --- ingesta ---
    fu = d.node(70, 126, 250, 86, "Fuentes\ncatálogo · fichas técnicas\ndocumentos del entrenador", box(BLUE))
    ch = d.node(360, 140, 150, 60, "Chunking", box(GOLD))
    em = d.node(540, 140, 160, 60, "Embeddings", box(GOLD))
    d.edge(fu, ch, exit=(1,0.5), entry=(0,0.5))
    d.edge(ch, em, exit=(1,0.5), entry=(0,0.5))
    d.edge(em, vector, "indexa", exit=(1,0.5), entry=(0.3,0))
    # --- consulta ---
    q  = d.node(70, 404, 250, 72, "Consulta del entrenador\n(ej. rutina con lesión)", box(BLUE))
    qe = d.node(360, 408, 150, 62, "Embedding\nde la consulta", box(GOLD))
    rt = d.node(540, 408, 160, 62, "Retrieval\ntop-k por similitud", box(GOLD))
    pr = d.node(760, 408, 190, 62, "Prompt aumentado\n(consulta + contexto)", box(GOLDST, "fontStyle=1;"))
    llm= d.node(1010, 398, 250, 82, "API LLM\nAnthropic Claude / OpenAI\nfuera de la arquitectura", box(WHITE, "dashed=1;strokeWidth=2;fontStyle=2;"))
    rs = d.node(1300, 408, 220, 62, "Respuesta\n(borrador a revisar)", box(BLUE))
    d.edge(q, qe, exit=(1,0.5), entry=(0,0.5))
    d.edge(qe, rt, exit=(1,0.5), entry=(0,0.5))
    d.edge(vector, rt, "top-k chunks", extra="dashed=1;strokeColor=#666666;fontColor=#666666;", exit=(0.3,1), entry=(0.5,0))
    d.edge(rt, pr, exit=(1,0.5), entry=(0,0.5))
    d.edge(pr, llm, exit=(1,0.5), entry=(0,0.5))
    d.edge(llm, rs, exit=(1,0.5), entry=(0,0.5))
    d.node(70, 540, 1450, 78, "<b>Por qué hoy va la Opción A y no B.</b>  Los casos de uso operan sobre datos estructurados (historial, catálogo, membresías) que caben en el prompt; RAG se justifica cuando el catálogo crezca a miles de fichas extensas y documentos de los entrenadores. RAG reutiliza el MISMO backbone asíncrono (workers y colas de la Opción A): solo agrega el pipeline de ingesta y una etapa de retrieval previa al armado del prompt.", box(CREAM, "align=left;spacingLeft=12;verticalAlign=middle;"))
    save("fase5b_rag.drawio", d.xml())

if __name__=="__main__":
    fase1(); fase2a(); fase2b(); fase3(); fase5(); fase5b(); evolucion(); print("Listo.")
