import { type Request, type Response, type NextFunction } from 'express';

/**
 * Middleware de autenticación JWT (placeholder del esqueleto).
 *
 * En el MVP todavía NO valida el token: solo deja el punto de extensión donde,
 * en la siguiente iteración, se verificará el JWT y se inyectará el `trainerId`
 * en `req` para garantizar el aislamiento multitenant en cada consulta.
 */
export function authMiddleware(_req: Request, _res: Response, next: NextFunction): void {
  // TODO(fase-1): verificar Authorization: Bearer <jwt>, decodificar y
  // adjuntar { trainerId } al request. Por ahora pasa de largo.
  next();
}
