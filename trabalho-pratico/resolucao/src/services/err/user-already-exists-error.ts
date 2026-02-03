export class UserAlreadyExistsError extends Error {
  constructor() {
    super('Esse E-mail já foi cadastrado.')
  }
}