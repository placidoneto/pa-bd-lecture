# Exemplo prático — API com Hapi.js, Sequelize e SQLite

## 1. Pré-requisitos

Certifique-se de ter instalado em sua máquina:
- **Node.js** (versão 14 ou superior)
- **npm** (gerenciador de pacotes do Node.js)

Para verificar se estão instalados corretamente, execute:

```bash
node --version
npm --version
```

## 2. Preparação do ambiente

Você pode preparar o ambiente de duas formas:
- **Clonando o repositório do projeto**, caso queira utilizar a estrutura já pronta
- **Criando o projeto do zero**, acompanhando a construção passo a passo

Escolha apenas uma das opções abaixo.

### Clonando o repositório

```bash
git clone https://github.com/IFRN/semin-rios-2o-bimestre-sobre-desenvolvimento-de-api-rest-pulso_hapi.git
```

### Inicializando do zero

Crie o diretório do projeto e entre nele:

```bash
mkdir projeto-pulso
cd projeto-pulso
```

Inicialize o npm para criar o arquivo `package.json`:

```bash
npm init
```

> Observação: <br> Este projeto foi desenvolvido utilizando Node.js 24.9.0 e npm 11.6.2.<br>  Nessas versões, o comando npm init não cria o `package.json` automaticamente sem interação, sendo necessário apenas pressionar Enter em todas as perguntas para gerar o arquivo com as configurações padrão.

Após a execução do comando, verifique se o arquivo `package.json` foi criado corretamente com um conteúdo semelhante a este:

```json
{
  "name": "projeto-pulso",
  "version": "1.0.0",
  "description": "",
  "license": "ISC",
  "author": "",
  "type": "commonjs",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1",
  }
}
```

## 3. Instalar as dependências

Caso você tenha **clonado o projeto pronto**, entre diretório raiz do projeto (neste caso: `projeto-pulso`) e rode:

```bash
npm install
```

Esse comando instalará automaticamente todas as dependências listadas no arquivo `package.json`.

As principais dependências utilizadas neste projeto são:

- `@hapi/hapi` — framework web
- `@hapi/boom` — tratamento padronizado de erros HTTP
- `@hapi/inert` e `@hapi/vision` — plugins necessários para o Swagger
- `hapi-swagger` — geração automática da documentação da API
- `joi` — validação de dados
- `sequelize` — ORM para banco de dados
- `sqlite3` — banco de dados SQLite

### Alternativa: Instalar dependências com versões específicas

Caso prefira instalar as dependências manualmente ou em um projeto vazio, utilize:

```bash
npm install @hapi/hapi @hapi/boom @hapi/inert @hapi/vision hapi-swagger joi sequelize sqlite3
```

Se quiser garantir exatamente as mesmas versões utilizadas no projeto, você pode usar:

```bash
npm install --save-exact
```

## 4. Estrutura atual do projeto (Arquitetura em Camadas)

Abaixo está a estrutura atual do projeto.

Essa organização pode ser visualizada ao clonar o repositório e será construída passo a passo ao longo deste material, seguindo a arquitetura em camadas apresentada anteriormente.

    projeto-pulso/
    │── src/
    │     ├── handlers/
    │     │     ├── medico.handler.js
    │     │     └── plantao.handler.js
    │     ├── models/
    │     │     ├── index.js
    │     │     ├── medico.js
    │     │     └── plantao.js
    │     ├── repositories/
    │     │     ├── medico.repository.js
    │     │     └── plantao.repository.js
    │     ├── services/
    │     │     ├── medico.service.js
    │     │     └── plantao.service.js
    │     ├── routes/
    │     │     ├── medico.routes.js
    │     │     ├── plantao.routes.js
    │     │     └── router.js
    │     ├── schemas/
    │     │     ├── medico.schema.js
    │     │     └── plantao.schema.js
    │     └── utils/
    │           ├── database.js
    │           └── server.js
    ├── index.js
    └── package.json

Essa é a estrutura base do projeto que será utilizada como referência durante todo o desenvolvimento.

Nos próximos passos, cada arquivo será criado e implementado individualmente, respeitando essa organização e a separação de responsabilidades definida pela arquitetura.

## 5. Arquivos de Utilitários

