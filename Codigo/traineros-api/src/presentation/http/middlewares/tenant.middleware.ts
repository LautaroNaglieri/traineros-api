/**
 * CAPA 1 · Presentación — aislamiento multitenant.
 * Toma el trainer_id del token (lo pondrá el jwtMiddleware) y lo deja en
 * req.trainerId para que TODA consulta de negocio quede acotada a ese tenant.
 * Esqueleto: el cableado existe; la extracción real se completa con el JWT.
 */
import { Request, Response, NextFunction } from 'express';

export function tenantMiddleware(req: Request, _res: Response, next: NextFunction): void {
  // TODO (post-esqueleto): derivar el trainerId del claim del JWT.
  req.trainerId = req.userId ?? 'tenant-demo';
  next();
}
