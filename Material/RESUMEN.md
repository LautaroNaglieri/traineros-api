# Material de referencia — TFI Desarrollo de Aplicaciones Web

Carpeta con la documentación fuente del trabajo. Archivos:

- **`TFI_TrainerOS.docx`** — Documento maestro del proyecto (las 5 fases desarrolladas).
- **`Consigna_TFI_Desarrollo_Web.docx`** — Consigna oficial del profesor.
- **`transcripcion_audio_profesor.txt`** — Transcripción del audio donde explica la consigna.

---

## La consigna en una página

Proyecto incremental en **5 fases** que simula la evolución de un producto real.
Libertad total de stack, pero **toda decisión debe justificarse** (criterio de
negocio, costo y rendimiento). Se evalúa el **criterio de diseñador**, no el código.

| Fase | Qué pide |
|------|----------|
| **1** | Arquitectura base (MVP): monolito tradicional/capas/MVC. Diagrama + justificación (por qué alcanza, cuáles son sus límites) + repo Git con estrategia de ramas + captura de commits del esqueleto. |
| **2** | Evolución a microservicios. **Paso A**: tradicional (REST síncrono). **Paso B**: moderno event-driven (Message Broker). Diagramas de ambas + patrones (API Gateway, CQRS, Circuit Breaker, Saga). Captura de commits del esqueleto de microservicios. |
| **3** | Robustez y escalabilidad: caché (Redis), read replicas, balanceadores, auto-scaling. |
| **4** | Infra/DevOps: nube, ambientes (Desa/QA/UAT/Prod), branching, CI/CD, Docker/Kubernetes, Terraform, **estimación de costos**. |
| **5** | Integración con IA: APIs de LLM (Opción A) o RAG con base vectorial (Opción B). |

### Entregables obligatorios
1. **Informe final** (PDF) con justificación técnica y de negocio de cada decisión + enlaces a repos + capturas de commits.
2. **Presentación ejecutiva** (defensa oral simulando venta a un CTO). **Regla estricta: NO se muestra código.** Solo diagramas, evolución, infra y justificación.
3. **Artículo técnico** (Medium/LinkedIn) en primera persona: desafíos, aprendizajes del paso de "programar" a "diseñar".

### Criterios de evaluación
- Criterio arquitectónico (40%) · Infra y DevOps (30%) · Evolución e IA (15%) · Calidad de entregables (15%).

---

## Puntos clave del audio del profesor

- Elegir arquitectura y **justificarla** (no "porque me gusta"). Recomienda no arrancar
  con monolito desorganizado; si es monolito, que tenga **al menos las 3 capas** (API)
  para poder extrapolar a microservicios.
- El **esqueleto en código** debe mostrar las carpetas de las 3 capas (presentación /
  negocio / ORM-datos). No importa si aún no hay base de datos cargada.
- Hacer el **diagrama de arquitectura** (cómo se conecta y organiza todo) — "que sea hermoso".
- Microservicios: diagrama tradicional y diagrama moderno (el moderno suma automatización
  y herramientas de IA; el diagrama es parecido).
- Infra: cantidad de servidores, equipo (pensar ~10 personas), branching + automatización
  (commit → validación → test → dev → prod), contenedores/Kubernetes/Docker/Terraform,
  y **estimación de costos** (averiguar precios reales, validar con IA).
- RAG/IA: puede ir como servicio aparte, "por fuera" de la arquitectura; justificar dónde entra.
- **Presentación**: slide presentable en ~10-12 min, **4 o 5 diapositivas** (idea →
  arquitectura inicial → arquitectura a microservicios → robustez/escalabilidad → infra).
- **Video** (entrega no presencial): **12 a 20 min** para grupo numeroso. **Todos hablan**
  y describen lo que hicieron (no leer títulos, no leer de corrido). Si no, manda a rendir.
- **Fecha límite: 19/06/2026.** Se puede ir compartiendo el informe por Google Docs para
  correcciones. Mail del profe: Dr.zottola@gmail.com.
