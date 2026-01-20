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
