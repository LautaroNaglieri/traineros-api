/**
 * Punto de entrada (composition root).
 * Aquí se "cablean" las capas: la infraestructura concreta (repositorios Prisma)
 * se inyecta en la capa de aplicación, y la aplicación se expone vía la capa
 * de presentación (Express). Es el ÚNICO lugar que conoce a todas las capas.
 */
import { env } from '@infrastructure/config/env';
import { logger } from '@shared/logger';
import { prisma } from '@infrastructure/database/prisma/client';
import { RutinaPrismaRepository } from '@infrastructure/database/repositories/rutina.prisma.repository';
import { RutinasService } from '@application/rutinas/rutinas.service';
import { buildServer } from '@presentation/http/server';

async function bootstrap(): Promise<void> {
  // Capa de Datos -> Capa de Aplicación (inyección de dependencias)
  const rutinaRepository = new RutinaPrismaRepository(prisma);
  const rutinasService = new RutinasService(rutinaRepository);

  // Capa de Aplicación -> Capa de Presentación
  const app = buildServer({ rutinasService });

  app.listen(env.PORT, () => {
    logger.info(`TrainerOS API escuchando en http://localhost:${env.PORT}`);
  });
}

bootstrap().catch((err) => {
  logger.error('Fallo al iniciar la API', err);
  process.exit(1);
});