O arquivo [src/utils/database.js](src/utils/database.js) configura a conexão com SQLite:

```javascript
const { Sequelize } = require('sequelize');

const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: './database.sqlite',
  logging: false
});

module.exports = sequelize;
```

SQLite armazena os dados em um arquivo local (`database.sqlite`), ideal para desenvolvimento.

---

Arquivo [src/utils/server.js](src/utils/server.js):

```javascript
const Hapi = require("@hapi/hapi");
const Inert = require("@hapi/inert");
const Vision = require("@hapi/vision");
const HapiSwagger = require("hapi-swagger");
const router = require("../routes/router");

const server = Hapi.server({
  port: 8000,
  host: "localhost"
});

// Configuração do Swagger
const swaggerOptions = {
  info: {
    title: 'API de Gerenciamento de Médicos e Plantões',
    version: '1.0.0',
    description: 'API REST com Hapi.js, Sequelize ORM e SQLite'
  },
  grouping: 'tags',
  tags: [
    { name: 'medicos', description: 'Operações relacionadas a médicos' },
    { name: 'plantoes', description: 'Operações relacionadas a plantões' }
  ]
};

// Registrar plugins
const init = async () => {
  await server.register([
    Inert,
    Vision,
    {
      plugin: HapiSwagger,
      options: swaggerOptions
    }
  ]);

  // Registrar rotas
  router.forEach((path) => server.route(path));
};

init();

module.exports = server;
```

**O que faz:**
- Cria o servidor Hapi na porta 8000
- Registra plugins: Inert (arquivos estáticos), Vision (templates), HapiSwagger
- Configura documentação Swagger/OpenAPI
- Registra todas as rotas da aplicação

## 5. Models (Entidades)

Arquivo [src/models/medico.js](src/models/medico.js):

```javascript
const { DataTypes } = require('sequelize');
const sequelize = require('../utils/database');

const Medico = sequelize.define('Medico', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  nome: {
    type: DataTypes.STRING(100),
    allowNull: false
  },
  crm: {
    type: DataTypes.STRING(20),
    allowNull: false,
    unique: true // CRM único
  },
  especialidade: {
    type: DataTypes.STRING(50),
    allowNull: false
  }
}, {
  tableName: 'medicos',
  timestamps: true // createdAt, updatedAt
});

module.exports = Medico;
```

**Campos da tabela `medicos`:**
- `id` — identificador único, gerado automaticamente
- `nome` — nome do médico
- `crm` — número do CRM (único)
- `especialidade` — especialidade do médico
- `createdAt` — data de criação
- `updatedAt` — data de última atualização

---

Arquivo [src/models/plantao.js](src/models/plantao.js):

```javascript
const { DataTypes } = require('sequelize');
const sequelize = require('../utils/database');

const Plantao = sequelize.define('Plantao', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  medicoId: {
    type: DataTypes.INTEGER,
    allowNull: false,
    references: {
      model: 'medicos',
      key: 'id'
    },
    onDelete: 'CASCADE', // Se deletar médico, deleta plantões
    onUpdate: 'CASCADE'
  },
  data: {
    type: DataTypes.DATEONLY,
    allowNull: false
  },
  horarioInicio: {
    type: DataTypes.STRING(5),
    allowNull: false
  },
  horarioFim: {
    type: DataTypes.STRING(5),
    allowNull: false
  },
  local: {
    type: DataTypes.STRING(100),
    allowNull: false
  }
}, {
  tableName: 'plantoes',
  timestamps: true
});

module.exports = Plantao;
```

**Campos da tabela `plantoes`:**
- `id` — identificador único, gerado automaticamente
- `medicoId` — referência ao médico (chave estrangeira)
- `data` — data do plantão (formato: YYYY-MM-DD)
- `horarioInicio` — hora de início (formato: HH:mm)
- `horarioFim` — hora de término (formato: HH:mm)
- `local` — local onde o plantão acontece
- `createdAt` — data de criação
- `updatedAt` — data de última atualização

---

Arquivo [src/models/index.js](src/models/index.js):

```javascript
const Medico = require('./medico');
const Plantao = require('./plantao');

// Definindo relacionamentos bidirecionais
Medico.hasMany(Plantao, {
  foreignKey: 'medicoId',
  as: 'plantoes' // médico.plantoes
});

Plantao.belongsTo(Medico, {
  foreignKey: 'medicoId',
  as: 'medico' // plantao.medico
});

module.exports = { Medico, Plantao };
```

