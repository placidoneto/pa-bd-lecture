import type { Prisma, User } from "../../generated/prisma/browser"

export interface UsersRepository {
  findById(id: string): Promise<User | null>
  findByEmail(email: string): Promise<User | null>
  findAll(): Promise<User[]>
  create(data: Prisma.UserCreateInput): Promise<User>
}