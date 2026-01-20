# Trabalho Prático - Pegar um plantão
## Objetivo
O objetivo desse trabalho prático é aplicar os conceitos do framework Hapi para desenvolver uma das funcionalidades principais do sistema do Pulso. A funcionalidade em questão permite que os profissionais possam assumir um plantão em aberto de determinada instituição de saúde. 

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
- meus_plantoes (Many to Many)

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

### Escala
- id (Long)
- nome (String)
- mes_de_referencia (String)
- escala_publicada (Boolean)
- setor_id (Long)

### Plantão
- hora_de_entrada (TimeType)
- hora_de_saida (TimeType)
- quantidade_profissionais (Int)
- escala_id (Long)
- profissionais (Many to Many)

## Regras de Negócio
1. Um profissional não deve pegar um plantão fora do prazo.
2. Um profissional deve pegar apenas plantões de setores que possuem as suas especialidades. 
3. O profissional deve pegar apenas plantões de instituições que ele está associado.
4. Os plantões disponíveis devem estar em escalas publicadas.
5. Uma escala publicada deve ter no mínimo 5 plantões. 
6. Um profissional só pode ser associado à uma instituição, se em sua lista de especialidades, pertencer a um setor na instituição.
7. Um profissional só pode pegar plantões em que a quantidade limite de profissionais não tenha sido atingida.
8. Ao cadastrar um profissional, deve ser informado em que instituição ele está associado.

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
│   ├── Setor.js
│   ├── Escala.js
│   └── Plantoes.js
├── repositories/
│   ├── profissional.repository.js
│   ├── instituicao.repository.js
│   ├── setor.repository.js
│   ├── escala.repository.js
│   └── plantao.repository.js
├── services/
│   ├── profissional.service.js
│   └── plantao.service.js
├── handlers/
│   ├── profissional.handler.js
│   └── plantao.handler.js
├── schemas/
│   ├── profissional.schema.js
│   └── plantao.schema.js
├── routes/
│   ├── router.js
│   ├── profissional.routes.js
│   └── plantao.routes.js
├── utils/
│   ├── database.js
│   ├── server.js
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

### Escala
- `GET /escalas` - Lista todas as escalas
- `POST /escalas` - Cria nova escala
- `PUT /escalas/{id}/publicar` - Publica escala (seta escala_publicada = true)

### Plantão (Funcionalidade Principal)
- `GET /plantoes/` - Lista plantões
- `POST /plantoes` - Cria novo plantão
- `PUT /plantoes/{id}/pegar ` - *Profissional assume plantão* 
  - Body: { "profissionalId": 1 }