**O que faz:**
- Define a relação 1:N entre Médicos e Plantões
- Usa `hasMany()` para indicar que um Médico pode ter vários Plantões
- Usa `belongsTo()` para indicar que um Plantão pertence a um Médico

**Por que usar?**
- Centraliza a importação de todos os modelos da aplicação
- Define os relacionamentos entre as entidades em um único arquivo
- Evita dependências circulares entre os modelos
- Segue o padrão do ORM Sequelize, onde o `index.js` é usado para configurar e exportar os modelos já relacionados

Esse arquivo garante que os modelos sejam carregados corretamente antes de serem utilizados em outras partes do projeto.

## 6. Repositories (Acesso ao banco)

Arquivo [src/repositories/medico.repository.js](src/repositories/medico.repository.js):

```javascript
const { Medico, Plantao } = require('../models');

exports.findAll = async () => {
  return await Medico.findAll({
    include: [{ model: Plantao, as: 'plantoes' }] // Eager loading
  });
};

exports.findById = async (id) => {
  return await Medico.findByPk(id, {
    include: [{ model: Plantao, as: 'plantoes' }]
  });
};

exports.findByCrm = async (crm) => {
  return await Medico.findOne({ where: { crm } });
};

exports.save = async (medicoData) => {
  return await Medico.create(medicoData);
};

exports.update = async (id, medicoData) => {
  const medico = await Medico.findByPk(id);
  if (!medico) return null;
  
  await medico.update(medicoData);
  return medico;
};

exports.delete = async (id) => {
  const medico = await Medico.findByPk(id);
  if (!medico) return false;
  
  await medico.destroy(); // Cascade delete nos plantões
  return true;
};
```

**Métodos:**
- `findAll()` — obtém todos os médicos com seus plantões
- `findById(id)` — obtém um médico por ID
- `findByCrm(crm)` — obtém um médico por CRM
- `save(medicoData)` — cria um novo médico
- `update(id, medicoData)` — atualiza um médico existente
- `delete(id)` — deleta um médico existente

---

Arquivo [src/repositories/plantao.repository.js](src/repositories/plantao.repository.js):

```javascript
const { Plantao, Medico } = require('../models');

exports.findAll = async () => {
  return await Plantao.findAll({
    include: [{ model: Medico, as: 'medico' }] // Inclui dados do médico
  });
};

exports.findById = async (id) => {
  return await Plantao.findByPk(id, {
    include: [{ model: Medico, as: 'medico' }]
  });
};

exports.findByMedicoId = async (medicoId) => {
  return await Plantao.findAll({
    where: { medicoId },
    include: [{ model: Medico, as: 'medico' }]
  });
};

exports.save = async (plantaoData) => {
  return await Plantao.create(plantaoData);
};

exports.update = async (id, plantaoData) => {
  const plantao = await Plantao.findByPk(id);
  if (!plantao) return null;
  
  await plantao.update(plantaoData);
  return plantao;
};

exports.delete = async (id) => {
  const plantao = await Plantao.findByPk(id);
  if (!plantao) return false;
  
  await plantao.destroy();
  return true;
};
```

**Métodos:**
- `findAll()` — obtém todos os plantões com dados do médico
- `findById(id)` — obtém um plantão por ID
- `findByMedicoId(medicoId)` — obtém plantões de um médico
- `save(plantaoData)` — cria um novo plantão
- `update(id, plantaoData)` — atualiza um plantão
- `delete(id)` — deleta um plantão

## 7. Services (Lógica de negócio)

Arquivo [src/services/medico.service.js](src/services/medico.service.js):

