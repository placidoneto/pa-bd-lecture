<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Http\Requests\UserRequest;
use App\Services\UserService;
use Illuminate\Http\JsonResponse;
use OpenApi\Attributes as OA;

/**
 * Controlador responsável por gerenciar as requisições HTTP relacionadas a Usuários
 */
class UserController extends Controller
{
    protected $userService;

    /**
     * Construtor do Controller
     * @param UserService $userService
     */
    public function __construct(UserService $userService)
    {
        $this->userService = $userService;
    }

    #[OA\Get(
        path: "/usuarios",
        operationId: "getUsersList",
        tags: ["Usuários"],
        summary: "Lista todos os usuários",
        responses: [
            new OA\Response(response: 200, description: "Lista de usuários")
        ]
    )]
    public function list(): JsonResponse
    {
        $usuarios = $this->userService->list();
        return response()->json($usuarios);
    }

    #[OA\Post(
        path: "/usuarios",
        operationId: "createUser",
        tags: ["Usuários"],
        summary: "Cria um novo usuário",
        responses: [
            new OA\Response(response: 201, description: "Usuário criado com sucesso"),
            new OA\Response(response: 422, description: "Erro de validação")
        ]
    )]
    public function create(UserRequest $request): JsonResponse
    {
        $usuario = $this->userService->create($request->validated());
        return response()->json($usuario, 201);
    }

    #[OA\Get(
        path: "/usuarios/{id}",
        operationId: "getUserById",
        tags: ["Usuários"],
        summary: "Busca um usuário específico",
        parameters: [
            new OA\Parameter(name: "id", in: "path", required: true, schema: new OA\Schema(type: "integer"))
        ],
        responses: [
            new OA\Response(response: 200, description: "Usuário encontrado"),
            new OA\Response(response: 404, description: "Usuário não encontrado")
        ]
    )]
    public function get_one(int $id): JsonResponse
    {
        $usuario = $this->userService->getOne($id);

        if (!$usuario) {
            return response()->json(['message' => 'Usuario não encontrado'], 404);
        }

        return response()->json($usuario);
    }

    #[OA\Put(
        path: "/usuarios/{id}",
        operationId: "updateUser",
        tags: ["Usuários"],
        summary: "Atualiza um usuário",
        parameters: [
            new OA\Parameter(name: "id", in: "path", required: true, schema: new OA\Schema(type: "integer"))
        ],
        responses: [
            new OA\Response(response: 200, description: "Usuário atualizado"),
            new OA\Response(response: 404, description: "Usuário não encontrado")
        ]
    )]
    public function update(UserRequest $request, int $id): JsonResponse
    {
        $usuario = $this->userService->update($id, $request->validated());

        if (!$usuario) {
            return response()->json(['message' => 'Usuario não encontrado'], 404);
        }

        return response()->json($usuario);
    }

    #[OA\Delete(
        path: "/usuarios/{id}",
        operationId: "deleteUser",
        tags: ["Usuários"],
        summary: "Remove um usuário",
        parameters: [
            new OA\Parameter(name: "id", in: "path", required: true, schema: new OA\Schema(type: "integer"))
        ],
        responses: [
            new OA\Response(response: 204, description: "Usuário deletado"),
            new OA\Response(response: 404, description: "Usuário não encontrado")
        ]
    )]
    public function destroy(int $id): JsonResponse
    {
        $deleted = $this->userService->delete($id);

        if (!$deleted) {
            return response()->json(['message' => 'Usuario não encontrado'], 404);
        }

        return response()->json(['message' => 'Usuario deletado com sucesso']);
    }
}
