/** CAPA 1 · Presentación — manejo centralizado de errores. */
import { Request, Response, NextFunction } from 'express';
import { AppError } from '@shared/errors';
import { logger } from '@shared/logger';

// eslint-disable-next-line @typescript-eslint/no-unused-vars
export function errorMiddleware(err: unknown, _req: Request, res: Response, _next: NextFunction): void {
  if (err instanceof AppError) {
    res.status(err.status).json({ error: err.message });
    return;
  }
  logger.error('Error no controlado', err);
  res.status(500).json({ error: 'Error interno' });
}