```javascript
const MedicoRepository = require('../repositories/medico.repository');

exports.listar = async () => {
  return await MedicoRepository.findAll();
};

exports.buscarPorId = async (id) => {
  return await MedicoRepository.findById(parseInt(id));
};

exports.criar = async (dto) => {
  // Verificar se já existe médico com o mesmo CRM
  const medicoExistente = await MedicoRepository.findByCrm(dto.crm);
  if (medicoExistente) {
    throw new Error('Já existe um médico cadastrado com este CRM');
  }
  
  return await MedicoRepository.save(dto);
};

exports.atualizar = async (id, dto) => {
  // Verificar se o CRM já existe em outro médico
  if (dto.crm) {
    const medicoExistente = await MedicoRepository.findByCrm(dto.crm);
    if (medicoExistente && medicoExistente.id !== parseInt(id)) {
      throw new Error('Já existe um médico cadastrado com este CRM');
    }
  }
  
  return await MedicoRepository.update(parseInt(id), dto);
};

exports.deletar = async (id) => {
  return await MedicoRepository.delete(parseInt(id));
};
```

**O que faz:**
- Implementa validação de CRM único
- Chama o Repository para operações de banco
- Lança erros com mensagens claras

---

Arquivo [src/services/plantao.service.js](src/services/plantao.service.js):

```javascript
const PlantaoRepository = require('../repositories/plantao.repository');
const MedicoRepository = require('../repositories/medico.repository');

exports.listar = async () => {
  return await PlantaoRepository.findAll();
};

exports.buscarPorId = async (id) => {
  return await PlantaoRepository.findById(parseInt(id));
};

exports.buscarPorMedico = async (medicoId) => {
  return await PlantaoRepository.findByMedicoId(parseInt(medicoId));
};

exports.criar = async (dto) => {
  // Verificar se o médico existe
  const medico = await MedicoRepository.findById(dto.medicoId);
  if (!medico) {
    throw new Error('Médico não encontrado');
  }
  
  return await PlantaoRepository.save(dto);
};

exports.atualizar = async (id, dto) => {
  // Verificar se o médico existe caso medicoId seja fornecido
  if (dto.medicoId) {
    const medico = await MedicoRepository.findById(dto.medicoId);
    if (!medico) {
      throw new Error('Médico não encontrado');
    }
  }
  
  return await PlantaoRepository.update(parseInt(id), dto);
};

exports.deletar = async (id) => {
  return await PlantaoRepository.delete(parseInt(id));
};
```

**O que faz:**
- Valida se o médico existe antes de criar/atualizar plantão
- Implementa regras de negócio específicas
- Chama o Repository para operações de banco

## 8. Handlers (Tratamento de requisições)

Arquivo [src/handlers/medico.handler.js](src/handlers/medico.handler.js):

```javascript
const MedicoService = require('../services/medico.service');
const Boom = require('@hapi/boom');

exports.listar = async (request, h) => {
  try {
    const medicos = await MedicoService.listar();
    return medicos;
  } catch (error) {
    throw Boom.internal('Erro ao listar médicos');
  }
};

exports.buscarPorId = async (request, h) => {
  try {
    const medico = await MedicoService.buscarPorId(request.params.id);
    if (!medico) {
      throw Boom.notFound('Médico não encontrado');
    }
    return medico;
  } catch (error) {
    if (error.isBoom) throw error;
    throw Boom.internal('Erro ao buscar médico');
  }
};

exports.criar = async (request, h) => {
  try {
    const medico = await MedicoService.criar(request.payload);
    return h.response(medico).code(201);
  } catch (error) {
    throw Boom.badRequest(error.message);
  }
};

exports.atualizar = async (request, h) => {
  try {
    const medico = await MedicoService.atualizar(request.params.id, request.payload);
    if (!medico) {
      throw Boom.notFound('Médico não encontrado');
    }
    return medico;
  } catch (error) {
    if (error.isBoom) throw error;
    throw Boom.badRequest(error.message);
  }
};

exports.deletar = async (request, h) => {
  try {
    const deleted = await MedicoService.deletar(request.params.id);
    if (!deleted) {
      throw Boom.notFound('Médico não encontrado');
    }
    return h.response().code(204);
  } catch (error) {
    if (error.isBoom) throw error;
    throw Boom.internal('Erro ao deletar médico');
  }
};
```
**O que faz:**
- Recebe dados da requisição (params, payload)
- Chama métodos do PlantaoService
- Retorna respostas HTTP adequadas
- Trata erros e converte em respostas HTTP padronizadas (404, 400, 500, etc.)
---

Arquivo [src/handlers/plantao.handler.js](src/handlers/plantao.handler.js):

