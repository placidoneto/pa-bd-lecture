import type { MoviesRepository } from "../repositories/movies-repository"
import type { UsersRepository } from "../repositories/users-repository"
import { UserNotFoundError } from "./err/user-not-found-error"

interface GetMoviesByUserServiceRequest {
  userId: string
}

export class GetMoviesByUserService {
  constructor(
    private moviesRepository: MoviesRepository,
    private usersRepository: UsersRepository
  ) {}

  async execute({ userId }: GetMoviesByUserServiceRequest) {
    const user = await this.usersRepository.findById(userId)

    if (!user) {
      throw new UserNotFoundError()
    }

    const movies = await this.moviesRepository.findByUserId(userId)

    return movies
  }
}
