<?php

namespace App\Services;

use App\Models\Tarefa;
use Illuminate\Database\Eloquent\Collection;

class TarefaService
{
    /**
     * @param array $data Array associativo com os dados (titulo, descricao, etc).
     * @return Tarefa Retorna o objeto da tarefa criada.
     */
    public function create(array $data): Tarefa
    {
        return Tarefa::create($data);
    }

    /**
     * @return Collection Coleção de objetos Tarefa.
     */
    public function list(): Collection
    {
        return Tarefa::all();
    }

    /**
     * @param int $id
     * @return Tarefa|null Retorna a Tarefa ou null se não encontrar.
     */
    public function getOne(int $id): ?Tarefa
    {
        return Tarefa::find($id);
    }

    /**
     * @param int $id ID da tarefa.
     * @param array $data Novos dados.
     * @return Tarefa|null Retorna a tarefa atualizada ou null se não existir.
     */
    public function update(int $id, array $data): ?Tarefa
    {
        $tarefa = Tarefa::find($id);

        if (!$tarefa) {
            return null;
        }

        $tarefa->update($data);
        return $tarefa;
    }

    /**
     * @param int $id
     * @return bool Retorna true se deletou, false se a tarefa não existia.
     */
    public function delete(int $id): bool
    {
        $tarefa = Tarefa::find($id);

        if (!$tarefa) {
            return false;
        }

        return $tarefa->delete();
    }
}