```javascript
const PlantaoService = require('../services/plantao.service');
const Boom = require('@hapi/boom');

exports.listar = async (request, h) => {
  try {
    const plantoes = await PlantaoService.listar();
    return plantoes;
  } catch (error) {
    throw Boom.internal('Erro ao listar plantões');
  }
};

exports.buscarPorId = async (request, h) => {
  try {
    const plantao = await PlantaoService.buscarPorId(request.params.id);
    if (!plantao) {
      throw Boom.notFound('Plantão não encontrado');
    }
    return plantao;
  } catch (error) {
    if (error.isBoom) throw error;
    throw Boom.internal('Erro ao buscar plantão');
  }
};

exports.buscarPorMedico = async (request, h) => {
  try {
    const plantoes = await PlantaoService.buscarPorMedico(request.params.medicoId);
    return plantoes;
  } catch (error) {
    throw Boom.internal('Erro ao buscar plantões do médico');
  }
};

exports.criar = async (request, h) => {
  try {
    const plantao = await PlantaoService.criar(request.payload);
    return h.response(plantao).code(201);
  } catch (error) {
    throw Boom.badRequest(error.message);
  }
};

exports.atualizar = async (request, h) => {
  try {
    const plantao = await PlantaoService.atualizar(request.params.id, request.payload);
    if (!plantao) {
      throw Boom.notFound('Plantão não encontrado');
    }
    return plantao;
  } catch (error) {
    if (error.isBoom) throw error;
    throw Boom.badRequest(error.message);
  }
};

exports.deletar = async (request, h) => {
  try {
    const deleted = await PlantaoService.deletar(request.params.id);
    if (!deleted) {
      throw Boom.notFound('Plantão não encontrado');
    }
    return h.response().code(204);
  } catch (error) {
    if (error.isBoom) throw error;
    throw Boom.internal('Erro ao deletar plantão');
  }
};
```
**O que faz:**
- Recebe dados da requisição (params, payload)
- Chama métodos do PlantaoService
- Retorna respostas HTTP adequadas
- Trata erros e converte em respostas HTTP padronizadas (404, 400, 500, etc.)
---
## 9. Routes (Responsável pelas rotas)
Arquivo [src/routes/medico.routes.js](src/routes/medico.routes.js):

```javascript
const MedicoHandler = require('../handlers/medico.handler');
const MedicoSchema = require('../schemas/medico.schema');
const Joi = require('joi');

module.exports = [
  {
    method: 'GET',
    path: '/medicos',
    options: {
      tags: ['api', 'medicos'],
      description: 'Listar todos os médicos',
      notes: 'Retorna a lista completa de médicos com seus plantões'
    },
    handler: MedicoHandler.listar
  },
  {
    method: 'GET',
    path: '/medicos/{id}',
    options: {
      tags: ['api', 'medicos'],
      description: 'Buscar médico por ID',
      notes: 'Retorna os dados de um médico específico com seus plantões',
      validate: {
        params: Joi.object({
          id: Joi.number().integer().required().description('ID do médico')
        })
      }
    },
    handler: MedicoHandler.buscarPorId
  },
  {
    method: 'POST',
    path: '/medicos',
    options: {
      tags: ['api', 'medicos'],
      description: 'Criar novo médico',
      notes: 'Cria um novo médico no sistema',
      validate: {
        payload: MedicoSchema.create,
        failAction: (request, h, error) => {
          return h.response({ message: error.message }).code(400).takeover();
        }
      }
    },
    handler: MedicoHandler.criar
  },
  {
    method: 'PUT',
    path: '/medicos/{id}',
    options: {
      tags: ['api', 'medicos'],
      description: 'Atualizar médico',
      notes: 'Atualiza os dados de um médico existente',
      validate: {
        params: Joi.object({
          id: Joi.number().integer().required().description('ID do médico')
        }),
        payload: MedicoSchema.update,
        failAction: (request, h, error) => {
          return h.response({ message: error.message }).code(400).takeover();
        }
      }
    },
    handler: MedicoHandler.atualizar
  },
  {
    method: 'DELETE',
    path: '/medicos/{id}',
    options: {
      tags: ['api', 'medicos'],
      description: 'Deletar médico',
      notes: 'Remove um médico e todos os seus plantões (CASCADE)',
      validate: {
        params: Joi.object({
          id: Joi.number().integer().required().description('ID do médico')
        })
      }
    },
    handler: MedicoHandler.deletar
  }
];
```
**O que faz**:
- Define o método HTTP e a URL de cada endpoint
- Configura a documentação da rota (Swagger)
- Define qual handler será executado
- Aplica validações de parâmetros e do corpo da requisição usando Joi

