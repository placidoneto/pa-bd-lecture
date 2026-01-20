const { DataTypes } = require('sequelize');
const sequelize = require('../utils/database');

const Medico = sequelize.define('Medico', {
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  nome: {
    type: DataTypes.STRING(100),
    allowNull: false
  },
  crm: {
    type: DataTypes.STRING(20),
    allowNull: false,
    unique: true // CRM único
  },
  especialidade: {
    type: DataTypes.STRING(50),
    allowNull: false
  }
}, {
  tableName: 'medicos',
  timestamps: true // createdAt, updatedAt
});

module.exports = Medico;
