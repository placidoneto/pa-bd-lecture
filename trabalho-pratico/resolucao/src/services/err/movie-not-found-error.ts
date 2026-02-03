export class MovieNotFoundError extends Error {
  constructor() {
    super('Filme não encontrado.')
  }
}
