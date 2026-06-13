/**
 * CAPA 1 · Presentación — rutas del módulo Rutinas.
 * Cadena: jwt -> tenant -> controller. (Ejemplo de cableado; sin lógica de negocio.)
 */
import { Router } from 'express';
import { RutinasService } from '@application/rutinas/rutinas.service';
import { RutinasController } from '../controllers/rutinas.controller';
import { jwtMiddleware } from '../middlewares/jwt.middleware';
import { tenantMiddleware } from '../middlewares/tenant.middleware';

export function buildRutinasRoutes(service: RutinasService): Router {
  const router = Router();
  const controller = new RutinasController(service);

  router.use(jwtMiddleware, tenantMiddleware);

  router.get('/', controller.listar);
  router.post('/', controller.crear);

  return router;
}
