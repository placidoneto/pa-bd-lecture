<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\TarefaController;
use App\Http\Controllers\UserController;

Route::get('/tarefas', [TarefaController::class, 'list']);
Route::post('/tarefas', [TarefaController::class, 'create']);
Route::get('/tarefas/{id}', [TarefaController::class, 'get_one']);
Route::put('/tarefas/{id}', [TarefaController::class, 'update']);
Route::delete('/tarefas/{id}', [TarefaController::class, 'destroy']);

Route::get('/usuarios', [UserController::class, 'list']);
Route::post('/usuarios', [UserController::class, 'create']);
Route::get('/usuarios/{id}', [UserController::class, 'get_one']);
Route::put('/usuarios/{id}', [UserController::class, 'update']);
Route::delete('/usuarios/{id}', [UserController::class, 'destroy']);
