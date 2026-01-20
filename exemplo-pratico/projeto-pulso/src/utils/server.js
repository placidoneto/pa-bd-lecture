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