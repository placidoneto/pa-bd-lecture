const medicoRoutes = require("./medico.routes");
const plantaoRoutes = require("./plantao.routes");

const router = [
  {
    method: "GET",
    path: "/",
    handler: (req, h) => {
      return { message: "API de Gerenciamento de Médicos e Plantões" };
    }
  },
  ...medicoRoutes,
  ...plantaoRoutes

//O spread (...) é equivalente a:
//   const router = [
//   { method: 'GET', path: '/' },
//   { method: 'GET', path: '/medicos' },
//   { method: 'POST', path: '/medicos' },
//   { method: 'GET', path: '/plantoes' }
// ];

];

module.exports = router;