/** CAPA 3 · Infraestructura — carga y validación de variables de entorno. */
import { z } from 'zod';

const schema = z.object({
  PORT: z.coerce.number().default(3000),
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  DATABASE_URL: z.string().url(),
  JWT_SECRET: z.string().min(1),
  JWT_EXPIRES_IN: z.string().default('1d'),
});

// En el esqueleto se permite arrancar con defaults; en prod estas variables son obligatorias.
export const env = schema.parse({
  ...process.env,
  DATABASE_URL: process.env.DATABASE_URL ?? 'postgresql://traineros:traineros@localhost:5432/traineros',
  JWT_SECRET: process.env.JWT_SECRET ?? 'dev-secret',
});
