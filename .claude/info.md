# Bitácora del TFI — TrainerOS (Desarrollo de Aplicaciones Web)

Registro de todo lo que se va haciendo, con fecha y hora, para tener siempre el
contexto completo del proyecto. Lo más nuevo arriba.

Equipo (6): Conrado Gómez · Nicolás Zyngale · Matías Saravia · Lautaro Naglieri ·
Pablo Czurylo · Leandro Gramajo · Empresa ficticia: **MMP-SOFTWARE**.

Fecha límite de entrega: **19/06/2026**. Mail del profe: dl.sotol@gmail.com.
Repo del código: https://github.com/LautaroNaglieri/traineros-api

---

## 2026-06-13 ~01:00 — Sesión 1: organización + pptx Fases 1 y 2 + esqueletos

### Qué se hizo
1. **Estructura de carpetas** del proyecto, organizada:
   ```
   Final/
   ├─ .claude/info.md          (esta bitácora)
   ├─ Material/                (docs fuente + RESUMEN.md)
   ├─ Presentacion/            (pptx + diagramas + generador)
   ├─ Codigo/                  (esqueletos Fase 1 y Fase 2)
   ├─ Articulo/                (vacío — artículo Medium, pendiente)
   └─ Informe/                 (vacío — informe PDF, pendiente)
   ```
