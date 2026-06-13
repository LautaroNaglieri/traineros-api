/**
 * MS Rutinas — esqueleto.
 * Internamente mantiene las 3 capas de la Fase 1 (presentación/aplicación/datos),
 * pero ahora es autónomo y PUBLICA eventos en el broker en vez de llamar a otros
 * servicios por HTTP. (Sin lógica de negocio.)
 */
import express from 'express';
import { TOPICS, EventEnvelope, RutinaAsignada } from '../../../shared-contracts/events';

const app = express();
app.use(express.json());

app.get('/health', (_req, res) => res.json({ status: 'ok', service: 'rutinas' }));

// Ejemplo de cableado de publicación (el publish real usa el SDK de Pub/Sub).
app.post('/rutinas', async (_req, res) => {
  const evento: EventEnvelope<RutinaAsignada> = {
    id: crypto.randomUUID(),
    topic: TOPICS.RUTINA_ASIGNADA,
    ocurridoEn: new Date().toISOString(),
    tenantId: 'tenant-demo',
    data: { rutinaId: 'r-1', alumnoId: 'a-1' },
  };
  // TODO (post-esqueleto): persistir la rutina y publicar `evento` en Pub/Sub.
  res.status(202).json({ publicado: evento.topic });
});

app.listen(3001, () => console.log('[rutinas] escuchando en :3001'));
