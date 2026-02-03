import { PrismaMoviesRepository } from "../../repositories/prisma/prisma-movies-repository"
import { PrismaUsersRepository } from "../../repositories/prisma/prisma-users-repository"
import { PublishMovieService } from "../publish-movie"

export function makePublishMovieService() {
  const moviesRepository = new PrismaMoviesRepository()
  const usersRepository = new PrismaUsersRepository()
  const publishMovieService = new PublishMovieService(moviesRepository, usersRepository)

  return publishMovieService
}
