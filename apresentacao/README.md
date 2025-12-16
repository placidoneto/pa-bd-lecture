# LARAVEL

## Introdução

Laravel é um framework PHP open-source criado por **Taylor Otwell**, lançado em 2011. Ele foi desenvolvido com o objetivo de tornar o desenvolvimento web mais simples, elegante e produtivo, seguindo o padrão arquitetural **MVC (Model-View-Controller)**.

O Laravel abstrai grande parte da complexidade comum no desenvolvimento web em PHP, oferecendo uma base sólida para construção de **APIs REST**, aplicações web completas e sistemas escaláveis.

Ele é conhecido por sua sintaxe expressiva, forte ecossistema e foco em boas práticas de engenharia de software.

---

## Principais Características

* Estrutura MVC bem definida;
* Roteamento simples e expressivo;
* ORM poderoso (Eloquent);
* Sistema de migrações e versionamento de banco de dados;
* Sistema de autenticação e autorização integrado;
* Suporte nativo a APIs REST e JSON;
* Grande ecossistema de pacotes e comunidade ativa.

---

## Arquitetura em Camadas (Estrutura Padrão do Laravel)

O Laravel **impõe uma estrutura padrão**, o que facilita a manutenção, o trabalho em equipe e a escalabilidade do sistema.

### 1. Routes (Camada de Entrada)

Responsável por:

* Definir endpoints da aplicação;
* Mapear URLs para controllers;
* Aplicar middlewares;
* Separar rotas web e rotas de API.

Normalmente localizadas em:

* ```routes/web.php```
* ```routes/api.php```

Exemplo:

```php
Route::get('/users', [UserController::class, 'index']);
```

---

### 2. Controllers (Controle da Requisição)

Responsável por:

* Receber a requisição HTTP;
* Validar dados de entrada;
* Orquestrar chamadas para services ou models;
* Retornar respostas (JSON ou views).

Controllers mantêm as rotas limpas e centralizam o fluxo da requisição.

---

### 3. Services (Lógica de Negócio)

Embora não seja obrigatório, o uso de **Services** é uma prática comum em projetos Laravel.

Responsável por:

* Implementar regras de negócio;
* Evitar lógica complexa dentro dos controllers;
* Facilitar testes e reutilização de código.

---

### 4. Models (Modelo de Negócio)

Os Models representam as entidades do sistema e utilizam o **Eloquent ORM**.

Responsável por:

* Representar tabelas do banco de dados;
* Definir relacionamentos (1-1, 1-N, N-N);
* Encapsular regras básicas do domínio.

Exemplo:

```php
class User extends Model {
    protected $fillable = ['name', 'email'];
}
```

### 5. Migrations (Estrutura e Versionamento do Banco de Dados)

As Migrations são responsáveis por definir e versionar a estrutura do banco de dados no Laravel.

Diferente de frameworks como o Django, onde o model também descreve o schema do banco, no Laravel existe uma separação clara de responsabilidades:

* Model → representa a entidade e a forma como a aplicação acessa os dados
* Migration → define como o banco de dados é criado e alterado ao longo do tempo

```php
Schema::create('users', function (Blueprint $table) {
    $table->id();
    $table->string('name');
    $table->string('email')->unique();
    $table->timestamps();
});
```

---

### 6. Repository

Em aplicações maiores, é comum utilizar o padrão **Repository** para:

* Isolar o acesso ao banco de dados;
* Evitar dependência direta do ORM;
* Facilitar testes unitários e mudanças de persistência.

---

### 7. DTOs e Requests

O Laravel utiliza **Form Requests** para validação e pode usar **DTOs** para transporte de dados.

Responsável por:

* Validar dados de entrada;
* Padronizar dados trafegados;
* Evitar exposição direta dos models.

---

## Princípios RESTful com Laravel

Laravel é amplamente utilizado para construção de APIs RESTful.

### 1. Recursos e Endpoints

Cada endpoint representa um recurso:

```
GET    /api/users
POST   /api/users
GET    /api/users/{id}
PUT    /api/users/{id}
DELETE /api/users/{id}
```

---

### 2. Uso semântico de métodos HTTP

* **GET** → buscar dados
* **POST** → criar recurso
* **PUT/PATCH** → atualizar
* **DELETE** → remover

---

### 3. Retorno de JSON

Laravel possui suporte nativo a JSON:

```php
return response()->json([
    'message' => 'API funcionando corretamente',
    'status' => 'ok'
], 200);
```

---

### 4. Códigos de Status HTTP

Utilização correta dos códigos:

* 200 → OK
* 201 → Created
* 400 → Bad Request
* 401 → Unauthorized
* 404 → Not Found
* 500 → Internal Server Error

---

### 5. Tratamento de Erros

Laravel possui:

* Exceptions globais;
* Handler centralizado (```app/Exceptions/Handler.php```);
* Respostas automáticas para APIs.

---

## Ecossistema e Ferramentas do Laravel

### Persistência

* Eloquent ORM
* Query Builder

### Migrações

* Migrations
* Seeders
* Factories

### Autenticação e Segurança

* Laravel Breeze
* Laravel Sanctum
* Laravel Passport

### Filas e Assincronismo

* Queues
* Jobs
* Redis

### Testes

* PHPUnit
* Pest

### Outras Ferramentas

* Blade (template engine)
* Artisan CLI
* Scheduler
* Cache e sessões

---

## Comparativo com outros Frameworks PHP

| Framework   | Característica       | Performance | Complexidade | Ideal para                    |
| ----------- | -------------------- | ----------- | ------------ | ----------------------------- |
| **Laravel** | Completo e elegante  | Alta        | Média        | APIs e sistemas robustos      |
| **Symfony** | Extremamente modular | Alta        | Alta         | Grandes projetos corporativos |
| **Slim**    | Microframework       | Muito alta  | Baixa        | APIs simples                  |

---

## Melhores Práticas com Laravel

* Utilizar corretamente MVC;
* Manter controllers enxutos;
* Centralizar regras de negócio em services;
* Utilizar Form Requests para validação;
* Versionar APIs;
* Utilizar migrations e seeders;
* Criar testes automatizados;
* Usar variáveis de ambiente (```.env```);
* Evitar lógica de negócio diretamente nas views ou rotas.
