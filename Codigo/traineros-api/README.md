# TrainerOS API — Fase 1: Monolito Modular **en Capas** (3-tier)

Esqueleto / *boilerplate* del backend de TrainerOS. Implementa una arquitectura
**monolito modular organizado por capas (3-tier)**, no por features sueltas.

> Nota de diseño: la diferencia con un "monolito modular" a secas es que aquí la
> dependencia fluye **en una sola dirección entre capas**
> (`presentación → aplicación → dominio ← infraestructura`). Cada capa tiene una
> única responsabilidad y solo conoce a la capa inmediatamente inferior mediante
> **interfaces**, nunca implementaciones concretas. Esto es lo que permite, en la
> Fase 2, extraer cada módulo de negocio como microservicio sin reescribir la lógica.

## Las 3 capas

```
src/
├─ presentation/      ← CAPA 1 · Presentación (HTTP)
│  └─ http/
│     ├─ routes/         Define las rutas REST y las asocia a controllers
│     ├─ controllers/    Traduce HTTP <-> casos de uso (sin lógica de negocio)
│     ├─ middlewares/    JWT, aislamiento multitenant, manejo de errores
│     └─ validators/     DTOs / validación de entrada
│
├─ application/       ← CAPA 2 · Aplicación / Negocio
│  ├─ auth/             Casos de uso de identidad
│  ├─ rutinas/          Casos de uso del núcleo (constructor de rutinas)
│  ├─ catalogo/         Casos de uso del catálogo de ejercicios
│  └─ pagos/            Casos de uso de membresías y cobros
│
├─ domain/            ← Núcleo · Entidades y contratos (independiente del framework)
│  ├─ entities/         Modelos de negocio puros (sin Prisma, sin Express)
│  └─ repositories/     INTERFACES de persistencia (puertos)
│
├─ infrastructure/    ← CAPA 3 · Datos / Infraestructura
│  ├─ database/
│  │  ├─ prisma/         Cliente Prisma (ORM)
│  │  └─ repositories/   IMPLEMENTACIONES Prisma de las interfaces de dominio
│  └─ config/           Carga y valida variables de entorno
│
├─ shared/            Utilidades transversales (errores, logger)
└─ main.ts            Punto de entrada: arma dependencias y levanta el server
```

### Regla de dependencias

```
presentation ──▶ application ──▶ domain ◀── infrastructure
                                   ▲
                       (las capas externas dependen del dominio,
                        el dominio no depende de nadie)
```

La capa de aplicación define **qué** necesita persistir (interfaz en `domain/repositories`).
La capa de infraestructura decide **cómo** lo persiste (Prisma + PostgreSQL). Se inyecta
la implementación en `main.ts`. Cambiar de ORM o de base no toca la lógica de negocio.

## Stack

| Capa          | Tecnología                          | Justificación breve |
|---------------|-------------------------------------|---------------------|
| Presentación  | Express + TypeScript                | Rápido, ecosistema enorme, tipado de punta a punta |
| Aplicación    | TypeScript (servicios planos)       | Lógica de negocio aislada del framework |
| Datos         | Prisma ORM + PostgreSQL             | Modelo relacional (entidades interconectadas) + multitenant por `trainer_id` |

## Estado de este esqueleto (Fase 1)

Según la consigna, el repositorio en esta fase contiene **solo boilerplate, sin lógica
de negocio**:

- [x] Configuración de Express + TypeScript
- [x] Prisma con esquema base y migración inicial
- [x] Middleware JWT (vacío) y middleware de aislamiento multitenant
- [x] ESLint + Prettier
- [x] Healthcheck (`GET /health`)
- [ ] Lógica de negocio (se implementa después del esqueleto)

## Scripts

```bash
npm install
docker compose up -d        # levanta PostgreSQL local
npm run prisma:migrate      # aplica la migración base
npm run dev                 # levanta la API en modo desarrollo
```

## Estrategia de ramas (GitHub Flow extendido)

- `main` → producción
- `dev`  → integración
- ramas temporales: `feat/*`, `fix/*`, `chore/*`

Los commits del esqueleto son del tipo:
`chore: init express + typescript`, `chore: setup prisma + schema base`,
`chore: eslint y prettier`, `feat: healthcheck endpoint`.
