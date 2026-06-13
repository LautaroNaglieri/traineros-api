/**
 * CAPA 3 · Infraestructura — implementación Prisma del puerto RutinaRepository.
 * Traduce entre el modelo de la base (Prisma) y la entidad de dominio.
 * Esqueleto: el contrato está implementado; el mapeo fino se completa luego.
 */
import { PrismaClient } from '@prisma/client';
import { Rutina } from '@domain/entities/rutina.entity';
import { RutinaRepository } from '@domain/repositories/rutina.repository';

export class RutinaPrismaRepository implements RutinaRepository {
  constructor(private readonly prisma: PrismaClient) {}

  async findByEntrenador(entrenadorId: string): Promise<Rutina[]> {
    const filas = await this.prisma.rutina.findMany({
      where: { entrenadorId },
      include: { ejercicios: true },
    });
    return filas.map((f) => ({
      id: f.id,
      entrenadorId: f.entrenadorId,
      alumnoId: f.alumnoId,
      nombre: f.nombre,
      creadaEn: f.creadaEn,
      ejercicios: f.ejercicios.map((e) => ({
        ejercicioId: e.ejercicioId,
        series: e.series,
        repeticiones: e.repeticiones,
      })),
    }));
  }

  async save(_rutina: Rutina): Promise<Rutina> {
    // TODO (post-esqueleto): persistir la rutina y sus ejercicios.
    throw new Error('No implementado en el esqueleto');
  }
}
