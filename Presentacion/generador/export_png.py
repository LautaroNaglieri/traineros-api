# -*- coding: utf-8 -*-
"""Exporta cada slide del pptx a PNG usando PowerPoint (COM).
Abre desde C:\\Temp porque PowerPoint COM no abre rutas del Desktop sincronizado.
"""
import os, shutil, time
import comtypes.client

base = r"C:\Users\Conrado\Desktop\Programacion\UNSTA\app-development\Final\Presentacion"
src  = os.path.join(base, "TrainerOS_TFI_Fase1-2.pptx")
tmp  = r"C:\Temp\trainer_deck.pptx"
os.makedirs(r"C:\Temp", exist_ok=True)
shutil.copy(src, tmp)

review = os.path.join(base, "generador", "_review")
os.makedirs(review, exist_ok=True)
for f in os.listdir(review):
    try: os.remove(os.path.join(review,f))
    except: pass

pp = comtypes.client.CreateObject("PowerPoint.Application")
pp.Visible = 1
time.sleep(1)
deck = pp.Presentations.Open(tmp, ReadOnly=True, WithWindow=False)
n = deck.Slides.Count
for i in range(1, n+1):
    deck.Slides(i).Export(os.path.join(review, f"slide_{i:02d}.png"), "PNG", 1920, 1080)
deck.Close()
pp.Quit()
print("Exportadas", n, "slides a _review/")
