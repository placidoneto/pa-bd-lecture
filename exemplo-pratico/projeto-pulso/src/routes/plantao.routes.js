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
