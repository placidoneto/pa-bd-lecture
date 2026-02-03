# Exemplo Prático - API de Usuários com Koa

## Introdução

Este projeto demonstra a construção de uma API REST utilizando o framework **Koa** para Node.js. O objetivo é apresentar na prática os conceitos fundamentais do framework, através de uma aplicação funcional de gerenciamento de usuários.

Diferente de um tutorial básico "Hello World", este exemplo implementa uma arquitetura completa com separação de responsabilidades, integração com banco de dados e boas práticas de desenvolvimento, servindo como base sólida para projetos reais.

## O que este exemplo ensina

### Conceitos do Koa

- **Servidor HTTP básico**: criação e configuração da aplicação Koa
- **Middlewares em cascata**: como o fluxo bidirecional funciona na prática
- **Contexto (ctx)**: manipulação de requisições e respostas
- **Roteamento**: organização de endpoints com @koa/router
- **Tratamento de erros**: captura e resposta de erros HTTP

### Arquitetura e organização

- **Controllers**: camada de entrada que recebe requisições HTTP
- **Services**: lógica de negócio e regras da aplicação
- **Repositories**: abstração de acesso aos dados
- **Factories**: padrão para criação de instâncias com dependências

### Integração com tecnologias

- **Prisma ORM**: modelagem e acesso ao banco de dados
- **TypeScript**: tipagem estática para maior segurança
- **PostgreSQL**: banco de dados relacional
- **Docker**: containerização do banco de dados

## Arquitetura do projeto

O projeto segue uma arquitetura em camadas, onde cada camada tem uma responsabilidade bem definida:

```
src/
├── server.ts                           # Ponto de entrada da aplicação
├── http/
│   └── controllers/
│       └── users/
│           ├── register.ts             # Controller de cadastro
│           ├── get-users.ts            # Controller de listagem
│           └── router.ts               # Definição das rotas
├── services/
│   ├── register.ts                     # Lógica de cadastro
│   ├── get-users.ts                    # Lógica de listagem
│   ├── err/
│   │   ├── user-already-exists-error.ts
│   │   └── user-not-found-error.ts
│   └── factories/
│       ├── make-register-service.ts
│       └── make-get-users.ts
├── repositories/
│   ├── users-repository.ts             # Interface do repositório
│   └── prisma/
│       └── prisma-users-repository.ts  # Implementação com Prisma
└── lib/
    └── prisma.ts                       # Cliente Prisma
```

### Fluxo de uma requisição

```
1. Requisição HTTP chega ao servidor Koa
   ↓
2. Passa pelos middlewares (bodyParser, etc)
   ↓
3. Router direciona para o controller correto
   ↓
4. Controller chama o service apropriado
   ↓
5. Service executa lógica de negócio
   ↓
6. Service usa repository para acessar dados
   ↓
7. Repository se comunica com o banco via Prisma
   ↓
8. Resposta retorna pela mesma cadeia
   ↓
9. Controller define status e body no ctx
   ↓
10. Koa envia resposta HTTP ao cliente
```

## Funcionalidades implementadas

### 1. Cadastro de usuários

**Endpoint**: `POST /api/users/register`

Cadastra um novo usuário no sistema após validar:
- Nome com pelo menos 3 caracteres
- Email em formato válido e único
- Senha com mínimo de 6 caracteres

A senha é automaticamente criptografada com bcrypt antes de ser armazenada.

**Exemplo de requisição**:
```json
{
  "name": "João Silva",
  "email": "joao@example.com",
  "password": "senha123"
}
```

**Exemplo de resposta (201)**:
```json
{
  "user": {
    "id": "uuid-gerado",
    "name": "João Silva",
    "email": "joao@example.com",
    "created_at": "2026-02-02T12:00:00.000Z"
  }
}
```

### 2. Listagem de usuários

**Endpoint**: `GET /api/users`

Retorna todos os usuários cadastrados no sistema, sem expor informações sensíveis como senha.

**Exemplo de resposta (200)**:
```json
{
  "users": [
    {
      "id": "uuid-1",
      "name": "João Silva",
      "email": "joao@example.com",
      "created_at": "2026-02-02T12:00:00.000Z"
    },
    {
      "id": "uuid-2",
      "name": "Maria Santos",
      "email": "maria@example.com",
      "created_at": "2026-02-02T13:00:00.000Z"
    }
  ]
}
```

## Detalhamento técnico

### Padrão Repository

O padrão Repository abstrai o acesso aos dados, permitindo trocar a implementação (por exemplo, de Prisma para outro ORM) sem afetar o restante da aplicação.

