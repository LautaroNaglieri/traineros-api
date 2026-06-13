# -*- coding: utf-8 -*-
"""
Presentación ejecutiva TFI TrainerOS (Fases 1 y 2).
Estilo corporativo tipo "Naturgy en un Scan": azul #1F4E79 + naranja #E8741E + gris,
portada azul, títulos azules, tarjetas, acentos naranjas y barra naranja al pie.
Diagramas: imágenes draw.io ajustadas (sin distorsión).
"""
import os
from PIL import Image
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BASE = r"C:\Users\Conrado\Desktop\Programacion\UNSTA\app-development\Final\Presentacion"
DIAG = os.path.join(BASE, "diagramas")

NAVY="1F4E79"; NAVY2="2A5E8C"; ORANGE="E8741E"; ORANGE2="C75F12"
CARD="ECF0F3"; CARD2="E1E8EE"; INK="404040"; GRAY="7A7A7A"; LGRAY="9AA6B2"; WHITE="FFFFFF"
def rgb(h): return RGBColor.from_string(h)
SW, SH = 13.333, 7.5

prs = Presentation(); prs.slide_width=Inches(SW); prs.slide_height=Inches(SH)
def blank(): return prs.slides.add_slide(prs.slide_layouts[6])

def rect(s,x,y,w,h,fill=None,line=None,line_w=1.0,radius=0.06,shape=MSO_SHAPE.RECTANGLE):
    sh=s.shapes.add_shape(shape,Inches(x),Inches(y),Inches(w),Inches(h))
    if fill is None: sh.fill.background()
    else: sh.fill.solid(); sh.fill.fore_color.rgb=rgb(fill)
    if line is None: sh.line.fill.background()
    else: sh.line.color.rgb=rgb(line); sh.line.width=Pt(line_w)
    sh.shadow.inherit=False
    if shape==MSO_SHAPE.ROUNDED_RECTANGLE:
        try: sh.adjustments[0]=radius
        except Exception: pass
    return sh

def P(runs,**kw): d={"runs":runs}; d.update(kw); return d
def txt(s,x,y,w,h,paras,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,wrap=True):
    tb=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=tb.text_frame
    tf.word_wrap=wrap; tf.vertical_anchor=anchor
    tf.margin_left=0; tf.margin_right=0; tf.margin_top=0; tf.margin_bottom=0
    for i,p in enumerate(paras):
        para=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        para.alignment=p.get("align",align)
        if "space_after" in p: para.space_after=Pt(p["space_after"])
        if "space_before" in p: para.space_before=Pt(p["space_before"])
        if "line" in p: para.line_spacing=p["line"]
        for (t,size,bold,color) in p["runs"]:
            r=para.add_run(); r.text=t; r.font.size=Pt(size); r.font.bold=bold
            r.font.color.rgb=rgb(color); r.font.name="Segoe UI"
    return tb

def bottom_bar(s): rect(s,0,SH-0.13,SW,0.13,fill=ORANGE)
def page(s,num,speaker=None):
    t=(f"{num}   ·   Expone: {speaker}") if speaker else num
    txt(s,8.0,SH-0.46,4.78,0.28,[P([(t,9.5,False,LGRAY)],align=PP_ALIGN.RIGHT)],align=PP_ALIGN.RIGHT)

def head(s,title,subtitle=None):
    txt(s,0.7,0.55,12.0,0.7,[P([(title,30,True,NAVY)])])
    if subtitle:
        txt(s,0.72,1.28,12.0,0.4,[P([(subtitle,14.5,False,GRAY)])])

def fit_image(s,path,ax,ay,aw,ah):
    iw,ih=Image.open(path).size; ar=iw/ih; box=aw/ah
    if ar>box: w=aw; h=aw/ar
    else: h=ah; w=ah*ar
    s.shapes.add_picture(path,Inches(ax+(aw-w)/2),Inches(ay+(ah-h)/2),Inches(w),Inches(h))

def diagram_slide(name, speaker=None):
    s=blank()
    fit_image(s,os.path.join(DIAG,name),0.25,0.22,12.83,6.9)
    bottom_bar(s); page(s,"",speaker)
    return s

