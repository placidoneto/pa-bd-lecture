import Router from '@koa/router'
import { register } from './register'
import { getUsers } from './get-users'

export const usersRouter = new Router()
usersRouter.post('/users', register)
usersRouter.get('/users', getUsers)