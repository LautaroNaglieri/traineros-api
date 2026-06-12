import express, { type Application } from 'express';

/**
 * Construye la aplicación Express (monolito modular).
 *
 * Los módulos de negocio (Auth, Rutinas, Catálogo, Pagos) se montarán aquí
 * a medida que avancen las fases. En el MVP esqueleto solo se configura el
 * núcleo HTTP; todavía sin lógica de negocio.
 */
export function createApp(): Application {
  const app = express();

  // Middlewares base
  app.use(express.json());
  app.use(express.urlencoded({ extended: true }));

  // TODO(fase-1): montar routers de módulos
  //   app.use('/api/auth', authRouter);
  //   app.use('/api/rutinas', rutinasRouter);
  //   app.use('/api/catalogo', catalogoRouter);
  //   app.use('/api/pagos', pagosRouter);

  return app;
}
