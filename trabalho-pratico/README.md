# Trabalho Prático - Criar insituição, criar setor, criar profissional
## Objetivo
O objetivo desse trabalho prático é aplicar os conceitos do framework Hapi para desenvolver uma das funcionalidades principais do sistema do Pulso. A funcionalidade em questão permite a criação de um profissional vinculado a uma instituição. 

## Entidades de Domínio

### Especialidade (ENUM - String)
- Cardiologia
- Pediatria
- Ortopedia
- Odontologia
- Fisioterapia

### Profissional
- id (Long)
- nome (String)
- crm (String)
- email (String)
- especialidades (ENUM)
- instituicao_id (Long)

### Instituição
- id (Long)
- nome (String)
- email (String)
- endereco (String)

### Setor
- id (Long)
- nome (String)
- especialidade (Especialidade)
- instituicao_id (Long)

## Regras de Negócio 
1. Um profissional só pode ser associado a uma instituição, se em sua lista de especialidades pertencer uma especialidade presente nos setores da instituição.
2. Ao cadastrar um profissional, deve ser informado em que instituição ele está associado.

## Diagrama explicativo

<img width="581" height="281" alt="diagrama drawio" src="https://github.com/user-attachments/assets/81562493-a00a-4b52-b1f1-e4117e0deb83" />

O profissional está vinculado porque a instituição tem um setor de Cardiologia, que também é especialidade do profissional

## Configuração do Projeto

### 1. Pré-requisitos
- **Node.js** 14+
- **npm** (Gerenciador de pacotes do Node.js)
- Verifique: `node --version` e `npm --version`

### 2. Instalar Dependências
```bash
npm install @hapi/hapi @hapi/boom @hapi/inert @hapi/vision hapi-swagger joi sequelize sqlite3
```

### 3. Estrutura do Projeto 
A estrutura em questão trabalha com Arquitetura em Camadas.
```
pulso-api/
├── config/
│   └── database.js
├── models/
│   ├── index.js
│   ├── Profissional.js
│   ├── Instituicao.js
│   └── Setor.js
├── repositories/
│   ├── profissional.repository.js
│   ├── instituicao.repository.js
│   └── setor.repository.js
├── services/
│   └── profissional.service.js
├── handlers/
│   └── profissional.handler.js
├── schemas/
│   └── profissional.schema.js
├── routes/
│   ├── router.js
│   └── profissional.routes.js
├── utils/
│   ├── database.js
│   └── server.js
├── index.js
└── package.json
```

### 4. Configuração do Banco (config/database.js)
```js
const { Sequelize } = require('sequelize');

const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: './pulso.sqlite',
  logging: false
});

module.exports = sequelize;
```
## Endpoints da API - Pulso (Pegar um Plantão)

### Profissional
- `GET /profissionais` - Lista todos os profissionais
- `POST /profissionais` - Cria novo profissional

### Instituição
- `GET /instituicoes` - Lista todas as instituições
- `POST /instituicoes` - Cria nova instituição

### Setor
- `GET /setores` - Lista todos os setores
- `POST /setores` - Cria novo setor