2. **Material/**: se copiaron los 3 archivos fuente (TFI_TrainerOS.docx, consigna,
   transcripción del audio) + se escribió `RESUMEN.md` con la consigna y los puntos
   clave del audio resumidos.
3. **Presentación ejecutiva (Fases 1 y 2)** — `Presentacion/TrainerOS_TFI_Fase1-2.pptx`,
   9 diapositivas, generada con python-pptx (verificada slide por slide exportando a PNG
   con PowerPoint). Diseño profesional, en español, sin código (regla del profe).
4. **Diagramas** en `Presentacion/diagramas/` (PNG alta resolución, hechos con PIL):
   - `fase1_monolito_3capas.png`
   - `fase2a_microservicios_tradicionales.png`
   - `fase2b_microservicios_modernos.png`
   - `evolucion_3_arquitecturas.png`  ← **la imagen de las 3 arquitecturas juntas**
5. **Código (esqueletos / diseño)** en `Codigo/`:
   - `traineros-api/` → **monolito modular EN CAPAS** (3-tier). Corrige el repo actual,
     que estaba como monolito modular por features (no en capas). Boilerplate sin lógica
     de negocio: Express+TS, Prisma+schema base+migración, middleware JWT vacío, tenant,
     ESLint/Prettier, healthcheck, Docker. Capas: presentation/ application/ domain/
     infrastructure/ shared/.
   - `fase2-microservicios/` → monorepo (gateway + 5 servicios + shared-contracts/events
     + docker-compose con emulador Pub/Sub). Esqueleto event-driven.

### Decisiones / notas técnicas
- El `.pptx` lleva los diagramas como **imágenes** (no formas nativas) porque el XML
  manual de formas/flechas que probé generaba un archivo que PowerPoint no abría. Las
  imágenes PIL son confiables y se ven mejor. Las slides de texto sí son formas nativas
  editables. El generador está en `Presentacion/generador/` (build_diagrams.py + build_pptx.py).
- Para regenerar/verificar el pptx: `export_png.py` usa PowerPoint vía COM, pero **debe
  abrir desde C:\Temp** (PowerPoint no abre rutas del Desktop sincronizado con OneDrive).
- Cuando se use el navegador (Claude-in-Chrome) usar **Brave**, no Chrome.

### Diagnóstico del repo GitHub (revisado con Brave el 13/06)
Repo `LautaroNaglieri/traineros-api`, rama `main`. Estado real:
- **Estructura actual** (`src/`): `config/`, `middlewares/`, `modules/{auth,rutinas,catalogo,pagos}/`,
  `routes/`, `app.ts`, `server.ts`. → Es **monolito modular POR FEATURES**, NO en capas.
  Las 3 capas no están separadas (no hay presentation/application/domain/infrastructure).
  **Esto es lo que hay que corregir** con el esqueleto de `Codigo/traineros-api/`.
- El README **dice** "monolito modular en 3 capas" pero la estructura no lo refleja → incoherencia.
- README dice **"8 integrantes"** → somos **6**. Corregir.
- Solo cubre Fase 1 (no hay nada de Fase 2).
- Lo bueno: ya tiene **commits de esqueleto limpios y en español** que sirven de modelo:
  `chore: configuración inicial de express y typescript`, `chore: configuración de prisma y
  esquema base`, `chore: configuración de eslint, prettier y husky`, `feat: endpoint de
  healthcheck`. Mantener ese estilo de mensajes al reemplazar.

### Plan de reemplazo del repo (para la sesión de push)
1. Inicializar git en `Final/` (hoy NO es repo) o clonar el remoto y reemplazar contenido.
2. Subir la estructura organizada (Material, Presentacion, Codigo, .claude, etc.).
3. Reescribir `Codigo/traineros-api/` como **monolito en capas** (ya hecho localmente).
4. Commits en **español, sin mención a IA, sin emojis**. Reusar el estilo de commits que ya existe.
5. Corregir "8 integrantes" → 6 en el README.
6. Sacar **capturas de los commits del esqueleto** (Fase 1 y Fase 2) para el informe.
   ⚠ Acción destructiva sobre repo de un compañero: confirmar con Conrado antes de pushear.

### PENDIENTE (próximas sesiones)
- [x] **Revisar el repo GitHub** traineros-api (hecho — ver diagnóstico arriba).
- [ ] **Subir todo a GitHub** (reemplazando lo actual) según el plan de arriba.
- [ ] **Subir todo a GitHub** (reemplazando lo actual). Commits en español, sin mención a
      herramientas de IA, sin emojis. Sacar **capturas de los commits del esqueleto**
      (Fase 1 y Fase 2) que pide la consigna.
- [ ] **Completar la presentación** con las Fases 3, 4 y 5 (hoy solo se armaron 1 y 2).
      El deck final apunta a 12 slides (ver numeración "X / 12" en los pies).
- [ ] **Informe final** (PDF) — está casi todo en TFI_TrainerOS.docx; falta armar el PDF
      con capturas de commits y links.
- [ ] **Artículo técnico** (Medium/LinkedIn).
- [ ] **Grabar el video** (12-20 min, todos hablan).

---

## Plan de la presentación (deck completo apuntado: ~14 min, 12 slides)

Hoy se armaron las slides 1-9 (cubren Fases 1 y 2). Faltan 10-12 (Fases 3-5).

| # | Slide | Fase | Expone | Tiempo |
|---|-------|------|--------|--------|
| 1 | Portada | — | Conrado Gómez | 0:30 |
| 2 | Problema y modelo de negocio | Contexto | Conrado Gómez | 1:00 |
| 3 | Monolito modular 3 capas (diagrama) | 1 | Nicolás Zyngale | 1:45 |
| 4 | Justificación y límites | 1 | Nicolás Zyngale | 1:15 |
| 5 | Cambio de contexto (B2B) | 2 | Matías Saravia | 1:00 |
| 6 | Microservicios tradicionales (diagrama) | 2A | Matías Saravia | 1:30 |
| 7 | Microservicios modernos / eventos (diagrama) | 2B | Lautaro Naglieri | 1:45 |
| 8 | Patrones aplicados (tabla) | 2 | Lautaro Naglieri | 1:15 |
| 9 | Las 3 arquitecturas en una mirada | 1+2 | (transición) | 0:30 |
| 10 | Robustez y escalabilidad (Redis, replicas, LB) | 3 | Pablo Czurylo | 1:30 |
| 11 | Infra, DevOps, ambientes y costos | 4 | Pablo Czurylo | 1:45 |
| 12 | Integración con IA + cierre | 5 | Leandro Gramajo | 1:30 |

Total aprox: **~14:45** (margen para ajustar al rango 12-15 min). Cada integrante
expone su bloque y describe lo que hizo (el profe rechaza el "leer títulos").

> Nota: la consigna escrita dice 10 min, pero el profe en el audio aclaró 12-20 min
> para grupos numerosos (somos 6). Apuntamos a 12-15.
