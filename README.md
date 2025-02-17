# API REST com Fastify e TypeScript 

## Alunos resposnáveis

- Lívia
- Luis Gustavo
- Marcos
- Ryan
- Igor



## 🎯 Objetivo

Este documento tem como objetivo demonstrar como criar uma **API REST** simples utilizando **Fastify** e **TypeScript**. A proposta é criar uma aplicação robusta, eficiente e bem estruturada.

## 🔥 Tecnologias

As principais tecnologias utilizadas neste projeto são:

- 🐺 **Fastify**: Framework para criar servidores web de forma rápida e eficiente.
- 💻 **Prisma**: ORM para facilitar a conexão com bancos de dados.
- 🦄 **PostgreSQL**: Banco de dados relacional utilizado para armazenar os dados.
- 🧑‍💻 **Node.js**: Plataforma para executar o código JavaScript/TypeScript.
- 🧩 **Zod**: Biblioteca para validação de dados.
- 📖 **Swagger**: Ferramenta para documentar a API.

---

### Iniciando o Projeto

1️⃣ **Criando o `package.json`** 📄

Execute o comando abaixo para gerar o arquivo `package.json` com as configurações padrão:

```bash
npm init -y
```

2️⃣ **Instalando as Dependências** 💅

Instale as dependências necessárias para o projeto:

```bash
npm install -D typescript
npm install -D @types/node
npm install ts-node
npm install zod
npm install fastify

```

3️⃣ **Adicionando Scripts no `package.json`** 💻

Adicione os seguintes scripts no arquivo `package.json` para facilitar a execução:

```json
"scripts": {
  "build": "tsc -p tsconfig.json",   // Para compilar o projeto usando o TypeScript
  "dev": "ts-node src/http/server.ts"  // Para rodar o servidor diretamente com o TypeScript
}
```
### tsx 

- (TypeScript Execute) é uma ferramenta que permite rodar arquivos TypeScript e JavaScript sem necessidade de compilação prévia. Ele é útil para desenvolvimento de servidores em Node.js com TypeScript, pois elimina a necessidade de compilar manualmente os arquivos .ts antes de executá-los

Se preferir utilizar o `tsx` para rodar o server, instale ele junto das dependencias 
- (se optar por usar o tsx, nao sera necessario instalar o `ts-node`, se optar por usar o `ts-node`, não sera necessario baixar o `tsx`)
```bash
npm install --save-dev tsx
```

e altere o `package.json`
```json
  "scripts": {
    "dev": "tsx watch src/http/server.ts"
  },
```

4️⃣ **Inicializando o TypeScript (tsc)** 🌟

Execute o comando abaixo para criar o arquivo `tsconfig.json`:

```bash
npx tsc --init
```

Em seguida, no arquivo `tsconfig.json`, adicione ou ajuste as configurações para garantir que a compilação do TypeScript funcione corretamente:

```json
/* Language and Environment */
"target": "ES2022",                                 
"lib": ["ES2023"],
...
/* Modules */
"module": "Node16",
...
```

5️⃣ **Criando Estrutura de Pastas** 📂

Crie a estrutura de pastas conforme abaixo para organizar o código:

```txt
├── src/
│   ├── http/
│   │   └── server.ts
├── .gitignore
├── package.json
└── tsconfig.json
```

6️⃣ **Testando a API** 🎉

Crie o arquivo `server.ts` dentro da pasta `http` com o seguinte código para iniciar o servidor:

```ts
import fastify from "fastify";

const app = fastify();

app.get("/", async (request, reply) => {
  return "Hello World!";
});

app.listen({ port: 8080, host: "0.0.0.0" }).then((address) => {
  console.log(`Server is running at ${address}`);
});
```

Execute o comando para rodar a api
```bash
npm run dev 
```

---

### ✨ Configurando o Swagger

1️⃣ **Instalando o Swagger** 📚

Para documentar a API, instale as dependências necessárias:

```bash
npm install @fastify/swagger @fastify/swagger-ui
```

2️⃣ **Configurando o Swagger no `server.ts`** 🖥️

