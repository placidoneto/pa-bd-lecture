import { PrismaMoviesRepository } from "../../repositories/prisma/prisma-movies-repository"
import { PrismaUsersRepository } from "../../repositories/prisma/prisma-users-repository"
import { GetMoviesByUserService } from "../get-movies-by-user"

export function makeGetMoviesByUserService() {
  const moviesRepository = new PrismaMoviesRepository()
  const usersRepository = new PrismaUsersRepository()
  const getMoviesByUserService = new GetMoviesByUserService(moviesRepository, usersRepository)

  return getMoviesByUserService
}
