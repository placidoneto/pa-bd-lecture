<?php

namespace App\Http\Controllers;

use OpenApi\Attributes as OA;

#[OA\Info(
    version: "1.0.0",
    title: "API Laravel - Gestão de Tarefas",
    description: "API RESTful para gerenciar tarefas e usuários"
)]
#[OA\Server(
    url: "http://127.0.0.1:8000/api",
    description: "Servidor de Desenvolvimento"
)]
#[OA\Tag(name: "Tarefas", description: "Operações relacionadas a tarefas")]
#[OA\Tag(name: "Usuários", description: "Operações relacionadas a usuários")]
abstract class Controller
{
    //
}
