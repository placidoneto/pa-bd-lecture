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

