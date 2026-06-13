/**
 * CAPA 1 · Presentación — middleware JWT (VACÍO en el esqueleto).
 * Según la consigna de la Fase 1, el esqueleto incluye el middleware JWT pero
 * todavía sin lógica de validación. Aquí queda el punto de extensión.
 */
import { Request, Response, NextFunction } from 'express';

// Extiende el Request de Express con los datos de autenticación.
declare global {
  // eslint-disable-next-line @typescript-eslint/no-namespace
  namespace Express {
    interface Request {
      userId?: string;
      trainerId?: string;
    }
  }
}

export function jwtMiddleware(_req: Request, _res: Response, next: NextFunction): void {
  // TODO (post-esqueleto): leer Authorization, verificar token con JWT_SECRET,
  // y poblar req.userId. Por ahora, solo continúa la cadena.
  next();
}
