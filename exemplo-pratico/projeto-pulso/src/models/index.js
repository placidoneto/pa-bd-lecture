const Medico = require('./medico');
const Plantao = require('./plantao');

// Definindo relacionamentos bidirecionais
Medico.hasMany(Plantao, {
  foreignKey: 'medicoId',
  as: 'plantoes' // médico.plantoes
});

Plantao.belongsTo(Medico, {
  foreignKey: 'medicoId',
  as: 'medico' // plantao.medico
});

module.exports = { Medico, Plantao };
