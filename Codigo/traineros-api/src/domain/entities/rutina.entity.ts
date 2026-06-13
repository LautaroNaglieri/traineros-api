/**
 * NÚCLEO · Dominio — entidad de negocio pura.
 * No depende de Prisma ni de Express: es el modelo que la lógica manipula.
 */
export interface RutinaEjercicio {
  ejercicioId: string;
  series: number;
  repeticiones: number;
}

export interface Rutina {
  id: string;
  entrenadorId: string;
  alumnoId: string;
  nombre: string;
  ejercicios: RutinaEjercicio[];
  creadaEn: Date;
}
