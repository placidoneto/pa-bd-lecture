# API REST ExpressJS

## Alunos responsáveis

- Leandro Sizílio
- Felipe da Costa
- Giovanna
- Leonardo 
- Maria Luisa

## Objetivo

É um framework minimalista para Node.js, projetado para facilitar a criação de servidores web e APIs de forma rápida e eficiente. Ele fornece uma estrutura leve, flexível e eficiente para lidar com as requisições HTTP, gerenciamento de rotas, integração com banco de dados e gerenciamento de middlewares.


# Pré-requesitos para o projeto:
* NodeJS
* ExpressJS
* PostgreSQL
* PgADMIN
* Força de vontade

# Preparando o ambiente
 - Crie e entre na pasta do projeto 
* Windows: ```mkdir meu-projeto``` e ```cd meu-projeto```
* Linux: ```mkdir meu-projeto``` e ```cd meu-projeto```

### Instale os ambientes

#### ExpressJS:
O ExpressJS é um framework utilizado para criar servidores Node.js de forma mais prática. 

```bash
npm install express --save
```

#### Servidor

* Crie um arquivo chamado ```index.js``` e adicione o seguinte código:

```javascript
const express = require('express')
const app = express()
const port = 8080

app.get('/', (req, res) => {
  res.send('Hello World!')
})

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
}) 
```