```typescript
// Interface que define o contrato
interface UsersRepository {
  create(data: CreateUserData): Promise<User>
  findByEmail(email: string): Promise<User | null>
  findMany(): Promise<User[]>
}

// Implementação concreta com Prisma
class PrismaUsersRepository implements UsersRepository {
  async create(data: CreateUserData) {
    return await prisma.user.create({ data })
  }
  // ...
}
```

### Factory Pattern

Factories centralizam a criação de instâncias, gerenciando dependências e facilitando testes:

```typescript
export function makeRegisterService() {
  const usersRepository = new PrismaUsersRepository()
  return new RegisterService(usersRepository)
}
```

### Validação com Zod

O Zod é usado para validar dados de entrada de forma type-safe:

```typescript
const registerSchema = z.object({
  name: z.string().min(3),
  email: z.string().email(),
  password: z.string().min(6)
})

// Uso no controller
const { name, email, password } = registerSchema.parse(ctx.request.body)
```

### Tratamento de erros personalizado

Erros customizados facilitam o tratamento específico:

```typescript
export class UserAlreadyExistsError extends Error {
  constructor() {
    super('Email já cadastrado')
  }
}

// Uso no service
const userExists = await this.usersRepository.findByEmail(email)
if (userExists) {
  throw new UserAlreadyExistsError()
}
```

## Como executar o projeto

### Pré-requisitos

- Node.js 18+ instalado
- Docker e Docker Compose (ou PostgreSQL local)

### Passo 1: Instalar dependências

```bash
npm install
```

### Passo 2: Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL="postgresql://postgres:postgres@localhost:5432/koa_exemplo"
PORT=3000
```

### Passo 3: Iniciar o banco de dados

Com Docker:
```bash
docker-compose up -d
```

Ou configure um PostgreSQL local e ajuste a `DATABASE_URL`.

### Passo 4: Executar migrations

```bash
npx prisma migrate dev
```

Este comando cria as tabelas no banco de dados conforme definido no schema do Prisma.

### Passo 5: Iniciar o servidor

```bash
npm run dev
```

O servidor estará rodando em `http://localhost:3000`.

## Testando a API

### Usando o arquivo exemples.http

O projeto inclui um arquivo `exemples.http` com requisições prontas. Use a extensão **REST Client** do VS Code para executá-las diretamente.

### Usando curl

**Cadastrar usuário**:
```bash
curl -X POST http://localhost:3000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "João Silva",
    "email": "joao@example.com",
    "password": "senha123"
  }'
```

**Listar usuários**:
```bash
curl http://localhost:3000/api/users
```

## Estrutura do banco de dados

### Tabela users

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| id | UUID | Identificador único (PK) |
| name | VARCHAR | Nome do usuário |
| email | VARCHAR | Email único |
| password_hash | VARCHAR | Senha criptografada |
| created_at | TIMESTAMP | Data de criação |

### Migrations

As migrations ficam em `prisma/migrations/` e mantêm o histórico de alterações no banco de dados, permitindo:
- Versionamento do schema
- Rollback se necessário
- Sincronização entre ambientes (dev, staging, prod)

## Próximos passos

Este exemplo serve como base para adicionar funcionalidades mais complexas:

1. **Autenticação JWT**: implementar login e proteção de rotas
2. **Atualização de usuários**: endpoint PUT/PATCH
3. **Deleção de usuários**: endpoint DELETE com validações
4. **Paginação**: adicionar limite e offset na listagem
5. **Filtros**: buscar usuários por nome ou email
6. **Testes**: unit tests e integration tests

## Tecnologias utilizadas

| Tecnologia | Versão | Propósito |
|-----------|--------|-----------|
| **Koa** | ^2.15.0 | Framework web minimalista |
| **@koa/router** | ^13.0.0 | Sistema de rotas |
| **@koa/bodyparser** | ^5.1.1 | Parsing de JSON |
| **Prisma** | ^6.2.0 | ORM para banco de dados |
| **PostgreSQL** | 15 | Banco de dados relacional |
| **TypeScript** | ^5.7.3 | Superset JavaScript com tipos |
| **Zod** | ^3.24.1 | Validação de schemas |
| **bcryptjs** | ^2.4.3 | Criptografia de senhas |
| **tsx** | ^4.19.2 | Execução de TypeScript |

## Conclusão

Este exemplo prático demonstra como o Koa, mesmo sendo minimalista, permite construir aplicações robustas e bem estruturadas. A arquitetura em camadas, o uso de padrões de projeto e a integração com ferramentas modernas (Prisma, TypeScript) resultam em código limpo, testável e escalável.

O projeto serve como ponto de partida tanto para aprendizado quanto para aplicações reais, podendo ser expandido conforme a necessidade.
