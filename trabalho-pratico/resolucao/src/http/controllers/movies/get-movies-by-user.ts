import type { RouterContext } from "@koa/router";
import z from "zod";
import { makeGetMoviesByUserService } from "../../../services/factories/make-get-movies-by-user";
import { UserNotFoundError } from "../../../services/err/user-not-found-error";

export async function getMoviesByUser(ctx: RouterContext) {
  const getMoviesByUserParamsSchema = z.object({
    userId: z.string().uuid()
  })

  const { userId } = getMoviesByUserParamsSchema.parse(ctx.params)
  const getMoviesByUserService = makeGetMoviesByUserService()

  try {
    const movies = await getMoviesByUserService.execute({ userId })

    ctx.status = 200
    ctx.body = {
      movies
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
