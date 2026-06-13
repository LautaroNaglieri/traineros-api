/** Utilidad transversal — error de aplicación con código HTTP. */
export class AppError extends Error {
  constructor(
    message: string,
    public readonly status: number = 400,
  ) {
    super(message);
    this.name = 'AppError';
  }
}