As rotas funcionam apenas como ponto de entrada da API, encaminhando a requisição para o handler correspondente.

---

Arquivo [src/routes/plantao.routes.js](src/routes/plantao.routes.js):

```javascript
const PlantaoHandler = require('../handlers/plantao.handler');
const PlantaoSchema = require('../schemas/plantao.schema');
const Joi = require('joi');

module.exports = [
  {
    method: 'GET',
    path: '/plantoes',
    options: {
      tags: ['api', 'plantoes'],
      description: 'Listar todos os plantões',
      notes: 'Retorna a lista completa de plantões com dados do médico'
    },
    handler: PlantaoHandler.listar
  },
  {
    method: 'GET',
    path: '/plantoes/{id}',
    options: {
      tags: ['api', 'plantoes'],
      description: 'Buscar plantão por ID',
      notes: 'Retorna os dados de um plantão específico com dados do médico',
      validate: {
        params: Joi.object({
          id: Joi.number().integer().required().description('ID do plantão')
        })
      }
    },
    handler: PlantaoHandler.buscarPorId
  },
  {
    method: 'GET',
    path: '/medicos/{medicoId}/plantoes',
    options: {
      tags: ['api', 'plantoes'],
      description: 'Buscar plantões de um médico',
      notes: 'Retorna todos os plantões de um médico específico',
      validate: {
        params: Joi.object({
          medicoId: Joi.number().integer().required().description('ID do médico')
        })
      }
    },
    handler: PlantaoHandler.buscarPorMedico
  },
  {
    method: 'POST',
    path: '/plantoes',
    options: {
      tags: ['api', 'plantoes'],
      description: 'Criar novo plantão',
      notes: 'Cria um novo plantão associado a um médico',
      validate: {
        payload: PlantaoSchema.create,
        failAction: (request, h, error) => {
          return h.response({ message: error.message }).code(400).takeover();
        }
      }
    },
    handler: PlantaoHandler.criar
  },
  {
    method: 'PUT',
    path: '/plantoes/{id}',
    options: {
      tags: ['api', 'plantoes'],
      description: 'Atualizar plantão',
      notes: 'Atualiza os dados de um plantão existente',
      validate: {
        params: Joi.object({
          id: Joi.number().integer().required().description('ID do plantão')
        }),
        payload: PlantaoSchema.update,
        failAction: (request, h, error) => {
          return h.response({ message: error.message }).code(400).takeover();
        }
      }
    },
    handler: PlantaoHandler.atualizar
  },
  {
    method: 'DELETE',
    path: '/plantoes/{id}',
    options: {
      tags: ['api', 'plantoes'],
      description: 'Deletar plantão',
      notes: 'Remove um plantão do sistema',
      validate: {
        params: Joi.object({
          id: Joi.number().integer().required().description('ID do plantão')
        })
      }
    },
    handler: PlantaoHandler.deletar
  }
];
```
---
Arquivo [src/routes/routes.js](src/routes/routes.js):

```javascript
const medicoRoutes = require("./medico.routes");
const plantaoRoutes = require("./plantao.routes");

const router = [
  {
    method: "GET",
    path: "/",
    handler: (req, h) => {
      return { message: "API de Gerenciamento de Médicos e Plantões" };
    }
  },
  ...medicoRoutes,
  ...plantaoRoutes

//O spread (...) é equivalente a:
//   const router = [
//   { method: 'GET', path: '/' },
//   { method: 'GET', path: '/medicos' },
//   { method: 'POST', path: '/medicos' },
//   { method: 'GET', path: '/plantoes' }
// ];

];

module.exports = router;
```
**O que faz:**
- Centraliza todas as rotas da aplicação
- Importa rotas de Médicos e Plantões
- Define rota raiz `/`

## 10. Schemas (Validação de dados)

