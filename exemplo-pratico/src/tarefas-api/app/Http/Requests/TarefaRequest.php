<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class TarefaRequest extends FormRequest
{
    /**
     * Determina se o usuário está autorizado a fazer essa requisição
     * Retorna true pois é uma API pública por enquanto
     */
    public function authorize(): bool
    {
        return true;
    }

    /**
     * Regras de validação para os dados da Tarefa
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        return [
            'titulo' => 'required|string|max:255',
            'descricao' => 'nullable|string',
            'usuario_id' => 'required|integer|exists:users,id',
        ];
    }
}
