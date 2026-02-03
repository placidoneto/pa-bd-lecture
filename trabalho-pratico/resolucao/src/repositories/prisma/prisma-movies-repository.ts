import type { Movie } from "../../../generated/prisma/browser";
import type { MovieCreateInput } from "../../../generated/prisma/models";
import type { MoviesRepository } from "../movies-repository";
import { prisma } from '../../lib/prisma'

export class PrismaMoviesRepository implements MoviesRepository {
  async create(data: MovieCreateInput): Promise<Movie> {
    const movie = await prisma.movie.create({ data })
    return movie
  }

  async findById(id: string): Promise<Movie | null> {
    const movie = await prisma.movie.findUnique({ where: { id } })
    return movie
  }

  async findAll(): Promise<Movie[]> {
    const movies = await prisma.movie.findMany()
    return movies
  }

  async findByUserId(userId: string): Promise<Movie[]> {
    const movies = await prisma.movie.findMany({
      where: { userId }
    })
    return movies
  }
}
