# Guía de contribución — TrainerOS

Equipo de 8 integrantes. Para evitar conflictos de merge y mantener `main` siempre
desplegable, seguimos un **GitHub Flow extendido**.

## Ramas

| Rama      | Propósito                             | Reglas                                 |
| --------- | ------------------------------------- | -------------------------------------- |
| `main`    | Producción. Siempre desplegable.      | Protegida. Solo entra por PR aprobado. |
| `dev`     | Integración del equipo.               | Base de las ramas de trabajo y los PR. |
| `feat/*`  | Nueva funcionalidad.                  | Temporal. Se borra al mergear.         |
| `fix/*`   | Corrección de bug.                    | Temporal. Se borra al mergear.         |
| `chore/*` | Config, tooling, docs, mantenimiento. | Temporal. Se borra al mergear.         |

### Nombre de ramas

```
feat/constructor-rutinas
fix/jwt-expiracion
chore/setup-eslint
```

## Flujo de trabajo

1. Partí siempre de `dev` actualizada:
   ```bash
   git checkout dev && git pull
   git checkout -b feat/mi-tarea
   ```
2. Commits chicos y descriptivos siguiendo **Conventional Commits**:
   ```
   feat: ...    fix: ...    chore: ...    docs: ...    refactor: ...    test: ...
   ```
3. Abrí un **Pull Request hacia `dev`**. Debe pasar CI (lint + typecheck) y tener
   al menos **1 review aprobado** de otro integrante.
4. Una vez en `dev` y validado, se promueve a `main` mediante PR `dev → main`.

## Mapeo con ambientes (Fases 4)

| Evento Git               | Ambiente / acción                        |
| ------------------------ | ---------------------------------------- |
| PR `feat/*` o `fix/*`    | CI: lint + tests + build.                |
| Merge a `dev`            | Deploy automático a Testing/QA.          |
| PR `dev → main` aprobado | Deploy a Producción (aprobación manual). |

> En el MVP (Fase 1) solo viven `main` y `dev`; el resto del pipeline se incorpora
> en fases posteriores del TFI.
