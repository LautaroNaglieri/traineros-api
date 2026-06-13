/** MS Catalogo — esqueleto. Catalogo global de ejercicios (casi 100% lecturas). */
import express from 'express';
const app = express();
app.get('/health', (_req, res) => res.json({ status: 'ok', service: 'catalogo' }));
app.listen(3002, () => console.log('[catalogo] escuchando en :3002'));
