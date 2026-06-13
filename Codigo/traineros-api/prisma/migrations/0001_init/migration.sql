-- Migración inicial (esqueleto base). Generada a partir de schema.prisma.
-- Crea las tablas del modelo relacional multitenant. Sin datos ni lógica.

CREATE TABLE "entrenadores" (
    "id" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "nombre" TEXT NOT NULL,
    "creadoEn" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "entrenadores_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "entrenadores_email_key" ON "entrenadores"("email");

CREATE TABLE "alumnos" (
    "id" TEXT NOT NULL,
    "entrenadorId" TEXT NOT NULL,
    "nombre" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    CONSTRAINT "alumnos_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "alumnos_entrenadorId_idx" ON "alumnos"("entrenadorId");

CREATE TABLE "ejercicios" (
    "id" TEXT NOT NULL,
    "nombre" TEXT NOT NULL,
    "grupo" TEXT NOT NULL,
    "videoUrl" TEXT,
    CONSTRAINT "ejercicios_pkey" PRIMARY KEY ("id")
);

CREATE TABLE "rutinas" (
    "id" TEXT NOT NULL,
    "entrenadorId" TEXT NOT NULL,
    "alumnoId" TEXT NOT NULL,
    "nombre" TEXT NOT NULL,
    "creadaEn" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "rutinas_pkey" PRIMARY KEY ("id")
);
CREATE INDEX "rutinas_entrenadorId_idx" ON "rutinas"("entrenadorId");

CREATE TABLE "rutina_ejercicios" (
    "id" TEXT NOT NULL,
    "rutinaId" TEXT NOT NULL,
    "ejercicioId" TEXT NOT NULL,
    "series" INTEGER NOT NULL,
    "repeticiones" INTEGER NOT NULL,
    CONSTRAINT "rutina_ejercicios_pkey" PRIMARY KEY ("id")
);

CREATE TABLE "membresias" (
    "id" TEXT NOT NULL,
    "entrenadorId" TEXT NOT NULL,
    "alumnoId" TEXT NOT NULL,
    "estado" TEXT NOT NULL DEFAULT 'activa',
    "venceEl" TIMESTAMP(3) NOT NULL,
    CONSTRAINT "membresias_pkey" PRIMARY KEY ("id")
);
CREATE UNIQUE INDEX "membresias_alumnoId_key" ON "membresias"("alumnoId");
CREATE INDEX "membresias_entrenadorId_idx" ON "membresias"("entrenadorId");
