const { Medico, Plantao } = require('../models');

exports.findAll = async () => {
  return await Medico.findAll({
    include: [{ model: Plantao, as: 'plantoes' }] // Eager loading
  });
};

exports.findById = async (id) => {
  return await Medico.findByPk(id, {
    include: [{ model: Plantao, as: 'plantoes' }]
  });
};

exports.findByCrm = async (crm) => {
  return await Medico.findOne({ where: { crm } });
};

exports.save = async (medicoData) => {
  return await Medico.create(medicoData);
};

exports.update = async (id, medicoData) => {
  const medico = await Medico.findByPk(id);
  if (!medico) return null;
  
  await medico.update(medicoData);
  return medico;
};

exports.delete = async (id) => {
  const medico = await Medico.findByPk(id);
  if (!medico) return false;
  
  await medico.destroy(); // Cascade delete nos plantões
  return true;
};

