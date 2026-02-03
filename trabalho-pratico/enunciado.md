# Trabalho Prático - API de Gerenciamento de Filmes

## Contexto

Você foi contratado por uma startup de streaming de vídeos para desenvolver o backend de sua plataforma. A primeira fase do projeto consiste em criar uma API REST que permita o gerenciamento de um catálogo de filmes, onde usuários cadastrados podem adicionar, visualizar e gerenciar filmes.

O time de frontend já está aguardando os endpoints para começar a integração, e você precisa entregar uma API funcional, bem estruturada e documentada.

## Objetivo do trabalho

Implementar uma API REST completa usando o framework **Koa**, aplicando os conceitos aprendidos na apresentação teórica e observados no exemplo prático. O projeto deve demonstrar sua capacidade de:

- Construir endpoints RESTful seguindo boas práticas
- Modelar dados relacionais corretamente
- Implementar operações CRUD completas
- Organizar código em camadas (controllers, services, repositories)
- Tratar erros de forma adequada
- Validar dados de entrada
- Documentar a API de forma clara

## Requisitos funcionais

### Parte 1: Gerenciamento de Usuários (Base fornecida)

Você pode usar o código do exemplo prático como ponto de partida. As funcionalidades de usuários já implementadas são:

- ✅ **Cadastrar usuário**: `POST /api/users/register`
- ✅ **Listar usuários**: `GET /api/users`

### Parte 2: Gerenciamento de Filmes (A ser implementado)

Você deve implementar as seguintes funcionalidades:

#### 2.1. Cadastrar filme

- **Endpoint**: `POST /api/movies`
- **Descrição**: Cadastra um novo filme vinculado a um usuário
- **Validações**:
  - Título é obrigatório (mínimo 1 caractere)
  - Descrição é obrigatória
  - Data de lançamento é obrigatória e deve ser uma data válida
  - ID do usuário é obrigatório e deve existir no banco

#### 2.2. Listar todos os filmes

- **Endpoint**: `GET /api/movies`
- **Descrição**: Retorna todos os filmes cadastrados
- **Informações**: Incluir dados do usuário que cadastrou cada filme

#### 2.3. Listar filmes por usuário

- **Endpoint**: `GET /api/movies/user/:userId`
- **Descrição**: Retorna todos os filmes cadastrados por um usuário específico
- **Validações**: Retornar erro 404 se o usuário não existir

#### 2.4. Buscar filme por ID

- **Endpoint**: `GET /api/movies/:id`
- **Descrição**: Retorna os detalhes de um filme específico
- **Informações**: Incluir dados do usuário que cadastrou
- **Validações**: Retornar erro 404 se o filme não existir

#### 2.5. Atualizar filme

- **Endpoint**: `PUT /api/movies/:id`
- **Descrição**: Atualiza informações de um filme existente
- **Regras**: Apenas título, descrição e data de lançamento podem ser atualizados
- **Validações**:
  - Filme deve existir
  - Mesmas validações do cadastro

#### 2.6. Deletar filme

- **Endpoint**: `DELETE /api/movies/:id`
- **Descrição**: Remove um filme do sistema
- **Validações**: Retornar erro 404 se o filme não existir

## Modelo de dados

### Entidade User (Já existe)

```typescript
{
  id: string          // UUID gerado automaticamente
  name: string        // Nome do usuário
  email: string       // Email único
  password_hash: string // Senha criptografada
  created_at: DateTime // Data de criação
  movies: Movie[]     // Relacionamento com filmes
}
```

### Entidade Movie (A ser criada)

```typescript
{
  id: string          // UUID gerado automaticamente
  title: string       // Título do filme
  description: string // Sinopse/descrição
  releaseDate: DateTime // Data de lançamento
  userId: string      // ID do usuário que cadastrou (FK)
  user: User          // Relacionamento com usuário
  created_at: DateTime // Data de cadastro no sistema
}
```

## Estrutura esperada

Siga a mesma arquitetura do exemplo prático:

```
src/
├── server.ts
├── http/
│   └── controllers/
│       ├── users/
│       │   ├── register.ts
│       │   ├── get-users.ts
│       │   └── router.ts
│       └── movies/              # VOCÊ DEVE CRIAR
│           ├── publish-movie.ts
│           ├── get-all-movies.ts
│           ├── get-movies-by-user.ts
│           └── router.ts
├── services/
│   ├── users/...
│   └── movies/                  # VOCÊ DEVE CRIAR
│       ├── publish-movie.ts
│       ├── get-all-movies.ts
│       ├── get-movies-by-user.ts
│       ├── err/
│       │   └── movie-not-found-error.ts
│       └── factories/
├── repositories/
│   ├── users-repository.ts
│   ├── movies-repository.ts     # VOCÊ DEVE CRIAR
│   └── prisma/
│       ├── prisma-users-repository.ts
│       └── prisma-movies-repository.ts # VOCÊ DEVE CRIAR
└── lib/
    └── prisma.ts
```

## Exemplos de requisições e respostas

### Cadastrar filme

**Requisição**:
```http
POST /api/movies
Content-Type: application/json

{
  "title": "Matrix",
  "description": "Um programador descobre que a realidade é uma simulação",
  "releaseDate": "1999-03-31",
  "userId": "uuid-do-usuario"
}
```

**Resposta (201)**:
```json
{
  "movie": {
    "id": "uuid-gerado",
    "title": "Matrix",
    "description": "Um programador descobre que a realidade é uma simulação",
    "releaseDate": "1999-03-31T00:00:00.000Z",
    "userId": "uuid-do-usuario",
    "created_at": "2026-02-02T15:00:00.000Z"
  }
}
```

### Listar filmes por usuário

**Requisição**:
```http
GET /api/movies/user/uuid-do-usuario
```

**Resposta (200)**:
```json
{
  "movies": [
    {
      "id": "uuid-1",
      "title": "Matrix",
      "description": "Um programador descobre que a realidade é uma simulação",
      "releaseDate": "1999-03-31T00:00:00.000Z",
      "created_at": "2026-02-02T15:00:00.000Z"
    },
    {
      "id": "uuid-2",
      "title": "Inception",
      "description": "Ladrões invadem sonhos para roubar segredos",
      "releaseDate": "2010-07-16T00:00:00.000Z",
      "created_at": "2026-02-02T16:00:00.000Z"
    }
  ]
}
```

## Passos para implementação

### 1. Atualizar o schema do Prisma

Adicione o modelo `Movie` ao arquivo `prisma/schema.prisma` e crie a migration:

```bash
npx prisma migrate dev --name add_movies_table
```

### 2. Criar os repositories

Defina a interface `MoviesRepository` e implemente `PrismaMoviesRepository`.

### 3. Criar os services

Implemente a lógica de negócio para cada operação (cadastrar, listar, buscar, atualizar, deletar).

### 4. Criar os controllers

Crie os controllers que recebem as requisições HTTP e chamam os services apropriados.

### 5. Configurar as rotas

Adicione as rotas de filmes ao router e registre no servidor.

### 6. Testar

Crie um arquivo `exemples.http` com exemplos de todas as requisições.
