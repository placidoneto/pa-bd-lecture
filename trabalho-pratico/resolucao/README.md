# Resolução - API de Gerenciamento de Filmes

## Descrição

Implementação completa da API de gerenciamento de filmes usando Koa, seguindo os requisitos do trabalho prático.

## Estrutura do Projeto

```
src/
├── server.ts
├── http/
│   └── controllers/
│       ├── users/
│       │   ├── register.ts
│       │   ├── get-users.ts
│       │   └── router.ts
│       └── movies/
│           ├── publish-movie.ts
│           ├── get-all-movies.ts
│           ├── get-movies-by-user.ts
│           └── router.ts
├── services/
│   ├── register.ts
│   ├── get-users.ts
│   ├── publish-movie.ts
│   ├── get-all-movies.ts
│   ├── get-movies-by-user.ts
│   ├── factories/
│   └── err/
├── repositories/
│   ├── users-repository.ts
│   ├── movies-repository.ts
│   └── prisma/
└── lib/
    └── prisma.ts
```

## Funcionalidades Implementadas

### Usuários
- ✅ Cadastro de usuários com hash de senha
- ✅ Listagem de usuários
- ✅ Validação de email único

### Filmes
- ✅ Cadastro de filmes vinculados a usuários
- ✅ Listagem de todos os filmes
- ✅ Listagem de filmes por usuário
- ✅ Relacionamento User → Movies

## Como Executar

### 1. Instalar dependências
```bash
npm install
```

### 2. Configurar variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:
```env
DATABASE_URL="postgresql://user:password@localhost:5432/koa_movies"
```

### 3. Executar migrations
```bash
npx prisma migrate dev
```

### 4. Iniciar o servidor
```bash
npm run dev
```

O servidor estará rodando em `http://localhost:3000`

## Usando Docker

```bash
docker-compose up -d
```

## Endpoints

### Usuários

#### Cadastrar Usuário
```http
POST /api/users/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "123456"
}
```

#### Listar Usuários
```http
GET /api/users
```

### Filmes

#### Cadastrar Filme
```http
POST /api/movies
Content-Type: application/json

{
  "title": "Matrix",
  "description": "Um programador descobre a verdade sobre a realidade",
  "releaseDate": "1999-03-31",
  "userId": "uuid-do-usuario"
}
```

#### Listar Todos os Filmes
```http
GET /api/movies
```

#### Listar Filmes por Usuário
```http
GET /api/movies/user/:userId
```

## Testes

Utilize o arquivo `exemples.http` para testar os endpoints.

## Tecnologias

- **Koa** - Framework web minimalista
- **Prisma** - ORM moderno para Node.js
- **PostgreSQL** - Banco de dados relacional
- **TypeScript** - Superset JavaScript com tipagem
- **bcryptjs** - Hash de senhas
- **Zod** - Validação de schemas

## Padrões Utilizados

- **Repository Pattern** - Abstração da camada de dados
- **Service Layer** - Lógica de negócio separada
- **Factory Pattern** - Criação de instâncias de serviços
- **Dependency Injection** - Inversão de dependências

## Tratamento de Erros

Erros personalizados:
- `UserAlreadyExistsError` - Email já cadastrado
- `UserNotFoundError` - Usuário não encontrado
- `MovieNotFoundError` - Filme não encontrado
