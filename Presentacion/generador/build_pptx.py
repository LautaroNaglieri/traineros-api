# -*- coding: utf-8 -*-
"""
Generador de la Presentación Ejecutiva — TFI TrainerOS (Fases 1 y 2).
- Diapositivas de diagramas: imágenes PIL a pantalla completa (Presentacion/diagramas/*.png).
- Diapositivas de texto: formas nativas de PowerPoint (editables).
Sin XML manual frágil -> el archivo abre sin problemas en PowerPoint.
"""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

BASE = r"C:\Users\Conrado\Desktop\Programacion\UNSTA\app-development\Final\Presentacion"
DIAG = os.path.join(BASE, "diagramas")

C = {
    "navy":"0F172A","slate":"334155","gray":"64748B","lgray":"94A3B8","white":"FFFFFF",
    "bg":"F8FAFC","line":"E2E8F0","panel":"1E293B","panelB":"334155",
    "blue":"2563EB","blueL":"EFF6FF","blueB":"BFDBFE",
    "indigo":"4F46E5","indigoL":"EEF2FF","indigoB":"C7D2FE",
    "slateD":"475569","slateL":"F1F5F9","slateB":"CBD5E1",
    "green":"059669","greenL":"ECFDF5","greenB":"A7F3D0",
    "amber":"D97706","amberL":"FEF3C7","amberB":"FDE68A","amberT":"92400E",
    "violet":"7C3AED","violetL":"F5F3FF","violetB":"DDD6FE",
    "red":"DC2626","redL":"FEF2F2","redB":"FECACA",
    "cyan":"0891B2","cyanL":"ECFEFF","cyanB":"A5F3FC",
}
def rgb(h): return RGBColor.from_string(h)
SW, SH = 13.333, 7.5

prs = Presentation(); prs.slide_width=Inches(SW); prs.slide_height=Inches(SH)
def blank(): return prs.slides.add_slide(prs.slide_layouts[6])

def bg(slide,color):
    s=slide.shapes.add_shape(MSO_SHAPE.RECTANGLE,0,0,Inches(SW),Inches(SH))
    s.fill.solid(); s.fill.fore_color.rgb=rgb(color); s.line.fill.background(); s.shadow.inherit=False
    sp=s._element; sp.getparent().remove(sp); slide.shapes._spTree.insert(2,sp); return s

def rect(slide,x,y,w,h,fill=None,line=None,line_w=1.25,radius=0.09,shape=MSO_SHAPE.ROUNDED_RECTANGLE):
    s=slide.shapes.add_shape(shape,Inches(x),Inches(y),Inches(w),Inches(h))
    if fill is None: s.fill.background()
    else: s.fill.solid(); s.fill.fore_color.rgb=rgb(fill)
    if line is None: s.line.fill.background()
    else: s.line.color.rgb=rgb(line); s.line.width=Pt(line_w)
    s.shadow.inherit=False
    if shape==MSO_SHAPE.ROUNDED_RECTANGLE:
        try: s.adjustments[0]=radius
        except Exception: pass
    return s

def P(runs,**kw):
    d={"runs":runs}; d.update(kw); return d

def txt(slide,x,y,w,h,paras,align=PP_ALIGN.LEFT,anchor=MSO_ANCHOR.TOP,wrap=True):
    tb=slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h)); tf=tb.text_frame
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

