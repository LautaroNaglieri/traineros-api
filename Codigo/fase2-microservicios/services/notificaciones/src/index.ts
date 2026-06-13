/**
 * MS Notificaciones — esqueleto.
 * SUSCRIBE eventos del broker y reacciona (push/email/WhatsApp). No expone API de
 * negocio: vive de la cola. Idempotente por `id` (Pub/Sub entrega at-least-once).
 * (Sin lógica de negocio.)
 */
import { TOPICS, EventEnvelope, RutinaAsignada, PagoConfirmado } from '../../../shared-contracts/events';

// Esqueleto del consumidor: en el real, cada handler se registra en una suscripción.
const handlers: Record<string, (e: EventEnvelope<unknown>) => Promise<void>> = {
  [TOPICS.RUTINA_ASIGNADA]: async (e) => {
    const _data = e.data as RutinaAsignada;
    // TODO: enviar push "tenés nueva rutina".
  },
  [TOPICS.PAGO_CONFIRMADO]: async (e) => {
    const _data = e.data as PagoConfirmado;
    // TODO: enviar recibo / confirmación.
  },
};

console.log('[notificaciones] suscripto a:', Object.keys(handlers).join(', '));
