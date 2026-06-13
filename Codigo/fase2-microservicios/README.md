# TrainerOS — Fase 2: Microservicios (esqueleto de monorepo)

Esqueleto de la evolución a microservicios. Muestra cómo el monolito en capas de la
Fase 1 se descompone por **capacidades de negocio** (los mismos módulos: Auth, Rutinas,
Catálogo, Pagos, Notificaciones), primero con REST síncrono (Paso A) y luego orientado
a eventos con un Message Broker (Paso B).

## Estructura

```
fase2-microservicios/
├─ gateway/                 API Gateway (ruteo, rate limiting, validación JWT)
├─ services/
│  ├─ auth/                 MS Auth & Tenants   (identidad, JWT, multitenant)
│  ├─ rutinas/              MS Rutinas          (núcleo · PUBLICA eventos)
│  ├─ catalogo/             MS Catálogo         (lecturas)
│  ├─ pagos/                MS Pagos            (membresías · PUBLICA eventos)
│  └─ notificaciones/       MS Notificaciones   (SUSCRIBE eventos)
├─ shared-contracts/        Contratos compartidos
│  └─ events/               Definición de los eventos de negocio (tipados)
├─ infra/                   IaC y manifiestos (Terraform, k8s) — Fase 3/4
└─ docker-compose.yml       Levanta servicios + emulador de Pub/Sub
```

Cada servicio es **autónomo**: su propio `package.json`, su propio `Dockerfile`
y su propia base de datos (patrón **Database per Service**). No comparten esquema.

## Paso A → Paso B

- **Paso A (tradicional):** los servicios se llaman por HTTP/REST a través del Gateway.
  Limitación: acoplamiento temporal (si un servicio cae, la cadena falla).
- **Paso B (moderno, event-driven):** Rutinas y Pagos **publican** hechos de negocio
  (`rutina.asignada`, `pago.confirmado`, ...) en **Google Pub/Sub**; Notificaciones,
  Analytics y Query (CQRS) los **consumen**. Desacople temporal + reintentos.

Patrones aplicados: API Gateway · Database per Service · Pub/Sub · CQRS · Saga ·
Circuit Breaker (ver presentación, slide 8).

## Estado

Esqueleto de los microservicios interconectados (sin lógica de negocio), según pide
la consigna de la Fase 2. Los contratos de eventos en `shared-contracts/events`
son el "lenguaje común" entre servicios.
