import { PrismaUserRepository } from "../../repositories/prisma/prisma-users-repository"
import { GetUsersService } from "../get-users"

export function makeGetUsersService() {
  const usersRepository = new PrismaUserRepository()
  const getUsersService = new GetUsersService(usersRepository)

  return getUsersService
}