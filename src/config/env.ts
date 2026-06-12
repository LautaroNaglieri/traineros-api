import 'dotenv/config';
import { z } from 'zod';

/**
 * Validación de variables de entorno con Zod.
 * Falla rápido (fail-fast) al arrancar si falta o es inválida alguna variable.
 */
const envSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  PORT: z.coerce.number().int().positive().default(3000),
  // Conexión a PostgreSQL gestionado (Neon / Railway). Se usará en la capa de datos (Prisma).
  DATABASE_URL: z.string().url().optional(),
  // Secreto para firmar/verificar JWT. El middleware de auth se implementa en fases posteriores.
  JWT_SECRET: z.string().min(1).optional(),
});

const parsed = envSchema.safeParse(process.env);

if (!parsed.success) {
  console.error('Variables de entorno inválidas:', parsed.error.flatten().fieldErrors);
  process.exit(1);
}

export const env = parsed.data;