INTEG="Conrado Gómez   ·   Nicolás Zyngale   ·   Matías Saravia   ·   Lautaro Naglieri   ·   Pablo Czurylo   ·   Leandro Gramajo"

# ---------------------------------------------------- 1. Portada
s=blank(); rect(s,0,0,SW,SH,fill=NAVY)
txt(s,0.8,2.45,11.73,1.0,[P([("TrainerOS",56,True,WHITE)],align=PP_ALIGN.CENTER)],align=PP_ALIGN.CENTER)
txt(s,0.8,3.62,11.73,0.55,[P([("“Del Código a la Arquitectura: El Criterio del Desarrollador”",22,True,ORANGE)],align=PP_ALIGN.CENTER)],align=PP_ALIGN.CENTER)
txt(s,0.8,4.28,11.73,0.45,[P([("Plataforma SaaS de gestión para entrenadores personales",15,False,"D6E0EA")],align=PP_ALIGN.CENTER)],align=PP_ALIGN.CENTER)
rect(s,0,4.95,SW,0.045,fill=ORANGE)
txt(s,0.8,5.55,11.73,0.4,[P([("Fase 1: Monolito modular en 3 capas      →      Fase 2: Microservicios tradicionales y modernos (event-driven)",13,False,"AEBFCE")],align=PP_ALIGN.CENTER)],align=PP_ALIGN.CENTER)
txt(s,0.8,6.45,11.73,0.6,[
    P([("TFI · Desarrollo de Aplicaciones Web · Equipo MMP-SOFTWARE",12.5,True,WHITE)],align=PP_ALIGN.CENTER,space_after=4),
    P([(INTEG,10.5,False,"AEBFCE")],align=PP_ALIGN.CENTER),
])

# ---------------------------------------------------- 2. Problema y negocio
s=blank()
head(s,"El problema y el modelo de negocio","Por qué existe TrainerOS y cómo gana dinero")
# tarjetas grandes
rect(s,0.7,1.95,5.95,2.4,fill=CARD)
txt(s,1.0,2.2,5.4,2.0,[
    P([("EL PROBLEMA",13,True,NAVY)],space_after=8),
    P([("Los entrenadores gestionan decenas de alumnos con ",13.5,False,INK),
       ("planillas de Excel y mensajes de WhatsApp",13.5,True,ORANGE),(".",13.5,False,INK)],space_after=7,line=1.18),
    P([("Caos logístico, rutinas desactualizadas y pérdida de control sobre los cobros de membresías.",13.5,False,INK)],line=1.18),
])
rect(s,6.85,1.95,5.78,2.4,fill=CARD)
txt(s,7.15,2.2,5.25,2.0,[
    P([("MODELO DE NEGOCIO — SaaS B2B2C",13,True,NAVY)],space_after=8),
    P([("Suscripción mensual por entrenador",13.5,True,ORANGE),
       (" (multitenant). El entrenador paga; sus alumnos usan gratis un panel móvil.",13.5,False,INK)],space_after=7,line=1.18),
    P([("Cada entrenador es un tenant aislado: sus datos nunca se cruzan con los de otro.",13.5,False,INK)],line=1.18),
])
# MVP
txt(s,0.7,4.62,8,0.35,[P([("Funcionalidades del MVP",15,True,NAVY)])])
mvp=[("Auth con Google","Identidad y acceso"),("Constructor de rutinas","Sobre catálogo de ejercicios"),
     ("Panel móvil del alumno","Rutina del día y progreso"),("Control de pagos","Membresías y alertas")]
bx=0.7; bw=2.96; gap=0.097
for i,(t,d) in enumerate(mvp):
    x=bx+i*(bw+gap)
    rect(s,x,5.1,bw,1.35,fill=CARD)
    rect(s,x,5.1,0.07,1.35,fill=ORANGE)
    txt(s,x+0.24,5.34,bw-0.42,0.95,[
        P([(t,12.5,True,NAVY)],space_after=4,line=1.05),
        P([(d,10.5,False,GRAY)],line=1.1)])
