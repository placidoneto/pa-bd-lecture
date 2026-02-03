export class UserNotFoundError extends Error {
  constructor() {
    super('Usuário não encontrado.')
  }
}
