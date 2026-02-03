import type { User } from "../../../generated/prisma/browser";
import type { UserCreateInput } from "../../../generated/prisma/models";
import type { UsersRepository } from "../users-repository";
import { prisma } from '../../lib/prisma'

export class PrismaUserRepository implements UsersRepository {
  async create(data: UserCreateInput): Promise<User> {
    const user = await prisma.user.create({ data })
    return user
  }

  async findById(id: string): Promise<User | null> {
    const user = await prisma.user.findUnique({ where: { id } })
    return user
  }

  async findByEmail(email: string): Promise<User | null> {
    const user = await prisma.user.findUnique({ where: { email } })
    return user
  }

  async findAll(): Promise<User[]> {
    const users = await prisma.user.findMany()

    return users
  }
}