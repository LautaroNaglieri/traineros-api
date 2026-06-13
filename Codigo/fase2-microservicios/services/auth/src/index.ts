/** MS Auth & Tenants — esqueleto. Emite/valida JWT y resuelve el tenant. */
import express from 'express';
const app = express();
app.get('/health', (_req, res) => res.json({ status: 'ok', service: 'auth' }));
app.listen(3000, () => console.log('[auth] escuchando en :3000'));