* Para rodar o servidor, utilize o comando ```node index.js``` e abra o navegador neste [link](http://localhost:8080/).


#### Integrando ao PostgresSQL 

* Instale a dependencia do postgres:
```bash
npm install pg
```

#### Instalando o prisma:

```bash
npm install prisma --save-dev
npm install @prisma/client
npx prisma init
```

* Adicione o endereço do banco no .env gerado pelo prisma:
```
DATABASE_URL="postgresql://USUARIO:SENHA@localhost:5432/NOMEDOBANCO?schema=public"
```

* Adicione os modelos exemplo no schema.prisma:

```
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model Servico {
  id           Int       @id @default(autoincrement())
  nome         String
  categoriaServico String
  dataCadastro DateTime  @default(now())

  prestadorId  Int
  prestador    Prestador @relation(fields: [prestadorId], references: [id])

  clienteId    Int
  cliente      Cliente   @relation(fields: [clienteId], references: [id])
}

model Prestador {
  id           Int        @id @default(autoincrement())
  nome         String     
  sobrenome    String
  timeDoCoracao String
  dataCadastro DateTime   @default(now())

  servicos     Servico[]
}

model Cliente {
  id           Int        @id @default(autoincrement())
  nome         String
  sobrenome    String    
  timeDoCoracao String
  dataCadastro DateTime   @default(now())

  servicos     Servico[]
}
```

#### Gerar migrações e Prisma Cliente

```bash
npx prisma migrate dev --name init
npx prisma generate
```

* Adiciona o prisma ao index.js:
```javascript
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();
```
#### Instalando cors

```bash
npm i cors
```

No index.js:

```javascript
const cors = require('cors');
app.use(cors());
app.use(express.json());
```

#### Instalando o Swagger

```bash
npm install swagger-ui-express swagger-jsdoc
```

* Adicione o Swagger ao index.js:
```javascript
const swaggerUi = require('swagger-ui-express');
const swaggerJsDoc = require('swagger-jsdoc');
```

* Adicione o Swagger:

```javascript
const swaggerOptions = {
  definition: {
    openapi: "3.0.0",
    info: {
      title: "My API",
      version: "1.0.0",
      description: "API documentation",
    },
    servers: [
      {
        url: "http://localhost:8080",
      },
    ],
  },
  apis: ["./index.js"], // Update with the correct filename
};

const swaggerDocs = swaggerJsDoc(swaggerOptions);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(swaggerDocs));
```

#### Adicione os detalhes do Swagger acima do endpoint criado inicialmente
```javascript
/**
 * @swagger
 * /:
 *   get:
 *     summary: Endpoint de Hello World
 *     description: Retorna um "Hello World!" message.
 *     responses:
 *       200:
 *         description: Resposta
 *         content:
 *           text/plain:
 *             schema:
 *               type: string
 *               example: "Hello World!"
 */
```
### CRUD de cliente

##### Get
```javascript
/**
 * @swagger
 * /clientes/{clienteId}:
 *   get:
 *     summary: Recuperar um cliente pelo ID
 *     tags: [Clientes]
 *     parameters:
 *       - in: path
 *         name: clienteId
 *         required: true
 *         schema:
 *           type: integer
 *         description: O ID do cliente a ser encontrado
 *     responses:
 *       200:
 *         description: Cliente encontrado com sucesso
 *       500:
 *         description: Erro interno do servidor
 */
app.get('/clientes/:clienteId', async (req, res) => {
  clienteId = parseInt(req.params.clienteId)
  try {
    const cliente = await prisma.cliente.findUnique({
      where:{
        id: clienteId
      }
    })
    res.status(200).json(cliente);
  } catch (error) {
    res.status(500).json({ error: 'Erro ao encontrar o  cliente', details: error.message });
  }
})
```

#### Post
```javascript
/**
 * @swagger
 * /clientes:
 *   post:
 *     summary: Cria um novo cliente
 *     tags: [Clientes]
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               nome:
 *                 type: string
 *                 description: Nome do cliente
 *                 example: João 
 *               sobrenome:
 *                 type: string
 *                 example: Silva
 *               timeDoCoracao:
 *                 type: string
 *                 example: Alecrim Futebol Clube
 *               
 *     responses:
 *       201:
 *         description: Cliente criado com sucesso
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 id:
 *                   type: integer
 *                   example: 1
 *                 nome:
 *                   type: string
 *                   example: João Silva
 * 
 *                
 *                 dataCadastro:
 *                   type: string
 *                   format: date-time
 *                   example: 2023-10-25T12:00:00.000Z
 *       500:
 *         description: Erro interno do servidor
 */
app.post('/clientes/', async (req, res) => {
  const { nome, sobrenome, timeDoCoracao } = req.body;

  if (!nome) {
    return res.status(400).json({ error: 'O campo "nome" é obrigatório.' });
  }

  if (!sobrenome) {
    return res.status(400).json({ error: 'O campo "sobrenome" é obrigatório.' });
  }

  if (!timeDoCoracao) {
    return res.status(400).json({ error: 'O campo "timeDoCoracao" é obrigatório.' });
  }
  
  try {
    const cliente = await prisma.cliente.create({
      data: {
        nome,
        sobrenome,
        timeDoCoracao
      },
    });
    res.status(201).json(cliente);
  } catch (error) {
    res.status(500).json({ error: 'Erro ao criar cliente', details: error.message });
  }
});
```

#### Put
```javascript

/**
 * @swagger
 * /clientes/{id}:
 *   put:
 *     summary: Atualiza um cliente pelo ID
 *     description: Atualiza o nome, sobrenome e time do coração de um cliente específico
 *     tags: [Clientes]
 *     parameters:
 *       - in: path
 *         name: id
 *         required: true
 *         schema:
 *           type: integer
 *         description: ID do cliente a ser atualizado
 *     requestBody:
 *       required: true
 *       content:
 *         application/json:
 *           schema:
 *             type: object
 *             properties:
 *               nome:
 *                 type: string
 *               sobrenome:
 *                 type: string
 *               timeDoCoracao:
 *                 type: string
 *     responses:
 *       200:
 *         description: Cliente atualizado com sucesso
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 id:
 *                   type: integer
 *                 nome:
 *                   type: string
 *                 sobrenome:
 *                   type: string
 *                 timeDoCoracao:
 *                   type: string
 *       500:
 *         description: Erro ao atualizar cliente
 */
app.put('/clientes/:clienteId', async (req, res) => {
  const { nome, sobrenome, timeDoCoracao } = req.body;
  clienteId = parseInt(req.params.clienteId)

  try {
    const cliente = await prisma.cliente.update({
      where:{
        id: clienteId
      },
      data: {
        nome,
        sobrenome,
        timeDoCoracao
      },
    });
    res.status(200).json(cliente);
  } catch (error) {
    res.status(500).json({ error: 'Erro ao atualizar cliente', details: error.message });
  }
})
```

#### Delete
```javascript

/**
 * @swagger
 * /clientes/{clienteId}:
 *   delete:
 *     summary: Excluir um cliente pelo ID
 *     tags: [Clientes]
 *     parameters:
 *       - in: path
 *         name: clienteId
 *         required: true
 *         schema:
 *           type: integer
 *         description: O ID do cliente a ser excluído
 *     responses:
 *       200:
 *         description: Cliente excluído com sucesso
 *       500:
 *         description: Erro interno do servidor
 */
app.delete('/clientes/:clienteId', async (req, res) => {
  clienteId = parseInt(req.params.clienteId)

  try {
    const cliente = await prisma.cliente.delete({
      where:{
        id: clienteId
      }
    })
    res.status(200).json(cliente);
  } catch (error) {
    res.status(500).json({ error: 'Erro ao deletar o  cliente', details: error.message });
  }
})
```

#### Get tudo
```javascript

/**
 * @swagger
 * /clientes:
 *   get:
 *     summary: Lista todos os clientes
 *     tags: [Clientes]
 *     responses:
 *       200:
 *         description: Lista de clientes retornada com sucesso
 *         content:
 *           application/json:
 *             schema:
 *               type: array
 *               items:
 *                 type: object
 *                 properties:
 *                   id:
 *                     type: integer
 *                     example: 1
 *                   nome:
 *                     type: string
 *                     example: João Silva
 *                   dataCadastro:
 *                     type: string
 *                     format: date-time
 *                     example: 2023-10-25T12:00:00.000Z
 *                   ordensServico:
 *                     type: array
 *                     items:
 *                       type: object
 *                       properties:
 *                         id:
 *                           type: integer
 *                           example: 1
 *                         clienteServicoId:
 *                           type: integer
 *                           example: 1
 *                         prestadorServicoId:
 *                           type: integer
 *                           example: 1
 *                         dataCadastro:
 *                           type: string
 *                           format: date-time
 *                           example: 2023-10-25T12:10:00.000Z
 *                         dataAgendamento:
 *                           type: string
 *                           format: date-time
 *                           example: 2023-10-30T14:00:00.000Z
 *       500:
 *         description: Erro interno do servidor
 */
app.get('/clientes/', async (req, res) => {
  try {
    const clientes = await prisma.cliente.findMany();
    res.json(clientes);
  } catch (error) {
    res.status(500).json({ error: 'Erro ao listar clientes', details: error.message });
  }
});

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
  console.log(`Documentação Swagger disponível em http://localhost:${port}/api-docs`);
}) 
```

# Inicie o servidor

* Para rodar o servidor, utilize o comando ```node index.js``` e abra o navegador neste [link](http://localhost:8080/).


# Trabalho Prático de Desenvolvimento de Software para Persistência usando ORM e ExpressJS

Bem-vindo ao Trabalho Prático de ExpressJS! Para garantir que você tenha uma experiência produtiva e tranquila, siga os passos da aula disponíveis na branch **main**. Após concluir as etapas da aula, você estará preparado para enriquecer seu projeto com os novos modelos que serão adicionados nesta atividade.

## Objetivo

O objetivo deste trabalho prático é que você, na prática, crie novas funcionalidades para o seu projeto. Use, como base, os endpoints implementados para o modelo **Cliente**:

* CRUD para os modelo **Serviço** 
* CRUD para o modelo **Prestador**
* Swagger para os novos endpoints 

Abaixo está o schema que você deverá seguir para a implementação:

```
model Servico {
  id           Int       @id @default(autoincrement())
  nome         String
  categoriaServico String
  dataCadastro DateTime  @default(now())

  prestadorId  Int
  prestador    Prestador @relation(fields: [prestadorId], references: [id])

  clienteId    Int
  cliente      Cliente   @relation(fields: [clienteId], references: [id])
}

model Prestador {
  id           Int        @id @default(autoincrement())
  nome         String     
  sobrenome    String
  timeDoCoracao String
  dataCadastro DateTime   @default(now())

  servicos     Servico[]
}

model Cliente {
  id           Int        @id @default(autoincrement())
  nome         String
  sobrenome    String    
  timeDoCoracao String
  dataCadastro DateTime   @default(now())

  servicos     Servico[]
}
```
