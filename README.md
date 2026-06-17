# TrainerOS — Trabajo Final Integrador (Desarrollo de Aplicaciones Web)

Workspace del TFI del **Grupo VOX** (6 integrantes): diseño de la evolución
arquitectónica de **TrainerOS**, una plataforma SaaS B2B2C de gestión para entrenadores
personales.

> "Del Código a la Arquitectura: El Criterio del Desarrollador"

El objetivo del trabajo es ejercitar el criterio de **diseñador de software**: cada
decisión arquitectónica está justificada por negocio, costo y rendimiento.

## Organización del repositorio

| Carpeta | Contenido |
|---------|-----------|
| [`Material/`](./Material) | Documentación fuente: consigna, documento maestro del proyecto y resumen. |
| [`Presentacion/`](./Presentacion) | Presentación ejecutiva (`.pptx`) de las 5 fases (10 min) y diagramas de arquitectura. |
| [`Codigo/`](./Codigo) | Esqueletos de código (diseño): monolito modular **en capas** (Fase 1) y microservicios (Fase 2). |
| [`Informe/`](./Informe) | Informe final (PDF) — en preparación. |
| [`Articulo/`](./Articulo) | Artículo técnico de divulgación — en preparación. |
| `.claude/info.md` | Bitácora del proyecto (qué se hizo, cuándo y qué falta). |

## Evolución arquitectónica (5 fases)

1. **Monolito modular en 3 capas** (MVP) — Node.js + Express + Prisma + PostgreSQL.
2. **Microservicios**: tradicionales (REST síncrono) → modernos (event-driven con Pub/Sub).
3. Robustez y escalabilidad (Redis, read replicas, balanceo, auto-scaling).
4. Infraestructura, DevOps y costos (GKE, Terraform, CI/CD, 4 ambientes en GCP).
5. Integración con IA (APIs de LLM).

## Equipo

Grupo VOX — Conrado Gómez · Nicolás Zyngale · Matías Saravia · Lautaro Naglieri ·
Pablo Czurylo · Leandro Gramajo.

## Estrategia de ramas

GitHub Flow extendido: `main` (producción) · `dev` (integración) · ramas temporales
`feat/*`, `fix/*`, `chore/*`. Toda contribución entra por Pull Request a `dev`.
