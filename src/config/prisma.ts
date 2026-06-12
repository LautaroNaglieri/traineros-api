import { PrismaClient } from '@prisma/client';

/**
 * Cliente Prisma único (singleton) para toda la app.
 *
 * En desarrollo se reutiliza la misma instancia entre recargas de `tsx watch`
 * para no agotar el pool de conexiones.
 */
const globalForPrisma = globalThis as unknown as { prisma?: PrismaClient };

export const prisma = globalForPrisma.prisma ?? new PrismaClient();

if (process.env.NODE_ENV !== 'production') {
  globalForPrisma.prisma = prisma;
}
