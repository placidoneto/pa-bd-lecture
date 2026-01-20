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

