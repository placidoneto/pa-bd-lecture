import type { UsersRepository } from "../repositories/users-repository"

export class GetUsersService {
  constructor(private userRepository: UsersRepository) {}

  async execute() {
    const users = await this.userRepository.findAll()

    return users
  }
}