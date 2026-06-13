/**
 * CAPA 2 · Aplicación — caso de uso del módulo Rutinas.
 * Depende de la INTERFAZ del repositorio (puerto del dominio), nunca de Prisma.
 * Esqueleto: la firma y el cableado están; la lógica de negocio se implementa
 * después (la consigna de Fase 1 pide solo el esqueleto).
 */
import { Rutina } from '@domain/entities/rutina.entity';
import { RutinaRepository } from '@domain/repositories/rutina.repository';
import { CrearRutinaDTO } from '@presentation/http/validators/rutina.dto';

export class RutinasService {
  constructor(private readonly repo: RutinaRepository) {}

  async listarPorEntrenador(trainerId: string): Promise<Rutina[]> {
    // El trainerId acota la consulta al tenant (aislamiento multitenant).
    return this.repo.findByEntrenador(trainerId);
  }

  async crear(trainerId: string, _datos: CrearRutinaDTO): Promise<Rutina> {
    // TODO (post-esqueleto): validar reglas de negocio y persistir.
    throw new Error('No implementado: lógica de negocio fuera del alcance del esqueleto');
  }
}
