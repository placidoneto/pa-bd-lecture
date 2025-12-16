<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Http\Requests\TarefaRequest;
use App\Services\TarefaService;
use Illuminate\Http\JsonResponse;
use OpenApi\Attributes as OA;

/**
 * Controlador responsável por gerenciar as requisições HTTP relacionadas a Tarefas
 */
class TarefaController extends Controller
{
    // Propriedade para armazenar a instância do serviço de tarefas
    protected $tarefaService;


    /**
     * Construtor do Controller
     * @param TarefaService $tarefaService
    */
    public function __construct(TarefaService $tarefaService)
    {
        $this->tarefaService = $tarefaService;
    }

    #[OA\Get(
        path: "/tarefas",
        operationId: "getTarefasList",
        tags: ["Tarefas"],
        summary: "Lista todas as tarefas",
        responses: [
            new OA\Response(response: 200, description: "Lista de tarefas retornada com sucesso")
        ]
    )]
    public function list(): JsonResponse
    {
        $tarefas = $this->tarefaService->list();
        return response()->json($tarefas);
    }

    #[OA\Post(
        path: "/tarefas",
        operationId: "createTarefa",
        tags: ["Tarefas"],
        summary: "Cria uma nova tarefa",
        responses: [
            new OA\Response(response: 201, description: "Tarefa criada com sucesso"),
            new OA\Response(response: 422, description: "Erro de validação")
        ]
    )]
    public function create(TarefaRequest $request): JsonResponse
    {
        // O método validated() garante que só passamos dados que passaram nas regras do Request
        $tarefa = $this->tarefaService->create($request->validated());

        return response()->json($tarefa, 201);
    }

    #[OA\Get(
        path: "/tarefas/{id}",
        operationId: "getTarefaById",
        tags: ["Tarefas"],
        summary: "Busca uma tarefa específica",
        parameters: [
            new OA\Parameter(name: "id", in: "path", required: true, schema: new OA\Schema(type: "integer"))
        ],
        responses: [
            new OA\Response(response: 200, description: "Tarefa encontrada"),
            new OA\Response(response: 404, description: "Tarefa não encontrada")
        ]
    )]
    public function get_one(int $id): JsonResponse
    {
        $tarefa = $this->tarefaService->getOne($id);

        if (!$tarefa) {
            return response()->json(['message' => 'Tarefa não encontrada'], 404);
        }

        return response()->json($tarefa);
    }

    #[OA\Put(
        path: "/tarefas/{id}",
        operationId: "updateTarefa",
        tags: ["Tarefas"],
        summary: "Atualiza uma tarefa",
        parameters: [
            new OA\Parameter(name: "id", in: "path", required: true, schema: new OA\Schema(type: "integer"))
        ],
        responses: [
            new OA\Response(response: 200, description: "Tarefa atualizada com sucesso"),
            new OA\Response(response: 404, description: "Tarefa não encontrada")
        ]
    )]
    public function update(TarefaRequest $request, int $id): JsonResponse
    {
        $tarefa = $this->tarefaService->update($id, $request->validated());

        if (!$tarefa) {
            return response()->json(['message' => 'Tarefa não encontrada'], 404);
        }

        return response()->json($tarefa);
    }

    #[OA\Delete(
        path: "/tarefas/{id}",
        operationId: "deleteTarefa",
        tags: ["Tarefas"],
        summary: "Remove uma tarefa",
        parameters: [
            new OA\Parameter(name: "id", in: "path", required: true, schema: new OA\Schema(type: "integer"))
        ],
        responses: [
            new OA\Response(response: 204, description: "Tarefa deletada com sucesso"),
            new OA\Response(response: 404, description: "Tarefa não encontrada")
        ]
    )]
    public function destroy(int $id): JsonResponse
    {
        $deleted = $this->tarefaService->delete($id);

        if (!$deleted) {
            return response()->json(['message' => 'Tarefa não encontrada'], 404);
        }

        return response()->json(['message' => 'Tarefa deletada com sucesso']);
    }
}
