/**
 * API Gateway — esqueleto.
 * Punto unico de entrada: valida JWT, aplica rate limiting y rutea a cada
 * microservicio. Los clientes no conocen la topologia interna. (Sin logica.)
 */
import express from 'express';
const app = express();

// Mapa de ruteo (en el real se hace con un reverse proxy / http-proxy-middleware).
const RUTAS = {
  '/api/auth': 'http://auth:3000',
  '/api/rutinas': 'http://rutinas:3001',
  '/api/catalogo': 'http://catalogo:3002',
  '/api/pagos': 'http://pagos:3003',
};

app.get('/health', (_req, res) => res.json({ status: 'ok', gateway: true, rutas: Object.keys(RUTAS) }));
app.listen(8080, () => console.log('[gateway] escuchando en :8080'));
