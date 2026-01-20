const server = require("./src/utils/server");
const sequelize = require("./src/utils/database");

(async () => {
  try {
    // Sincronizar banco de dados
    await sequelize.sync({ force: false }); // force: true recria as tabelas
    console.log('Banco de dados sincronizado');
    
    // Iniciar servidor
    await server.start();
    console.log('Servidor rodando em:', server.info.uri);
  } catch (error) {
    console.error('Erro ao iniciar:', error);
    process.exit(1);
  }
})();