import type { RouterContext } from "@koa/router";
import { makeGetAllMoviesService } from "../../../services/factories/make-get-all-movies";

export async function getAllMovies(ctx: RouterContext) {
  const getAllMoviesService = makeGetAllMoviesService()

  try {
    const movies = await getAllMoviesService.execute()

    ctx.status = 200
    ctx.body = {
      movies
    }
  } catch(err) {
    throw err
  }
}
