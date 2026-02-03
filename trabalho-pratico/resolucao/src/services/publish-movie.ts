import type { MoviesRepository } from "../repositories/movies-repository"
import type { UsersRepository } from "../repositories/users-repository"
import { UserNotFoundError } from "./err/user-not-found-error"

interface PublishMovieServiceRequest {
  title: string
  description: string
  releaseDate: Date
  userId: string
}

export class PublishMovieService {
  constructor(
    private moviesRepository: MoviesRepository,
    private usersRepository: UsersRepository
  ) {}

  async execute({ title, description, releaseDate, userId }: PublishMovieServiceRequest) {
    const user = await this.usersRepository.findById(userId)

    if (!user) {
      throw new UserNotFoundError()
    }

    const movie = await this.moviesRepository.create({
      title,
      description,
      releaseDate,
      user: {
        connect: {
          id: userId
        }
      }
    })

    return movie
  }
}
