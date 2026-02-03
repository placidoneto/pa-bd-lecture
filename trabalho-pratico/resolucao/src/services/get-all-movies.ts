import type { MoviesRepository } from "../repositories/movies-repository"

export class GetAllMoviesService {
  constructor(private moviesRepository: MoviesRepository) {}

  async execute() {
    const movies = await this.moviesRepository.findAll()

    return movies
  }
}