Arquivo [src/schemas/medico.schema.js](src/schemas/medico.schema.js):

```javascript
const Joi = require('joi');

exports.create = Joi.object({
  nome: Joi.string()
    .required()
    .min(3)
    .max(100)
    .messages({
      'string.base': 'Nome deve ser um texto',
      'string.empty': 'Nome não pode estar vazio',
      'string.min': 'Nome deve ter no mínimo 3 caracteres',
      'string.max': 'Nome não pode ter mais de 100 caracteres',
      'any.required': 'Nome é obrigatório'
    }),
  crm: Joi.string()
    .required()
    .min(4)
    .max(20)
    .messages({
      'string.base': 'CRM deve ser um texto',
      'string.empty': 'CRM não pode estar vazio',
      'string.min': 'CRM deve ter no mínimo 4 caracteres',
      'string.max': 'CRM não pode ter mais de 20 caracteres',
      'any.required': 'CRM é obrigatório'
    }),
  especialidade: Joi.string()
    .required()
    .min(3)
    .max(50)
    .messages({
      'string.base': 'Especialidade deve ser um texto',
      'string.empty': 'Especialidade não pode estar vazia',
      'string.min': 'Especialidade deve ter no mínimo 3 caracteres',
      'string.max': 'Especialidade não pode ter mais de 50 caracteres',
      'any.required': 'Especialidade é obrigatória'
    })
});

exports.update = Joi.object({
  nome: Joi.string()
    .min(3)
    .max(100)
    .messages({
      'string.base': 'Nome deve ser um texto',
      'string.empty': 'Nome não pode estar vazio',
      'string.min': 'Nome deve ter no mínimo 3 caracteres',
      'string.max': 'Nome não pode ter mais de 100 caracteres'
    }),
  crm: Joi.string()
    .min(4)
    .max(20)
    .messages({
      'string.base': 'CRM deve ser um texto',
      'string.empty': 'CRM não pode estar vazio',
      'string.min': 'CRM deve ter no mínimo 4 caracteres',
      'string.max': 'CRM não pode ter mais de 20 caracteres'
    }),
  especialidade: Joi.string()
    .min(3)
    .max(50)
    .messages({
      'string.base': 'Especialidade deve ser um texto',
      'string.empty': 'Especialidade não pode estar vazia',
      'string.min': 'Especialidade deve ter no mínimo 3 caracteres',
      'string.max': 'Especialidade não pode ter mais de 50 caracteres'
    })
}).min(1).messages({
  'object.min': 'Pelo menos um campo deve ser fornecido para atualização'
});
```

**O que faz:**
- Valida dados de criação e atualização
- Garante tipos de dados corretos (números, strings, datas)

---
Arquivo [src/schemas/plantao.schema.js](src/schemas/plantao.schema.js):

```javascript
const Joi = require('joi');

exports.create = Joi.object({
  medicoId: Joi.number()
    .integer()
    .required()
    .messages({
      'number.base': 'ID do médico deve ser um número',
      'number.integer': 'ID do médico deve ser um número inteiro',
      'any.required': 'ID do médico é obrigatório'
    }),
  data: Joi.date()
    .iso()
    .required()
    .messages({
      'date.base': 'Data deve ser uma data válida',
      'date.format': 'Data deve estar no formato ISO (YYYY-MM-DD)',
      'any.required': 'Data é obrigatória'
    }),
  horarioInicio: Joi.string()
    .pattern(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/)
    .required()
    .messages({
      'string.base': 'Horário de início deve ser um texto',
      'string.pattern.base': 'Horário de início deve estar no formato HH:mm',
      'any.required': 'Horário de início é obrigatório'
    }),
  horarioFim: Joi.string()
    .pattern(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/)
    .required()
    .messages({
      'string.base': 'Horário de fim deve ser um texto',
      'string.pattern.base': 'Horário de fim deve estar no formato HH:mm',
      'any.required': 'Horário de fim é obrigatório'
    }),
  local: Joi.string()
    .required()
    .min(3)
    .max(100)
    .messages({
      'string.base': 'Local deve ser um texto',
      'string.empty': 'Local não pode estar vazio',
      'string.min': 'Local deve ter no mínimo 3 caracteres',
      'string.max': 'Local não pode ter mais de 100 caracteres',
      'any.required': 'Local é obrigatório'
    })
});

exports.update = Joi.object({
  medicoId: Joi.number()
    .integer()
    .messages({
      'number.base': 'ID do médico deve ser um número',
      'number.integer': 'ID do médico deve ser um número inteiro'
    }),
  data: Joi.date()
    .iso()
    .messages({
      'date.base': 'Data deve ser uma data válida',
      'date.format': 'Data deve estar no formato ISO (YYYY-MM-DD)'
    }),
  horarioInicio: Joi.string()
    .pattern(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/)
    .messages({
      'string.base': 'Horário de início deve ser um texto',
      'string.pattern.base': 'Horário de início deve estar no formato HH:mm'
    }),
  horarioFim: Joi.string()
    .pattern(/^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/)
    .messages({
      'string.base': 'Horário de fim deve ser um texto',
      'string.pattern.base': 'Horário de fim deve estar no formato HH:mm'
    }),
  local: Joi.string()
    .min(3)
    .max(100)
    .messages({
      'string.base': 'Local deve ser um texto',
      'string.empty': 'Local não pode estar vazio',
      'string.min': 'Local deve ter no mínimo 3 caracteres',
      'string.max': 'Local não pode ter mais de 100 caracteres'
    })
}).min(1).messages({
  'object.min': 'Pelo menos um campo deve ser fornecido para atualização'
});

```

