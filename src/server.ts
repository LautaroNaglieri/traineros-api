import { createApp } from './app.js';
import { env } from './config/env.js';

/**
 * Punto de entrada del servidor.
 * Levanta la aplicación Express en el puerto configurado.
 */
const app = createApp();

const server = app.listen(env.PORT, () => {
  console.log(`TrainerOS API escuchando en http://localhost:${env.PORT} [${env.NODE_ENV}]`);
});

// Apagado ordenado (graceful shutdown)
for (const signal of ['SIGINT', 'SIGTERM'] as const) {
  process.on(signal, () => {
    console.log(`\n${signal} recibido. Cerrando servidor...`);
    server.close(() => process.exit(0));
  });
}