bottom_bar(s); page(s,"2 / 12","Conrado Gómez")

# ---------------------------------------------------- 3. Fase 1 diagrama
diagram_slide("fase1_monolito_3capas.png","Nicolás Zyngale")

# ---------------------------------------------------- 4. Justificación
s=blank()
head(s,"¿Por qué alcanza para arrancar? ¿Cuáles son sus límites?","El monolito como decisión deliberada, no como pecado")
rect(s,0.7,1.95,5.9,4.55,fill=CARD)
rect(s,0.7,1.95,5.9,0.09,fill=NAVY)
txt(s,1.0,2.2,5.35,0.4,[P([("POR QUÉ ALCANZA PARA ARRANCAR",13.5,True,NAVY)])])
just=[("Costo y time-to-market mínimos","Un deploy, una base y un pipeline. USD 7–16/mes; sprints semanales."),
      ("Un solo lenguaje de punta a punta","Node.js comparte ecosistema con el frontend (TypeScript full-stack)."),
      ("Ideal para carga I/O-bound","95% lecturas/escrituras, sin cómputo pesado: Express + Prisma rinde."),
      ("Modularidad intencional","Los módulos ya son los futuros microservicios. Abarata la Fase 2.")]
yy=2.78
for t,d in just:
    txt(s,1.0,yy,5.3,0.9,[
        P([("■  ",10.5,True,NAVY),(t,12,True,INK)],space_after=2,line=1.05),
        P([("      "+d,10.8,False,GRAY)],line=1.12)]); yy+=0.92
rect(s,6.75,1.95,5.88,4.55,fill=CARD)
rect(s,6.75,1.95,5.88,0.09,fill=ORANGE)
txt(s,7.05,2.2,5.35,0.4,[P([("SUS LÍMITES  (disparan la Fase 2)",13.5,True,ORANGE2)])])
lims=[("Solo escala vertical","Un pico en Rutinas obliga a escalar todo el monolito."),
      ("Acoplamiento de despliegue","Un deploy defectuoso de un módulo tumba todo el sistema."),
      ("Base única = riesgo concentrado","Una query pesada de reportes degrada lo transaccional."),
      ("Cuello de botella de equipos","Varios equipos: merge conflicts y releases que coordinar."),
      ("Sin alta disponibilidad","Render/Railway no dan autoscaling granular ni SLAs.")]
yy=2.78
for t,d in lims:
    txt(s,7.05,yy,5.3,0.72,[
        P([("■  ",10.5,True,ORANGE),(t,12,True,INK)],space_after=1,line=1.05),
        P([("      "+d,10.8,False,GRAY)],line=1.1)]); yy+=0.735
bottom_bar(s); page(s,"4 / 12","Nicolás Zyngale")

# ---------------------------------------------------- 5. Contexto
s=blank()
head(s,"El negocio fuerza la evolución a microservicios","12 meses después: convenios B2B con dos cadenas regionales de gimnasios")
rect(s,0.7,1.9,11.93,0.95,fill=NAVY)
txt(s,1.0,1.9,5.0,0.95,[
    P([("De ",13,False,"AEBFCE"),("100 entrenadores",18,True,WHITE)],space_after=1),
    P([("monolito · ~5.000 alumnos",11,False,"AEBFCE")])],anchor=MSO_ANCHOR.MIDDLE)
