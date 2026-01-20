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