Adicione o seguinte código no `server.ts` para configurar o Swagger e permitir o acesso à documentação da API:
pode ser utilizado o swagger

```ts
[...]
import swagger from '@fastify/swagger';
import swaggerUi from '@fastify/swagger-ui'; 

// Registrando o Swagger como uma rota do Fastify
fastify.register(swagger, {
  swagger: {
    info: {
      title: 'API Fastify',
      description: 'Documentação da API usando Swagger',
      version: '1.0.0',
    },
    host: 'localhost:8080',
    schemes: ['http'],                //opcional
    consumes: ['application/json'],   //opcional
    produces: ['application/json'],   //opcional
  }
});

// Rota para acessar a documentação do Swagger
fastify.register(swaggerUi, {
  routePrefix: '/docs', // URL da documentação
  uiConfig: {              //opcional
    docExpansion: 'full',
    deepLinking: false,
  }, //opcional
  staticCSP: true,
  transformSpecificationClone: true,
});
[...]

```

### exemplo de rota documentada 
```js
fastify.get('/usuarios', {
  schema: {
    description: 'Obtém a lista de usuários',
    tags: ['Usuários'], // Agrupa no Swagger
    summary: 'Retorna todos os usuários',
    response: {
      200: {
        description: 'Lista de usuários retornada com sucesso',
        type: 'array',
        items: {
          type: 'object',
          properties: {
            id: { type: 'integer' },
            nome: { type: 'string' },
            email: { type: 'string' }
          }
        }
      }
    }
  }
}, async (request, reply) => {
  return [
    { id: 1, nome: 'Ryan', email: 'ryan@example.com' },
    { id: 2, nome: 'Placido', email: 'placido@example.com' }
  ];
});
```

Agora sua API está documentada pelo swagger e acessível pela URL `http://localhost:8080/docs`. 🌐

---
## Prisma

O Prisma é um ORM moderno e eficiente para Node.js e TypeScript, projetado para facilitar a comunicação entre a sua aplicação e o banco de dados. Ele simplifica as operações de CRUD (criação, leitura, atualização e exclusão), tornando-as mais fáceis e tipadas. Para aproveitar ainda mais o Prisma, você pode instalar uma extensão no VS Code, o que facilita o desenvolvimento.

### Iniciando o Prisma

Primeiro, para instalar o prisma, execute o comando no terminal

```bash
npm install --save-dev prisma
npm install @prisma/client
```

Em seguida, execute o seguinte comando para inicializar o Prisma com suporte ao banco de dados PostgreSQL:

```bash
npx prisma init --datasource-provider postgresql
```

### Configuração do Banco de Dados


Apos rodar o comando acima, sera gerado o arquivo `.env`, configure a URL de conexão com o banco de dados

```ts
DATABASE_URL="postgresql://usuario:senha@localhost:5432/nomedobanco?schema=public"
```

### Criando Modelos no Prisma
Depois de executar o comando no terminal, sera criado uma pasta `📂prisma` com o arquivo `schema.prisma` onde sera possivel criar seus modelos do banco

```ts
[...]

model Book{
  id        String     @id @db.Uuid @default(uuid())
  title     String
  author    String
  description String? @db.Text
  IsFavorite Boolean @default(false)
  IsReading Boolean @default(false)
  IsFinished Boolean @default(false)
}
```
### Como fazer relação entre modelos
no arquivo `schema.prisma`, as relações são feitas pela sintaxe `@relation`, como nessa relação 1:N
```ts
model Author {
  id        String   @id @db.Uuid @default(uuid())
  name      String
  books     Book[]   @relation("AuthorBooks") //um autor pode ter varios livros
}

model Book {
  id        String   @id @db.Uuid @default(uuid())
  title     String
  authorId  String
  author    Author   @relation(fields: [authorId], references: [id], name: "AuthorBooks")
}

```

