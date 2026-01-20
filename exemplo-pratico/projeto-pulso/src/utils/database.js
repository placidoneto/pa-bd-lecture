const { Sequelize } = require('sequelize');

// SQLite em arquivo - simples e didático
const sequelize = new Sequelize({
  dialect: 'sqlite',
  storage: './database.sqlite',
  logging: false // Desabilita logs SQL no console
});

module.exports = sequelize;
