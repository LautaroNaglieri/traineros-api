/**
 * NÚCLEO · Dominio — PUERTO de persistencia (interfaz).
 * La capa de aplicación depende de esta abstracción. La capa de infraestructura
 * la implementa con Prisma. Así el negocio no conoce la tecnología de datos.
 */
import { Rutina } from '../entities/rutina.entity';

export interface RutinaRepository {
  findByEntrenador(entrenadorId: string): Promise<Rutina[]>;
  save(rutina: Rutina): Promise<Rutina>;
}
