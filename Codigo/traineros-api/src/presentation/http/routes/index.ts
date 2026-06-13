/** CAPA 1 · Presentación — registro central de rutas. */
import { Router } from 'express';
import { ServerDeps } from '../server';
import { healthRoutes } from './health.routes';
import { buildRutinasRoutes } from './rutinas.routes';

export function buildRoutes(deps: ServerDeps): Router {
  const router = Router();

  router.use('/health', healthRoutes());
  router.use('/api/rutinas', buildRutinasRoutes(deps.rutinasService));

  return router;
}
