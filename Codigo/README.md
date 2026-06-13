# Código — Esqueletos de arquitectura (diseño)

Esta carpeta contiene el **diseño en código** (esqueletos / boilerplate) de las dos
primeras fases de TrainerOS. El objetivo del TFI es ejercitar el criterio de
**diseñador de software**: no se implementa el producto completo, sino la estructura
que demuestra cada decisión arquitectónica.

| Carpeta | Fase | Arquitectura |
|---------|------|--------------|
| [`traineros-api/`](./traineros-api) | Fase 1 | Monolito modular **en capas** (3-tier) — reemplaza el repo actual |
| [`fase2-microservicios/`](./fase2-microservicios) | Fase 2 | Monorepo de microservicios (REST → event-driven) |

> Importante: el repositorio `traineros-api` original estaba organizado como
> "monolito modular" (por features), no **en capas**. Este esqueleto corrige eso:
> la estructura está organizada por capas con dependencias en una sola dirección
> (presentación → aplicación → dominio ← infraestructura). Ver
> [`traineros-api/README.md`](./traineros-api/README.md).
