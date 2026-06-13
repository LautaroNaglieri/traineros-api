/**
 * Contratos de eventos de negocio (compartidos entre microservicios).
 * Son el "lenguaje común": un publicador y un suscriptor acuerdan esta forma.
 * Esqueleto: solo las definiciones tipadas, sin lógica.
 */

export const TOPICS = {
  RUTINA_ASIGNADA: 'rutina.asignada',
  ENTRENAMIENTO_COMPLETADO: 'entrenamiento.completado',
  PAGO_CONFIRMADO: 'pago.confirmado',
  MEMBRESIA_POR_VENCER: 'membresia.por_vencer',
} as const;

export type Topic = (typeof TOPICS)[keyof typeof TOPICS];

export interface EventEnvelope<T> {
  id: string; // idempotencia (Pub/Sub entrega at-least-once)
  topic: Topic;
  ocurridoEn: string; // ISO 8601
  tenantId: string; // trainer_id
  data: T;
}

export interface RutinaAsignada {
  rutinaId: string;
  alumnoId: string;
}

export interface PagoConfirmado {
  membresiaId: string;
  alumnoId: string;
  monto: number;
}
