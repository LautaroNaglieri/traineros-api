# Bitácora del TFI — TrainerOS (Desarrollo de Aplicaciones Web)

Registro de todo lo que se va haciendo, con fecha y hora, para tener siempre el
contexto completo del proyecto. Lo más nuevo arriba.

Equipo (6): Conrado Gómez · Nicolás Zyngale · Matías Saravia · Lautaro Naglieri ·
Pablo Czurylo · Leandro Gramajo · **Grupo VOX**. (La empresa/producto ficticio del
caso de negocio es **TrainerOS**; se quitó toda referencia a la marca "MMP-SOFTWARE".)

Fecha límite de entrega: **19/06/2026**. Mail del profe: **Dr.zottola@gmail.com**
Repo del código: https://github.com/LautaroNaglieri/traineros-api

---

## 2026-06-15 — Sesión 2: borrador del informe pulido, diagramas completos e informe en Google Docs

### Qué se hizo
1. **Correcciones al informe maestro** (`Material/TFI_TrainerOS.docx`):
   - **Autoría** → "Autores — Grupo VOX" con los 6 integrantes (antes decía "Lautaro Naglieri").
     Corregidos también los metadatos del archivo (autor/título), que estaban en "Un-named".
   - **Eliminada toda mención a "MMP-SOFTWARE"** (cuerpo + tablas). La empresa ficticia pasa a
     llamarse simplemente **TrainerOS**; se conservó el argumento de "la empresa crece a 3 equipos"
     (justifica microservicios — ley de Conway, es lo que pide la consigna).
   - Arreglos detectados por un **agente que simuló ser el profesor** (revisión crítica del borrador):
     costos no-prod unificados a **$150** (total ~$670; antes "$120–150"); celda de branching con `|`
     literal → `·`; "6 tópicos" → **"6 tópicos (4 de negocio + 2 de IA)"**; índice vacío → índice manual.
2. **Diagramas draw.io** (`Presentacion/diagramas/drawio/` + generador `build_drawio.py`):
   - **fase2a (tradicional) rehecho completo**: 5 servicios con **BD propia etiquetada** (incl. la de
     Notificaciones: log de envíos · plantillas · prefs · idempotencia) y las **llamadas REST síncronas**
     dibujadas entre cajas adyacentes (Notificaciones reubicado al centro para evitar cruces). Antes el
     diagrama no mostraba ninguna llamada entre servicios, contradiciendo su nota de "acoplamiento temporal".
   - **fase2b (eventos) corregido**: el API Gateway estaba **desconectado** (no llegaba a los servicios);
     ahora rutea los comandos a Rutinas y Pagos.
   - **Creados fase3 (robustez/escalabilidad) y fase5 (integración IA, flujo asíncrono)**. Faltaban.
   - Render a PNG con **draw.io desktop** (escala 2).
3. **Figuras del docx**: el documento **ya tenía 5 figuras embebidas viejas/desprolijas**; se
   reemplazaron las **5** (Figuras 1–5) por las versiones limpias de draw.io, manteniendo ancho 620 px.
4. **Capturas de commits del esqueleto** (lo que pide la consigna) insertadas en el docx con epígrafe + link:
   - **Fase 1**: commit `2e1baa5` "esqueleto del monolito modular en capas" (detalle + árbol de las 3 capas
     presentation/application/domain/infrastructure). Imágenes en `Material/commits-fase-1/`.
   - **Fase 2**: commit `c743488` "esqueleto del monorepo de microservicios" (gateway + 5 servicios +
     shared-contracts + docker-compose con Pub/Sub). Imágenes en `Material/commits-fase-2/`.
   - Son las **2 únicas** capturas de commits que exige la consigna (Fases 3/4/5 son conceptuales).
5. **Presentación** regenerada (`build_pptx.py`): portada "Grupo VOX" + toma los PNG corregidos.
   ⚠ Sigue cubriendo **solo Fases 1–2** (9 slides). Pendiente completar a 5 fases.
6. **README + esta bitácora**: "MMP-SOFTWARE" → **Grupo VOX**.
7. **Informe formal en Google Docs**: se subió el `.docx` a Drive y se **convirtió** a Google Doc nativo
   **"TFI_TrainerOS"** (comentable por el profe, exportable a PDF). URL:
   https://docs.google.com/document/d/1rOQxEYt8FT7fUDVfMSMYxHFX2v_mYKIEvHSRzYZaYX8/edit
   Conversión verificada slide/figura por figura: las 5 figuras + 2 capturas + tablas quedaron bien.
   PDF exportado a `Informe/TFI_TrainerOS.pdf`.

### Notas / decisiones
- El intento de armar el Google Doc **tipeando a mano** (Markdown auto-detect funciona) se descartó:
  insertar 7 imágenes a mano es frágil. La vía confiable fue **subir el .docx y convertirlo**.
