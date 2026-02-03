import { PrismaUserRepository } from "../../repositories/prisma/prisma-users-repository";
import { RegisterService } from "../register";

export function makeRegisterService() {
  const usersRepository = new PrismaUserRepository
  const registerService = new RegisterService(usersRepository)

  return registerService
}