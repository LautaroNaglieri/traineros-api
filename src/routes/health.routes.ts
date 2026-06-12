import { Router, type Request, type Response } from 'express';

/**
 * Router de healthcheck. Lo usan los balanceadores de carga y las probes de
 * Kubernetes (readiness/liveness) para saber si la instancia está viva.
 */
export const healthRouter = Router();

healthRouter.get('/health', (_req: Request, res: Response) => {
  res.status(200).json({
    status: 'ok',
    service: 'traineros-api',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
  });
});
