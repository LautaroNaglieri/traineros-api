/** CAPA 1 · Presentación — healthcheck (lo único 100% funcional del esqueleto). */
import { Router, Request, Response } from 'express';

export function healthRoutes(): Router {
  const router = Router();

  router.get('/', (_req: Request, res: Response) => {
    res.status(200).json({ status: 'ok', service: 'traineros-api', ts: new Date().toISOString() });
  });

  return router;
}
