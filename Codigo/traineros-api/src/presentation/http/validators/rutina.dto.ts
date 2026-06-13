/** CAPA 1 · Presentación — validación de entrada (DTO) del módulo Rutinas. */
import { z } from 'zod';

export const crearRutinaSchema = z.object({
  alumnoId: z.string().uuid(),
  nombre: z.string().min(1),
  ejercicios: z
    .array(
      z.object({
        ejercicioId: z.string().uuid(),
        series: z.number().int().positive(),
        repeticiones: z.number().int().positive(),
      }),
    )
    .default([]),
});

export type CrearRutinaDTO = z.infer<typeof crearRutinaSchema>;
