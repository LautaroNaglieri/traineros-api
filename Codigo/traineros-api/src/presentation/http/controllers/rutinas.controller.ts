/**
 * CAPA 1 · Presentación — controller de Rutinas.
 * Traduce HTTP <-> caso de uso. No decide reglas de negocio: delega en el service.
 * Esqueleto: los handlers están cableados pero la lógica vive (vacía) en la capa
 * de aplicación.
 */
import { Request, Response, NextFunction } from 'express';
import { RutinasService } from '@application/rutinas/rutinas.service';

export class RutinasController {
  constructor(private readonly service: RutinasService) {}

  listar = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      // req.trainerId lo inyecta el tenantMiddleware desde el JWT
      const rutinas = await this.service.listarPorEntrenador(req.trainerId!);
      res.json(rutinas);
    } catch (err) {
      next(err);
    }
  };

  crear = async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    try {
      const rutina = await this.service.crear(req.trainerId!, req.body);
      res.status(201).json(rutina);
    } catch (err) {
      next(err);
    }
  };
}
