# API Laravel – Gestão de Tarefas

Este repositório contém um **exemplo prático de API REST desenvolvida com Laravel**, com o objetivo de demonstrar a estrutura básica do framework, boas práticas e organização do código.

O tema escolhido é **Gestão de Tarefas**, por ser simples e suficiente para ilustrar conceitos como rotas, controllers, models, migrations e serviços.

---

## 1. Requisitos

- PHP 8.1 ou superior
- Composer

### Baixar e configurar o Composer

1. Abra o PowerShell e rode:

```bash
php -r "copy('https://getcomposer.org/installer', 'composer-setup.php');"
php composer-setup.php
php -r "unlink('composer-setup.php');"
```

2. Mova o Composer para um lugar global e adicione ao path:

```bash
move composer.phar C:\composer\composer.phar
C:\composer (adicionar o diretório no path)
```

---

## 2. Criar o projeto Laravel

```bash
composer create-project laravel/laravel tarefas-api
cd tarefas-api
```

---

## 3. Estrutura básica do projeto

O Laravel já fornece uma estrutura bem definida:

```
tarefas-api/
│── app/
│   ├── Http/
│   │   ├── Controllers/
│   │   │   └── TarefaController.php
│   │   └── Requests/
│   │       └── TarefaRequest.php
│   ├── Models/
│   │   └── Tarefa.php
│   └── Services/
│       └── TarefaService.php
│
│── database/
│   ├── migrations/
│       └── xxxx_xx_xx_create_tarefas_table.php
│
│── routes/
│   └── api.php
│
│── .env
│── artisan
```

### Responsabilidades das camadas

- **Controllers** → Controlam o fluxo da requisição
- **Requests** → Centraliza regras de validações de requisições
- **Models** → Representam as entidades do sistema
- **Services** → Contêm a lógica de negócio
- **Migrations** → Versionam a estrutura do banco de dados
- **Routes** → Definem os endpoints da API

---

## 4. Configurando o ambiente

Clone o arquivo `.env.example` e altere o nome para `.env`

### Banco de dados

Altere os dados com base no seu postgres, configuração padrão:

```env
DB_CONNECTION=postgresql
DB_HOST=127.0.0.1
DB_PORT=5432
DB_DATABASE=laravel
DB_USERNAME=postgres
DB_PASSWORD=postgres
```

### Chave do app

Utilizada para criptografias de sessões, cookies e tokens CSRF. Utilize o seguinte comando para gera-lo:

```bash
php artisan key:generate
```

### Baixar dependencias

```bash
composer install
```

---

## 5. Tabela (Tarefa)

Para criar o model, migration e controller das tarefas, rode na raiz do projeto:

```bash
php artisan make:model Tarefa -cmR
```

Isso cria:

- `app/Models/Tarefa.php`

- `database/migrations/xxxx_create_tarefas_table.php`

- `app/Htpp/Controllers/TarefaController.php`

- `app/Http/Requests/TarefaRequest.php`

### Definição da tabela:

Cole este código no arquivo de migration que foi criado:

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::create('tarefas', function (Blueprint $table) {
            $table->id();
            $table->string('titulo');
            $table->text('descricao')->nullable();
            $table->dateTime('data_conclusao')->nullable()->default(null);
            $table->unsignedBigInteger('usuario_id');
            $table->foreign('usuario_id')->references('id')->on('users')->onDelete('cascade');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('tarefas');
    }
};
```

Execute a migration:

```bash
php artisan migrate
```

---

## 6. Model (Tarefa)

O **Model** representa a entidade do sistema e é responsável pela comunicação com o banco de dados. No Laravel, usamos o **Eloquent ORM** para manipular dados de forma orientada a objetos.

Cole este código no arquivo `app/Models/Tarefa.php` que foi criado:

```php
<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Tarefa extends Model
{
    // Define explicitamente qual tabela do banco este Model representa
    // Convenção Laravel: se omitido, busca por `tarefas` (plural snake_case do nome da classe)
    protected $table = 'tarefas';

    // Define quais campos podem ser preenchidos em massa via create() ou update()
    // Isso protege contra ataques onde usuários tentam modificar campos não autorizados
    protected $fillable = [
        'titulo',
        'descricao',
        "usuario_id"
    ];

    // Converte automaticamente os tipos dos dados ao recuperar do banco
    protected $casts = [
        'data_conclusao' => 'datetime',
        'created_at' => 'datetime',
        'updated_at' => 'datetime'
    ];
}
```

---

## 7. Service (Lógica de Negócio)

A camada de **Service** é responsável por concentrar a **lógica de negócio** da aplicação, mantendo os Controllers mais limpos e focados apenas nas requisições HTTP.

### Criar o Service

- Crie manualmente a pasta `app/Services/`
- Dentro dela, crie o arquivo `TarefaService.php`
- Cole o seguinte código dentro desse arquivo:

```php
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
```

- Crie também o arquivo `UsuarioService.php`
- Cole o seguinte código dentro desse arquivo:

```php
<?php