def chip(slide,x,y,text_,fill,fg,size=11,w=None):
    cw=w if w else (0.22+0.085*len(text_))
    rect(slide,x,y,cw,0.33,fill=fill,line=None,radius=0.5)
    txt(slide,x,y,cw,0.33,[P([(text_,size,True,fg)],align=PP_ALIGN.CENTER)],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    return cw

def header(slide,tag,tagc,title,subtitle=None):
    rect(slide,0,0,0.16,SH,fill=tagc,line=None,radius=0,shape=MSO_SHAPE.RECTANGLE)
    chip(slide,0.55,0.42,tag,tagc,"FFFFFF",size=11)
    paras=[P([(title,26,True,C["navy"])],space_after=2)]
    if subtitle: paras.append(P([(subtitle,14,False,C["gray"])]))
    txt(slide,0.55,0.76,12.2,1.0,paras)

def footer(slide,num,speaker=None):
    rect(slide,0.55,7.04,12.23,0.012,fill=C["line"],line=None,radius=0,shape=MSO_SHAPE.RECTANGLE)
    txt(slide,0.55,7.10,8.0,0.3,[P([("TrainerOS — TFI Desarrollo de Aplicaciones Web",9.5,False,C["lgray"])])])
    right=(f"Expone: {speaker}    ·    {num}") if speaker else num
    txt(slide,8.0,7.10,4.78,0.3,[P([(right,9.5,True,C["gray"])],align=PP_ALIGN.RIGHT)],align=PP_ALIGN.RIGHT)

def image_slide(name):
    s=blank(); s.shapes.add_picture(os.path.join(DIAG,name),0,0,width=Inches(SW),height=Inches(SH)); return s

INTEG="Conrado Gómez · Nicolás Zyngale · Matías Saravia · Lautaro Naglieri · Pablo Czurylo · Leandro Gramajo"

# ---------------------------------------------------- 1. Portada
s=blank(); bg(s,C["navy"])
rect(s,0,0,SW,0.18,fill=C["blue"],line=None,radius=0,shape=MSO_SHAPE.RECTANGLE)
rect(s,0,SH-0.18,SW,0.18,fill=C["green"],line=None,radius=0,shape=MSO_SHAPE.RECTANGLE)
txt(s,0.9,1.1,11.5,0.5,[P([("TRABAJO FINAL INTEGRADOR  ·  DESARROLLO DE APLICACIONES WEB",13,True,C["blueB"])])])
txt(s,0.9,1.65,11.5,1.3,[P([("TrainerOS",58,True,C["white"])])])
txt(s,0.9,2.9,11.5,0.6,[P([("Plataforma SaaS de gestión para entrenadores personales",21,False,C["blueB"])])])
txt(s,0.9,3.62,11.6,0.5,[P([("“Del Código a la Arquitectura: El Criterio del Desarrollador”",15,False,C["lgray"])])])
rect(s,0.9,4.5,11.55,1.15,fill="1E293B",line="334155",line_w=1.0,radius=0.06)
txt(s,1.2,4.68,11.0,0.9,[
    P([("Defensa de arquitectura — Fases 1 y 2",15,True,C["white"])],space_after=4),
    P([("Fase 1: Monolito modular en 3 capas   ",12.5,False,C["blueB"]),
       ("→   ",12.5,True,C["green"]),
       ("Fase 2: Microservicios tradicionales y modernos (event-driven)",12.5,False,C["blueB"])]),
])
txt(s,0.9,6.0,11.55,0.7,[
    P([("Equipo MMP-SOFTWARE",11.5,True,C["lgray"])],space_after=2),
    P([(INTEG,11,False,C["gray"])]),
])

# ---------------------------------------------------- 2. Problema y negocio
s=blank(); bg(s,C["bg"])
header(s,"CONTEXTO",C["slateD"],"El problema y el modelo de negocio","Por qué existe TrainerOS y cómo gana dinero")
rect(s,0.55,1.85,5.95,2.55,fill=C["white"],line=C["redB"],line_w=1.25,radius=0.05)
rect(s,0.7,2.0,0.08,2.25,fill=C["red"],line=None,radius=0.5)
txt(s,0.95,2.05,5.4,2.3,[
    P([("EL PROBLEMA",12,True,C["red"])],space_after=6),
    P([("Los entrenadores gestionan decenas de alumnos con ",13,False,C["slate"]),
       ("planillas de Excel y mensajes de WhatsApp",13,True,C["navy"]),(".",13,False,C["slate"])],space_after=6,line=1.15),
    P([("Resultado: caos logístico, rutinas desactualizadas y pérdida de control sobre los cobros de membresías.",13,False,C["slate"])],line=1.15),
])
rect(s,6.85,1.85,5.93,2.55,fill=C["white"],line=C["greenB"],line_w=1.25,radius=0.05)
rect(s,7.0,2.0,0.08,2.25,fill=C["green"],line=None,radius=0.5)
txt(s,7.25,2.05,5.4,2.3,[
    P([("MODELO DE NEGOCIO — SaaS B2B2C",12,True,C["green"])],space_after=6),
    P([("Suscripción mensual por entrenador",13,True,C["navy"]),
       (" (multitenant). El entrenador paga la herramienta; sus alumnos acceden gratis a un panel móvil.",13,False,C["slate"])],space_after=6,line=1.15),
    P([("Cada entrenador es un ",13,False,C["slate"]),("tenant aislado",13,True,C["navy"]),
       (": sus datos nunca se cruzan con los de otro.",13,False,C["slate"])],line=1.15),
])
txt(s,0.55,4.66,8,0.35,[P([("Funcionalidades del MVP",14,True,C["navy"])])])
mvp=[("Auth con Google","Identidad y acceso",C["blue"],C["blueL"],C["blueB"]),
     ("Constructor de rutinas","Desde catálogo de ejercicios",C["indigo"],C["indigoL"],C["indigoB"]),
     ("Panel móvil del alumno","Rutina del día y progreso",C["green"],C["greenL"],C["greenB"]),
     ("Control de pagos","Membresías y alertas de venc.",C["amber"],C["amberL"],C["amberB"])]
bx=0.55; bw=2.96; gap=0.10
for i,(t,d,col,bgc,bb) in enumerate(mvp):
    x=bx+i*(bw+gap)
    rect(s,x,5.12,bw,1.45,fill=bgc,line=bb,line_w=1.25,radius=0.07)
    rect(s,x+0.18,5.28,bw-0.36,0.06,fill=col,line=None,radius=0.5)
    txt(s,x+0.2,5.46,bw-0.4,1.0,[
        P([(t,12.5,True,C["navy"])],space_after=4,line=1.05),
        P([(d,10.5,False,C["gray"])],line=1.1),
    ])
footer(s,"2 / 12","Conrado Gómez")

# ---------------------------------------------------- 3. Fase 1 diagrama (imagen)
image_slide("fase1_monolito_3capas.png")

# ---------------------------------------------------- 4. Fase 1 justificación
s=blank(); bg(s,C["bg"])
header(s,"FASE 1 · JUSTIFICACIÓN",C["blue"],"¿Por qué alcanza para arrancar? ¿Cuáles son sus límites?",
       "El monolito como decisión deliberada, no como pecado")
rect(s,0.55,1.85,6.0,4.55,fill=C["white"],line=C["greenB"],line_w=1.25,radius=0.04)
rect(s,0.8,2.03,5.5,0.06,fill=C["green"],line=None,radius=0.5)
txt(s,0.85,2.2,5.4,0.4,[P([("SUFICIENTE PARA ARRANCAR",14,True,C["green"])])])
just=[("Costo y time-to-market mínimos","Un solo despliegue, una base y un pipeline. Costo fijo USD 7–16/mes; se itera en sprints semanales."),
      ("Un solo lenguaje de punta a punta","Node.js comparte ecosistema con el frontend (TypeScript full-stack): menos fricción, más velocidad."),
      ("Ideal para carga I/O-bound","El sistema es 95% lecturas/escrituras, sin cómputo pesado: Express + Prisma rinde de sobra."),
      ("Modularidad intencional","Los módulos ya tienen límites claros: son los futuros microservicios. Abarata la Fase 2.")]
yy=2.72
for t,d in just:
    txt(s,0.95,yy,5.35,0.85,[
        P([("●  ",11,True,C["green"]),(t,12,True,C["navy"])],space_after=2,line=1.05),
        P([("      "+d,10.8,False,C["slate"])],line=1.12)])
    yy+=0.9
rect(s,6.8,1.85,5.98,4.55,fill=C["white"],line=C["redB"],line_w=1.25,radius=0.04)
rect(s,7.05,2.03,5.48,0.06,fill=C["red"],line=None,radius=0.5)
txt(s,7.1,2.2,5.4,0.4,[P([("SUS LÍMITES  (disparan la Fase 2)",14,True,C["red"])])])
lims=[("Solo escala vertical","Un pico en Rutinas obliga a escalar TODO el monolito."),
      ("Acoplamiento de despliegue","Un deploy defectuoso de cualquier módulo tumba el sistema completo."),
      ("Base única = riesgo concentrado","Una query pesada de reportes degrada las operaciones transaccionales."),
      ("Cuello de botella de equipos","Varios equipos generan merge conflicts y releases que coordinar."),
      ("Sin alta disponibilidad","Render/Railway no ofrecen autoscaling granular ni SLAs.")]
yy=2.72
for t,d in lims:
    txt(s,7.2,yy,5.3,0.7,[
        P([("●  ",11,True,C["red"]),(t,12,True,C["navy"])],space_after=1,line=1.05),
        P([("      "+d,10.8,False,C["slate"])],line=1.1)])
    yy+=0.72
footer(s,"4 / 12","Nicolás Zyngale")

# ---------------------------------------------------- 5. Fase 2 contexto
s=blank(); bg(s,C["bg"])
header(s,"FASE 2 · CAMBIO DE CONTEXTO",C["indigo"],"El negocio fuerza la evolución a microservicios",
       "12 meses después: convenios B2B con dos cadenas regionales de gimnasios")
rect(s,0.55,1.85,12.23,0.95,fill=C["navy"],line=None,radius=0.05)
txt(s,0.85,1.85,5.3,0.95,[
    P([("De",13,False,C["lgray"]),("   100 entrenadores",17,True,C["white"])],space_after=1),
    P([("monolito · ~5.000 alumnos",11,False,C["lgray"])])],anchor=MSO_ANCHOR.MIDDLE)
txt(s,5.9,1.85,1.2,0.95,[P([("→",26,True,C["green"])],align=PP_ALIGN.CENTER)],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
txt(s,7.1,1.85,5.5,0.95,[
    P([("A",13,False,C["lgray"]),("   5.000 entrenadores",17,True,C["green"])],space_after=1),
    P([("~120.000 alumnos activos · equipos independientes",11,False,C["lgray"])])],anchor=MSO_ANCHOR.MIDDLE)
txt(s,0.55,3.0,8,0.35,[P([("Tres presiones que el monolito no resuelve",14.5,True,C["navy"])])])
press=[("Picos de tráfico violentos","De 18 a 21 h los alumnos consultan su rutina desde el gimnasio (lecturas masivas) mientras los entrenadores planifican. Los lunes el pico se triplica.",C["blue"],C["blueL"],C["blueB"]),
       ("Equipos independientes","La empresa crece a tres equipos (Core de rutinas, Pagos/B2B, Experiencia del alumno) que necesitan desplegar sin coordinarse.",C["indigo"],C["indigoL"],C["indigoB"]),
       ("Requisitos B2B","Las cadenas exigen SLA de disponibilidad, facturación consolidada y notificaciones masivas que no pueden competir por recursos con el flujo crítico.",C["violet"],C["violetL"],C["violetB"])]
px0=0.55; pw=3.97; pg=0.16
for i,(t,d,col,bgc,bb) in enumerate(press):
    x=px0+i*(pw+pg)
    rect(s,x,3.5,pw,2.85,fill=C["white"],line=bb,line_w=1.25,radius=0.05)
    rect(s,x+0.25,3.7,pw-0.5,0.06,fill=col,line=None,radius=0.5)
    rect(s,x+0.3,3.92,0.55,0.55,fill=bgc,line=None,radius=0.2)
    txt(s,x+0.3,3.92,0.55,0.55,[P([(str(i+1),20,True,col)],align=PP_ALIGN.CENTER)],align=PP_ALIGN.CENTER,anchor=MSO_ANCHOR.MIDDLE)
    txt(s,x+0.3,4.62,pw-0.6,1.6,[
        P([(t,14,True,C["navy"])],space_after=5,line=1.05),
        P([(d,11,False,C["slate"])],line=1.2)])
footer(s,"5 / 12","Matías Saravia")

# ---------------------------------------------------- 6. Fase 2A (imagen)
image_slide("fase2a_microservicios_tradicionales.png")
# ---------------------------------------------------- 7. Fase 2B (imagen)
image_slide("fase2b_microservicios_modernos.png")

# ---------------------------------------------------- 8. Patrones (tabla)
s=blank(); bg(s,C["bg"])
header(s,"FASE 2 · PATRONES",C["green"],"Patrones aplicados y su justificación",
       "Cada patrón responde a un problema concreto del negocio — no se usa “porque sí”")
pat=[("API Gateway","Punto único de entrada (Kong / Cloud Endpoints)","Centraliza JWT, rate limiting y versionado; los clientes no conocen la topología interna.",C["amber"]),
     ("Database per Service","Cada microservicio con su propia base","Autonomía de esquema y de despliegue; evita el acoplamiento por datos.",C["slateD"]),
     ("Pub/Sub (eventos)","Rutinas y Pagos publican; Notif./Analytics/Query suscriben","Desacopla en el tiempo: una caída no se propaga; los eventos se reintentan.",C["violet"]),
     ("CQRS","Escritura (Rutinas) vs. lectura (Query, vista materializada)","Carga asimétrica: miles leen, pocos escriben. Se optimiza cada lado por separado.",C["green"]),
     ("Saga (orquestada)","Cobro: pago → confirmación → membresía → notificación","Sin transacciones distribuidas: consistencia eventual con compensaciones (rollback).",C["blue"]),
     ("Circuit Breaker","Llamadas síncronas residuales (pasarela de pago externa)","Evita el efecto dominó: ante fallos abre el circuito y responde con fallback.",C["red"])]
ty=1.95; rowh=0.74
rect(s,0.55,ty,12.23,0.42,fill=C["navy"],line=None,radius=0.04)
for x,w,t in [(0.75,2.7,"PATRÓN"),(3.55,4.2,"DÓNDE SE APLICA"),(7.9,4.75,"POR QUÉ")]:
    txt(s,x,ty,w,0.42,[P([(t,10.5,True,C["white"])])],anchor=MSO_ANCHOR.MIDDLE)
yy=ty+0.42
for i,(name,where,why,col) in enumerate(pat):
    fillc=C["white"] if i%2==0 else C["slateL"]
    rect(s,0.55,yy,12.23,rowh,fill=fillc,line=C["line"],line_w=0.75,radius=0.0,shape=MSO_SHAPE.RECTANGLE)
    rect(s,0.55,yy,0.07,rowh,fill=col,line=None,radius=0,shape=MSO_SHAPE.RECTANGLE)
    txt(s,0.78,yy,2.7,rowh,[P([(name,12,True,col)])],anchor=MSO_ANCHOR.MIDDLE)
    txt(s,3.55,yy,4.2,rowh,[P([(where,10.3,False,C["slate"])],line=1.1)],anchor=MSO_ANCHOR.MIDDLE)
    txt(s,7.9,yy,4.75,rowh,[P([(why,10.3,False,C["slate"])],line=1.1)],anchor=MSO_ANCHOR.MIDDLE)
    yy+=rowh
footer(s,"8 / 12","Lautaro Naglieri")

# ---------------------------------------------------- 9. Panorama (imagen)
image_slide("evolucion_3_arquitecturas.png")

out=os.path.join(BASE,"TrainerOS_TFI_Fase1-2.pptx")
prs.save(out)
print("OK ->",out,"| slides:",len(prs.slides._sldIdLst))
