/** MS Pagos — esqueleto. Membresias y cobros; PUBLICA pago.confirmado. */
import express from 'express';
const app = express();
app.get('/health', (_req, res) => res.json({ status: 'ok', service: 'pagos' }));
app.listen(3003, () => console.log('[pagos] escuchando en :3003'));
