import type { RouterContext } from "@koa/router";
import z from "zod";
import { makeRegisterService } from "../../../services/factories/make-register-service";
import { UserAlreadyExistsError } from "../../../services/err/user-already-exists-error";

export async function register(ctx: RouterContext) {
  const registerSchema = z.object({
    name: z.string().min(3, 'Nome de usuário precisa ter no mínimo 3 caracteres'),
    password: z.string().min(3, 'A senha precisa ter no mínimo 3 caracteres'),
    email: z.email()
  })

  const { name, password, email} = registerSchema.parse(ctx.request.body)
  const registerService  = makeRegisterService()

  try {
    await registerService.execute({ email, name, password })

    ctx.status = 201
    ctx.body = {
      message: 'Usuário criado com sucesso'
    }
  } catch(err) {
    if(err instanceof UserAlreadyExistsError) {
      ctx.throw(409, err.message)
    }

    throw err
  }
}