- La **subida de archivos al navegador no se puede automatizar** (diálogo nativo / input en iframe);
  ese paso lo hace Conrado a mano.
- **Compartir el Google Doc** con el profe (rol Comentador) lo hace Conrado (no se modifican permisos por él).

### PENDIENTE
- [ ] Compartir el Google Doc con el profe como **Comentador** (Conrado).
- [ ] **Completar la presentación** a las 5 fases (hoy 1–2; ya existen los diagramas de 3 y 5).
      Debe entrar en **10 min** (consigna): recortar texto y apuntar a pocas slides.
- [ ] **Artículo técnico** (Medium/LinkedIn) — sin empezar.
- [ ] Grabar el **video** (12–20 min, todos hablan).

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

### Decisiones / notas técnicas (estado FINAL)
- **Diagramas**: son archivos **.drawio reales** (editables) en `Presentacion/diagramas/drawio/`,
  generados por `Presentacion/generador/build_drawio.py` y renderizados a PNG con el **draw.io
  desktop** (`render_drawio.sh`). Estilo elegido por Conrado: **draw.io clásico** (rectángulos
  rectos, bordes/flechas negras, rellenos planos azul/dorado/verde, flujo vertical). Tomó como
  referencia su captura. (Iteraciones previas: HTML→PIL→draw.io; quedó draw.io.)
- **Presentación**: `build_pptx.py` arma el `.pptx`. Las slides de texto son formas nativas
  editables; las de diagrama embeben los PNG ajustados sin distorsión. **Estilo corporativo
  tipo "Naturgy en un Scan"**: azul #1F4E79 + naranja #E8741E + gris, barra naranja al pie.
  (Referencia: `UNSTA/innovation-challenge/docs/Presentacion_Semifinal_Naturgy_en_un_Scan.pptx`.)
- Para verificar el pptx: `export_png.py` usa PowerPoint vía COM, pero **abre desde C:\Temp**
  (PowerPoint no abre rutas del Desktop sincronizado con OneDrive).
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

### Push a GitHub — HECHO (13/06)
- `Final/` ahora es repo git conectado a `origin` (LautaroNaglieri/traineros-api).
- Se hicieron 5 commits en español (sin IA, sin emojis) sobre la historia existente y se
  pusheó a **`main`** (no estaba protegida; push directo OK): `350e02a..61cb0ff`.
  - `chore: reorganiza el repositorio como workspace del TFI`
  - `feat: esqueleto del monolito modular en capas (Fase 1)`
  - `feat: esqueleto del monorepo de microservicios (Fase 2)`
  - `docs: presentacion ejecutiva y diagramas de las fases 1 y 2`
  - `docs: material de referencia y resumen de la consigna`
- `main` quedó con: .claude, Material, Presentacion, Codigo (traineros-api + fase2-microservicios),
  Informe, Articulo, README.md. El layout viejo (src/ por features en la raíz) fue reemplazado.
- Commits de esqueleto previos (express, prisma, eslint, healthcheck) se conservan en la historia.
- Config commit: user "Conrado Gómez" <conradogomez556@gmail.com>.

### Diagramas: ahora son .drawio REALES (13/06)
- Los 4 diagramas son **archivos `.drawio` nativos** (mxGraph), editables en draw.io /
  diagrams.net, en `Presentacion/diagramas/drawio/`. Se renderizan a PNG con el **draw.io
  desktop** (instalado en `C:\Program Files\draw.io\draw.io.exe`).
- Generador: `Presentacion/generador/build_drawio.py` → produce los .drawio.
  Render: `render_drawio.sh` (o el comando del README del generador). Pipeline en
  `Presentacion/generador/README.md`. (Se eliminó el generador PIL `build_diagrams.py`.)
- Motivo: las versiones anteriores (PIL) "se veían hechas por código"; ahora es draw.io
  de verdad renderizando los diagramas.

### PENDIENTE (próximas sesiones)
- [x] Revisar el repo GitHub (diagnóstico arriba).
- [x] Subir todo a GitHub reemplazando lo anterior (en `main`).
- [ ] **Sincronizar la rama `dev`**: quedó con el layout viejo. Si el equipo branchea desde
      `dev`, vería la estructura vieja. Decidir con el equipo si se actualiza `dev` al nuevo workspace.
- [ ] **Capturas de los commits del esqueleto** (Fase 1 y Fase 2) para el informe.
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

Total aprox: **~14:45** — pero el objetivo es **10 min** (ver nota), hay que recortar. Cada integrante
expone su bloque y describe lo que hizo (el profe rechaza el "leer títulos").

> Nota (Conrado, 15/06): la presentación es de **10 min** (consigna). El deck armado
> hoy apunta a ~14 min, así que al completarlo a las 5 fases hay que recortar para entrar
> en 10 min (menos texto por slide, transiciones rápidas).
