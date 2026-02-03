import crypto from 'node:crypto'
import type { UsersRepository } from '../repositories/users-repository.js'
import { UserAlreadyExistsError } from './err/user-already-exists-error.js'

interface RegisterServiceRequest {
  name: string
  password: string
  email: string
}

export class RegisterService {
  constructor(private usersRepository: UsersRepository) {}

  async execute({name, password, email}: RegisterServiceRequest) {
    const password_hash = crypto
      .createHash('sha256')
      .update(password)
      .digest('hex')

    const userWithSameEmail = await this.usersRepository.findByEmail(email)

    if (userWithSameEmail) {
      throw new UserAlreadyExistsError()
    }

    await this.usersRepository.create({name, email, password_hash})
  }
}