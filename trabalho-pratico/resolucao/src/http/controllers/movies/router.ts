import Router from '@koa/router'
import { getAllMovies } from './get-all-movies'
import { publishMovie } from './publish-movie'
import { getMoviesByUser } from './get-movies-by-user'

export const moviesRouter = new Router()
moviesRouter.get('/movies', getAllMovies)
moviesRouter.post('/movies', publishMovie)
moviesRouter.get('/movies/user/:userId', getMoviesByUser)