namespace App\Services;

use App\Models\User;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Support\Facades\Hash;

class UserService
{
    public function list(): Collection
    {
        return User::all();
    }

    public function create(array $data): User
    {
        $data['password'] = Hash::make($data['password']);

        return User::create($data);
    }

    public function getOne(int $id): ?User
    {
        return User::find($id);
    }

    public function update(int $id, array $data): ?User
    {
        $user = User::find($id);

        if (!$user) {
            return null;
        }

        if (isset($data['password'])) {
            $data['password'] = Hash::make($data['password']);
        }

        $user->update($data);
        return $user;
    }

    public function delete(int $id): bool
    {
        $user = User::find($id);

        if (!$user) {
            return false;
        }

        return $user->delete();
    }
}
```

---

## 8. Controller (Controlador de Requisições HTTP)

O **Controller** é responsável por **receber requisições HTTP**, processá-las e retornar respostas. Ele funciona como intermediário entre as rotas e a lógica de negócio.

Cole este código no arquivo `app/Http/Controllers/TarefaController.php` que foi gerado:

```php
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

```

- Crie o controller do Usuario:

```bash
php artisan make:controller UserController --api --requests
```

- Cole este código no arquivo `app/Http/Controllers/UserController.php` que foi gerado:

```php
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

```

---

## 9. Form Request (Validação de Dados)

O **Form Request** é uma classe especializada que centraliza as **regras de validação** e **autorização** de requisições HTTP. Ele mantém o Controller limpo e facilita a reutilização de regras.

Cole este código no arquivo `app/Http/Requests/TarefaRequest.php` que foi gerado:

```php
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
        ];
    }
}

```

- Crie o request do Usuario:

```bash
php artisan make:request UserRequest
```

Cole este código no arquivo `app/Http/Controllers/UserRequest.php` que foi gerado:

```php
<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class UserRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true;
    }

    /**
     * Get the validation rules that apply to the request.
     *
     * @return array<string, \Illuminate\Contracts\Validation\ValidationRule|array<mixed>|string>
     */
    public function rules(): array
    {
        $userId = $this->route('id');

        return [
            'name' => 'required|string|max:255',
            'email' => 'required|email|max:255',
            'password' => 'required|string|max:32',
        ];
    }

    public function messages(): array
    {
        return [
            'name.required' => 'O nome é obrigatório',
            'email.required' => 'O email é obrigatório',
            'email.email' => 'Email inválido',
            'email.unique' => 'Este email já está em uso',
            'password.required' => 'A senha é obrigatória'
        ];
    }
}

```

---

## 10. Rotas da API

As **rotas** definem os **endpoints** da sua API e mapeiam URLs para métodos dos Controllers.

Cole este código no arquivo `routes/api.php`:

```php
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

```

---

## 11. Documentação

- Edite o arquivo `app/Http/Controllers/Controller.php`:

```php
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

```

- Utilize o comando:

```bash
php artisan l5-swagger:generate
```

---

## 12. Executar a aplicação

```bash
php artisan serve
```

A API ficará disponível em:

```
http://127.0.0.1:8000/api
```

Acesse a documentação com swagger em:

```
http://127.0.0.1:8000/api/documentation
```