txt(s,6.0,1.9,1.0,0.95,[P([("→",26,True,ORANGE)],align=PP_ALIGN.CENTER)],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
txt(s,7.0,1.9,5.4,0.95,[
    P([("A ",13,False,"AEBFCE"),("5.000 entrenadores",18,True,ORANGE)],space_after=1),
    P([("~120.000 alumnos activos · equipos independientes",11,False,"AEBFCE")])],anchor=MSO_ANCHOR.MIDDLE)
txt(s,0.7,3.1,8,0.35,[P([("Tres presiones que el monolito no resuelve",15,True,NAVY)])])
press=[("Picos de tráfico violentos","De 18 a 21 h los alumnos consultan su rutina desde el gimnasio (lecturas masivas). Los lunes el pico se triplica."),
       ("Equipos independientes","Tres equipos (Core de rutinas, Pagos/B2B, Experiencia del alumno) que necesitan desplegar sin coordinarse."),
       ("Requisitos B2B","Las cadenas exigen SLA, facturación consolidada y notificaciones masivas que no pueden competir con el flujo crítico.")]
px0=0.7; pw=3.94; pg=0.155
for i,(t,d) in enumerate(press):
    x=px0+i*(pw+pg)
    rect(s,x,3.6,pw,2.7,fill=CARD)
    rect(s,x+0.28,3.85,0.6,0.6,fill=ORANGE)
    txt(s,x+0.28,3.85,0.6,0.6,[P([(str(i+1),20,True,WHITE)],align=PP_ALIGN.CENTER)],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    txt(s,x+0.28,4.62,pw-0.56,1.55,[
        P([(t,14,True,NAVY)],space_after=5,line=1.05),
        P([(d,11,False,INK)],line=1.2)])
bottom_bar(s); page(s,"5 / 12","Matías Saravia")

# ---------------------------------------------------- 6,7 diagramas
diagram_slide("fase2a_microservicios_tradicionales.png","Matías Saravia")
diagram_slide("fase2b_microservicios_modernos.png","Lautaro Naglieri")

# ---------------------------------------------------- 8. Patrones (tabla)
s=blank()
head(s,"Patrones aplicados y su justificación","Cada patrón responde a un problema concreto del negocio — no se usa “porque sí”")
pat=[("API Gateway","Punto único de entrada (Kong / Cloud Endpoints)","Centraliza JWT, rate limiting y versionado; oculta la topología interna."),
     ("Database per Service","Cada microservicio con su propia base","Autonomía de esquema y de despliegue; evita el acoplamiento por datos."),
     ("Pub/Sub (eventos)","Rutinas y Pagos publican; Notif./Analytics/Query suscriben","Desacopla en el tiempo: una caída no se propaga; los eventos se reintentan."),
     ("CQRS","Escritura (Rutinas) vs. lectura (Query, vista materializada)","Carga asimétrica: miles leen, pocos escriben. Se optimiza cada lado."),
     ("Saga (orquestada)","Cobro: pago → confirmación → membresía → notificación","Consistencia eventual con compensaciones (rollback), sin trans. distribuidas."),
     ("Circuit Breaker","Llamadas síncronas residuales (pasarela de pago externa)","Evita el efecto dominó: ante fallos abre el circuito y responde fallback.")]
ty=1.95; rowh=0.72
rect(s,0.7,ty,11.93,0.44,fill=NAVY)
for x,w,t in [(0.92,2.7,"PATRÓN"),(3.7,4.0,"DÓNDE SE APLICA"),(7.85,4.6,"POR QUÉ")]:
    txt(s,x,ty,w,0.44,[P([(t,10.5,True,WHITE)])],anchor=MSO_ANCHOR.MIDDLE)
yy=ty+0.44
for i,(name,where,why) in enumerate(pat):
    rect(s,0.7,yy,11.93,rowh,fill=(WHITE if i%2==0 else CARD))
    rect(s,0.7,yy,0.06,rowh,fill=ORANGE)
    txt(s,0.92,yy,2.75,rowh,[P([(name,12,True,NAVY)])],anchor=MSO_ANCHOR.MIDDLE)
    txt(s,3.7,yy,4.05,rowh,[P([(where,10.3,False,INK)],line=1.1)],anchor=MSO_ANCHOR.MIDDLE)
    txt(s,7.85,yy,4.6,rowh,[P([(why,10.3,False,INK)],line=1.1)],anchor=MSO_ANCHOR.MIDDLE)
    yy+=rowh
bottom_bar(s); page(s,"8 / 12","Lautaro Naglieri")

# ---------------------------------------------------- 9. diagrama evolución
diagram_slide("evolucion_3_arquitecturas.png")

out=os.path.join(BASE,"TrainerOS_TFI_Fase1-2.pptx")
prs.save(out)
print("OK ->",out,"| slides:",len(prs.slides._sldIdLst))