e uma relação um pouco mais complexa entre, livro, editoria e autor
```ts
model Author {
  id        String   @id @db.Uuid @default(uuid())
  name      String
  books     Book[]   @relation("AuthorBooks") // Um autor pode ter vários livros
}

model Publisher {
  id        String   @id @db.Uuid @default(uuid())
  name      String
  books     Book[]   @relation("PublisherBooks") // Uma editora pode publicar vários livros
}

model Book {
  id          String   @id @db.Uuid @default(uuid())
  title       String
  authorId    String
  publisherId String

  author      Author   @relation(fields: [authorId], references: [id], name: "AuthorBooks")
  publisher   Publisher @relation(fields: [publisherId], references: [id], name: "PublisherBooks")
}

```

- (se preferir que o id seja um numero inteiro e não um uid, utilize esse codigo)
```ts
id        Int      @id @default(autoincrement())
```

Com os modelos criados, faça uma migração com o comando abaixo, depois de executar a migração, de um nome e ela sera concluida, gerando a migração e os arquivos .sql

```bash
npx prisma migrate dev
```

---

Para modularizar a aplicação, criamos duas pastas dentro de `📂http`: `📂routes`, que contém todas as rotas da API, e `📂service`, onde você deve criar o arquivo `prisma.ts`, que será reutilizado nas rotas.

```
├── prisma/
├── src/
│   ├── http/
│   │   ├── service/
│   │   ├── routes/
│   │   └── server.ts
├── .env
├── package.json
├── package-lock.json
└── tsconfig.json
```

O arquivo `prisma.ts` se conecta ao banco com o Prisma:

```ts
import { PrismaClient } from "@prisma/client";

export const prisma = new PrismaClient();
```


## Criando rotas personalizadas

Na pasta `📂routes`, dentro do arquivo `createBook.ts`, criamos a rota para criar um livro, utilizando o Zod para validar o objeto. Para garantir que o Swagger documente corretamente o endpoint, passamos o schema diretamente no código.

### Create

```ts
import { FastifyInstance } from "fastify";
import { z } from "zod";
import { prisma } from "../services/prisma";

export async function createBook(app: FastifyInstance) {
    app.post("/books", {
        schema: { // Configuração do Swagger
            description: "Cria um novo livro",
            tags: ["Livros"], // Categoria no Swagger
            body: {
                type: "object",
                required: ["title", "author", "description"],
                properties: {
                    title: { type: "string", description: "Título do livro" },
                    author: { type: "string", description: "Autor do livro" },
                    description: { type: "string", description: "Descrição do livro" }
                }
            },
            response: {
                201: {
                    description: "Livro criado com sucesso",
                    type: "object",
                    properties: {
                        bookId: { type: "string", description: "ID do livro criado" }
                    }
                }
            }
        }
    }, async (request, reply) => {
        // Validação do corpo da requisição
        const createBookBody = z.object({
            title: z.string(),
            author: z.string(),
            description: z.string(),
        });

        // Extração e validação dos dados
        const { title, author, description } = createBookBody.parse(request.body);

        // Criação do livro no banco de dados
        const book = await prisma.book.create({
            data: { 
                title, 
                author, 
                description 
            },
        });

        // Retorno da resposta
        return reply.status(201).send({ bookId: book.id });
})}

```
Então volte ao arquivo `server.ts` para registrar a criação da rota com `app.register()`
```ts
[...]

app.get("/",  () => {
    return "servidor ok";
})

app.register(createBook) // <--
app.register(getBook)
app.register(updateBook)
app.register(deleteBook)

app.listen({port: 8080}).then(() => {
    console.log("Server is running on port 8080");
})
...

```

### GET