**O que faz:**
- Valida dados de criação e atualização
- Usa regex para validar formato de hora (HH:mm)
- Garante tipos de dados corretos (números, strings, datas)

## 11. Arquivos de Entrada e Configuração

Arquivo [index.js](index.js):

```javascript
const server = require("./src/utils/server");
const sequelize = require("./src/utils/database");

(async () => {
  try {
    // Sincronizar banco de dados
    await sequelize.sync({ force: false }); // force: true recria as tabelas
    console.log('Banco de dados sincronizado');
    
    // Iniciar servidor
    await server.start();
    console.log('Servidor rodando em:', server.info.uri);
  } catch (error) {
    console.error('Erro ao iniciar:', error);
    process.exit(1);
  }
})();
```

**O que faz:**
- Importa e inicia o servidor
- Exibe mensagens de boas-vindas no console
- Mostra URLs de acesso (API e Swagger)

## 12. Executar a aplicação


No diretório raiz do projeto (neste caso: `projeto-pulso`), rode:

    node index.js

**A API estará disponível em:** `http://127.0.0.1:8000`

**O Swagger (documentação interativa) estará em:** `http://127.0.0.1:8000/documentation`

## 13. Exemplos de requisições

### Médicos

#### Listar todos os médicos
```bash
curl -X GET http://127.0.0.1:8000/medicos
```

#### Buscar médico por ID
```bash
curl -X GET http://127.0.0.1:8000/medicos/1
```

#### Criar novo médico
```bash
curl -X POST http://127.0.0.1:8000/medicos \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Dr. João Silva",
    "crm": "12345",
    "especialidade": "Cardiologia"
  }'
```

#### Atualizar médico
```bash
curl -X PUT http://127.0.0.1:8000/medicos/1 \
  -H "Content-Type: application/json" \
  -d '{
    "especialidade": "Cirurgia Geral"
  }'
```

### Plantões

#### Listar todos os plantões
```bash
curl -X GET http://127.0.0.1:8000/plantoes
```

#### Buscar plantão por ID
```bash
curl -X GET http://127.0.0.1:8000/plantoes/1
```

#### Buscar plantões de um médico específico
```bash
curl -X GET http://127.0.0.1:8000/medicos/1/plantoes
```

#### Criar novo plantão
```bash
curl -X POST http://127.0.0.1:8000/plantoes \
  -H "Content-Type: application/json" \
  -d '{
    "medicoId": 1,
    "data": "2024-01-20",
    "horarioInicio": "08:00",
    "horarioFim": "16:00",
    "local": "Hospital Central"
  }'
```

#### Atualizar plantão
```bash
curl -X PUT http://127.0.0.1:8000/plantoes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "local": "Clínica Privada"
  }'
```

#### Deletar plantão
```bash
curl -X DELETE http://127.0.0.1:8000/plantoes/1
```