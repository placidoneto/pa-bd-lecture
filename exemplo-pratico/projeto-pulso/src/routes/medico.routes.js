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