Igualmente para a função get, criamos um arquivo `getBooks.ts` dentro de routes, junto do schema para a documentação do swagger
```ts
import { FastifyInstance } from "fastify";
import { prisma } from "../services/prisma";
import z from "zod";

export async function getBook(app: FastifyInstance) {
    app.get("/books", {
        schema: {
            description: "Retorna todos os livros cadastrados",
            tags: ["Livros"],
            response: {
                200: {
                    description: "Lista de livros",
                    type: "array",
                    items: {
                        type: "object",
                        properties: {
                            id: { type: "string", format: "uuid" },
                            title: { type: "string" },
                            author: { type: "string" },
                            description: { type: "string" }
                        }
                    }
                }
            }
        }
    }, async (request, reply) => {
        const books = await prisma.book.findMany();
        return reply.status(200).send(books);
    });

    app.get("/books/:bookId", {
        // o schema é para a documentação do swagger
        schema: {
            description: "Retorna um livro pelo ID",
            tags: ["Livros"],
            params: {
                type: "object",
                properties: {
                    bookId: { type: "string", format: "uuid", description: "ID do livro" }
                },
                required: ["bookId"]
            },
            response: {
                200: {
                    description: "Detalhes do livro",
                    type: "object",
                    properties: {
                        id: { type: "string", format: "uuid" },
                        title: { type: "string" },
                        author: { type: "string" },
                        description: { type: "string" }
                    }
                },
                404: {
                    description: "Livro não encontrado",
                    type: "object",
                    properties: {
                        message: { type: "string" }
                    }
                }
            }
        } //aqui começa a criação do endpoint
    }, async (request, reply) => {
        const getBookParams = z.object({
            bookId: z.string().uuid(),
        });

        const { bookId } = getBookParams.parse(request.params);

        const book = await prisma.book.findUnique({
            where: { id: bookId }
        });

        if (!book) {
            return reply.status(404).send({ message: "Livro não existe" });
        }

        return reply.status(200).send(book);
    });
}

```

e registramos no `server.ts`
```ts
...

app.register(createBook) 
app.register(getBook) // <- aqui
...
```
Agora criamos o endpoint de update com o arquivo `updateBooks.ts`

### Update

```ts
import { FastifyInstance } from "fastify";
import z from "zod";
import { prisma } from "../services/prisma";

export async function updateBook(app: FastifyInstance) {
  app.patch("/books/:bookId", {
    schema: {
      description: "Atualiza informações de um livro pelo ID",
      tags: ["Livros"],
      params: {
        type: "object",
        properties: {
          bookId: { type: "string", format: "uuid", description: "ID do livro" }
        },
        required: ["bookId"]
      },
      body: {
        type: "object",
        properties: {
          isFavorite: { type: "boolean", description: "Marcar como favorito" },
          isReading: { type: "boolean", description: "Marcar como em leitura" },
          isFinished: { type: "boolean", description: "Marcar como finalizado" }
        }
      },
      response: {
        200: {
          description: "Livro atualizado com sucesso",
          type: "object",
          properties: {
            message: { type: "string" }
          }
        },
        404: {
          description: "Livro não encontrado",
          type: "object",
          properties: {
            message: { type: "string" }
          }
        }
      }
    }
  }, async (request, reply) => {
    // Validação do parâmetro da requisição
    const getBookParams = z.object({
      bookId: z.string().uuid(),
    });

    // Validação do corpo da requisição
    const getBookBody = z.object({
      isFavorite: z.optional(z.boolean()),
      isReading: z.optional(z.boolean()),
      isFinished: z.optional(z.boolean()),
    });

    // Extrai os dados do corpo da requisição
    const { bookId } = getBookParams.parse(request.params);
    const { isFavorite, isReading, isFinished } = getBookBody.parse(request.body);

    // Busca o livro no banco de dados
    const book = await prisma.book.findUnique({
      where: { id: bookId }
    });

    // Se não encontrar o livro, retorna 404
    if (!book) {
      return reply.status(404).send({ message: "Livro não encontrado" });
    }

    // Atualiza o livro no banco de dados
    await prisma.book.update({
      where: { id: bookId },
      data: {
        IsFavorite: isFavorite ?? book.IsFavorite,
        IsReading: isReading ?? book.IsReading,
        IsFinished: isFinished ?? book.IsFinished,
      }
    });

    reply.status(200).send({ message: "Livro atualizado com sucesso" });
  });
}

```
e para terminar o crud, vamos fazer o `delete`, criando tambem um arquivo dentro da pasta routes

### Delete

