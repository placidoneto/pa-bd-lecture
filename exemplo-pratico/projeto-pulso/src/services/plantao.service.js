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
