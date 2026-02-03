import type { RouterContext } from "@koa/router";
import { makeGetUsersService } from "../../../services/factories/make-get-users";

export async function getUsers(ctx: RouterContext) {
  const registerService  = makeGetUsersService()

  try {
    const users = await registerService.execute()

    ctx.status = 200
    ctx.body = {
      users
    }
  } catch(err) {
    throw err
  }
}