```ts
import { FastifyInstance } from "fastify";
import z from "zod";
import { prisma } from "../services/prisma";

export async function deleteBook(app: FastifyInstance) {
    app.delete("/books/:bookId", {
        schema: {
            description: "Deleta um livro pelo ID",
            tags: ["Livros"],
            params: {
                type: "object",
                properties: {
                    bookId: { type: "string", format: "uuid", description: "ID do livro" }
                },
                required: ["bookId"]
            },
            response: {
                204: {
                    description: "Livro deletado com sucesso"
                },
                404: {
                    description: "Livro não encontrado",
                    type: "object",
                    properties: {
                        message: { type: "string" }
                    }
                }
            }
        }
    }, async (request, reply) => {
        const getBookParams = z.object({
            bookId: z.string().uuid(),
        });
         // Extração e validação dos dados
        const { bookId } = getBookParams.parse(request.params);

        const book = await prisma.book.findUnique({
            where: { id: bookId }
        });

        if (!book) {
            return reply.status(404).send({ message: "Livro não existe" });
        }

        await prisma.book.delete({
            where: { id: bookId }
        });

        return reply.status(204).send();
    });
}

```

finalizando com todas as importações dentro do `server.ts`, assim temos uma api rest com fastify documentada com o swagger

```ts
import fastify from "fastify";
import { createBook } from "./routes/createBooks";
import { getBook } from "./routes/getBooks";
import { updateBook } from "./routes/updateBook";
import { deleteBook } from "./routes/deleteBook";

import swagger from '@fastify/swagger';
import swaggerUi from '@fastify/swagger-ui';

const app = fastify();

// Configuração do Swagger
app.register(swagger, {
    swagger: {
      info: {
        title: 'API Fastify',
        description: 'Documentação da API usando Swagger',
        version: '1.0.0',
      },
      host: 'localhost:8080',
      schemes: ['http'],
      consumes: ['application/json'],
      produces: ['application/json'],
    }
  });
  
  app.register(swaggerUi, {
    routePrefix: '/docs', // URL da documentação
    uiConfig: {
      docExpansion: 'full',
      deepLinking: false,
    },
    staticCSP: true,
    transformSpecificationClone: true,
  });

app.get("/",  () => {
    return "servidor ok";
})

app.register(createBook)
app.register(getBook)
app.register(updateBook)
app.register(deleteBook)

app.listen({ port: 8080, host: "0.0.0.0" }).then((address) => {
  console.log(`Server is running at ${address}`);
});
```

## Comparação com DjangoRest Framework

O Fastify e o Django Rest Framework são dois frameworks para construir APIs, mas são bem diferentes:

- Fastify é baseado em Node.js (JavaScript), focado em alta performance e escala. É mais rápido e ideal para quem precisa de APIs rápidas e simples de configurar. A comunidade está crescendo, mas ainda é menor do que a do Django.

- Django Rest Framework é uma biblioteca para Django (Python), com muitas funcionalidades já prontas para APIs, como autenticação e serialização. É mais completo e tem uma comunidade enorme, mas pode ser um pouco mais pesado e meno- s rápido que o Fastify.

Em resumo: se você precisa de performance máxima, vai de Fastify; se quer algo mais pronto para usar e com uma comunidade forte, o DjangoRest Framework é a melhor escolha.

# **Trabalho Prático de Desenvolvimento de Software para Persistência usando ORM e Fastify**

## 📌 **Objetivo**

O objetivo deste trabalho é desenvolver uma aplicação para gerenciar **cursos, aulas e professores** utilizando a tecnologia Fastify como framework para criação de uma API REST e Prisma ORM para persistência de dados. A aplicação deve permitir a **criação, leitura, atualização e exclusão** de registros no banco de dados, garantindo a integridade e consistência das informações.

## 🎯 **Descrição**

A aplicação será um sistema de gerenciamento de **mini cursos**, onde:

- Cada **professor** pode ministrar **vários cursos**;
- Cada **curso** pode ter **várias aulas** associadas;
- As informações de **professores, cursos e aulas** devem ser armazenadas e gerenciadas através da API.

