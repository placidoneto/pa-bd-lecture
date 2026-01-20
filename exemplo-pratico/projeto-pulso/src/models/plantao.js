const { DataTypes } = require('sequelize');
const sequelize = require('../utils/database');

const Plantao = sequelize.define('Plantao', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  medicoId: {
    type: DataTypes.INTEGER,
    allowNull: false,
    references: {
      model: 'medicos',
      key: 'id'
    },
    onDelete: 'CASCADE', // Se deletar médico, deleta plantões
    onUpdate: 'CASCADE'
  },
  data: {
    type: DataTypes.DATEONLY,
    allowNull: false
  },
  horarioInicio: {
    type: DataTypes.STRING(5),
    allowNull: false
  },
  horarioFim: {
    type: DataTypes.STRING(5),
    allowNull: false
  },
  local: {
    type: DataTypes.STRING(100),
    allowNull: false
  }
}, {
  tableName: 'plantoes',
  timestamps: true
});

module.exports = Plantao;
