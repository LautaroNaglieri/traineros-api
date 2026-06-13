/** CAPA 3 · Infraestructura — instancia única del cliente Prisma (ORM). */
import { PrismaClient } from '@prisma/client';

export const prisma = new PrismaClient();