A API REST deve seguir boas práticas de desenvolvimento, utilizando **Fastify** para a criação das rotas e **Prisma ORM** para a comunicação com o banco de dados.

## 📜 **Requisitos de Entrega do Trabalho Prático**

### 1️⃣ **Modelagem do Banco de Dados**

Criar um modelo de dados que atenda à descrição acima, contendo as seguintes entidades:

#### **Entidades e Atributos**

- **Professor**

  - `Id` (Identificador único, chave primária)
  - `Nome` (Nome completo)
  - `Cpf` (Cadastro de Pessoa Física, único)
  - `Email` (Endereço de e-mail, único)
  - `Senha` (Senha para autenticação)

- **Curso**

  - `Id` (Identificador único, chave primária)
  - `Nome` (Nome do curso)
  - `Id_Professor` (Relação com a tabela **Professor**, identificando o responsável pelo curso)

- **Aula**
  - `Id` (Identificador único, chave primária)
  - `Video` (URL ou referência para o vídeo da aula)
  - `Descrição` (Texto com detalhes sobre o conteúdo da aula)
  - `Id_Curso` (Relação com a tabela **Curso**)

#### **Relacionamentos**

- **Um professor pode ministrar vários cursos**, mas cada curso tem **apenas um professor**.
- **Um curso pode ter várias aulas**, mas cada aula pertence a **apenas um curso**.

### 2️⃣ **Implementação da API REST**

Desenvolver uma API REST para gerenciar os dados, garantindo as seguintes funcionalidades:

#### **Endpoints**

✅ **Professor**

- Criar um professor (`POST /professores`)
- Listar todos os professores (`GET /professores`)
- Buscar um professor pelo ID (`GET /professores/:id`)
- Atualizar dados de um professor (`PUT /professores/:id`)
- Excluir um professor (`DELETE /professores/:id`)

✅ **Curso**

- Criar um curso (`POST /cursos`)
- Listar todos os cursos (`GET /cursos`)
- Buscar um curso pelo ID (`GET /cursos/:id`)
- Atualizar um curso (`PUT /cursos/:id`)
- Excluir um curso (`DELETE /cursos/:id`)

✅ **Aula**

- Criar uma aula (`POST /aulas`)
- Listar todas as aulas (`GET /aulas`)
- Buscar uma aula pelo ID (`GET /aulas/:id`)
- Atualizar uma aula (`PUT /aulas/:id`)
- Excluir uma aula (`DELETE /aulas/:id`)

### 3️⃣ **Tecnologias Utilizadas**

- **Node.js** com **Fastify** para criação da API
- **Prisma ORM** para comunicação com o banco de dados
- **Banco de dados relacional** (PostgreSQL ou MySQL)
- **Postman ou Insomnia** para testes de API

## 🔍 **Diagrama do Modelo de Dados**

```mermaid
erDiagram
    PROFESSOR {
        int Id PK
        string Nome
        string Cpf UNIQUE
        string Email UNIQUE
        string Senha
    }

    CURSO {
        int Id PK
        string Nome
        int Id_Professor FK "Referência para Professor"
    }

    AULA {
        int Id PK
        string Video
        string Descricao
        int Id_Curso FK "Referência para Curso"
    }

    PROFESSOR ||--o{ CURSO : "Ministra"
    CURSO ||--o{ AULA : "Possui"
```

## 📦 **Entrega**


- Link do Assigment: [API REST com Fastify e TypeScript](https://classroom.github.com/a/ysMqsypr)
- OBS: Uma pasta deverá ser criada no Repositório com o nome `api-rest-fastify-typescript` e todo o código deverá ser colocado dentro dessa pasta.
- OBS2: Todos os TP deverão estar no mesmo repositorio, em pastas separadas, com o nome do TP indicado.
- O nome da equipe do repositorio deverá ser o nome da equipe do TP.

## 📚 Referências

- [FastFy](https://fastify.dev)
- [Zod](https://zod.dev)
- [Prisma](https://www.prisma.io/orm)
- [Swagger](https://swagger.io) 
- [Video referencia](https://www.youtube.com/watch?v=E6mZSJFozvM)