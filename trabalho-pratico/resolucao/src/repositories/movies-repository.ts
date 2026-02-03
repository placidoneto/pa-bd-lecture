import type { Prisma, Movie } from "../../generated/prisma/browser"

export interface MoviesRepository {
  findById(id: string): Promise<Movie | null>
  findAll(): Promise<Movie[]>
  findByUserId(userId: string): Promise<Movie[]>
  create(data: Prisma.MovieCreateInput): Promise<Movie>
}
