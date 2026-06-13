/**
 * CAPA 1 · Presentación — bootstrap de Express.
 * Arma la app HTTP: middlewares base, rutas y manejo de errores.
 * No contiene lógica de negocio: solo orquesta el transporte HTTP.
 */
import express, { Application } from 'express';
import { RutinasService } from '@application/rutinas/rutinas.service';
import { buildRoutes } from './routes';
import { errorMiddleware } from './middlewares/error.middleware';

export interface ServerDeps {
  rutinasService: RutinasService;
}

export function buildServer(deps: ServerDeps): Application {
  const app = express();

  app.use(express.json());
  app.use('/', buildRoutes(deps));

  // El manejo de errores va al final de la cadena
  app.use(errorMiddleware);

  return app;
}
