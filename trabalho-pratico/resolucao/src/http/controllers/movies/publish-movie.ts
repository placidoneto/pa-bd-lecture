import type { RouterContext } from "@koa/router";
import z from "zod";
import { makePublishMovieService } from "../../../services/factories/make-publish-movie";
import { UserNotFoundError } from "../../../services/err/user-not-found-error";

export async function publishMovie(ctx: RouterContext) {
  const publishMovieSchema = z.object({
    title: z.string().min(1, 'Título é obrigatório'),
    description: z.string().min(1, 'Descrição é obrigatória'),
    releaseDate: z.coerce.date(),
    userId: z.string().uuid()
  })

  const { title, description, releaseDate, userId } = publishMovieSchema.parse(ctx.request.body)
  const publishMovieService = makePublishMovieService()

  try {
    const movie = await publishMovieService.execute({
      title,
      description,
      releaseDate,
      userId
    })

    ctx.status = 201
    ctx.body = {
      message: 'Filme publicado com sucesso',
      movie
    }
  } catch(err) {
    if (err instanceof UserNotFoundError) {
      ctx.status = 404
      ctx.body = {
        message: err.message
      }
      return
    }
    throw err
  }
}
