import 'dotenv/config'
import Koa from 'koa'
import bodyParser from '@koa/bodyparser'
import Router from '@koa/router'
import { usersRouter } from './http/controllers/users/router'
import { moviesRouter } from './http/controllers/movies/router'

const app = new Koa()
const router = new Router({ prefix: '/api' })

app.use(bodyParser())

router.use(usersRouter.routes())
router.use(moviesRouter.routes())
app.use(router.routes())
app.use(router.allowedMethods())

app.listen('3000', () => {
  console.log('Servidor rodando na porta 3000')
})
