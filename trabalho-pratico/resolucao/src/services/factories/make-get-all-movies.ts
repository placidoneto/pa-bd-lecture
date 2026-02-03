import { PrismaMoviesRepository } from "../../repositories/prisma/prisma-movies-repository"
import { GetAllMoviesService } from "../get-all-movies"

export function makeGetAllMoviesService() {
  const moviesRepository = new PrismaMoviesRepository()
  const getAllMoviesService = new GetAllMoviesService(moviesRepository)

  return getAllMoviesService
}
