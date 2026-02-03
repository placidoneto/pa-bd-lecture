# Koa

## Introdução

O **Koa** é um framework **open-source para Node.js** voltado para a criação de aplicações web e APIs **modernas, expressivas e minimalistas**. Criado pela mesma equipe responsável pelo Express.js, o Koa representa uma evolução conceitual no desenvolvimento de servidores HTTP em JavaScript, oferecendo uma base pequena, elegante e altamente extensível. Diferente de frameworks que já incluem funcionalidades prontas por padrão, o Koa entrega apenas o essencial, permitindo que o desenvolvedor construa sua aplicação escolhendo exatamente os componentes que precisa.

O uso intensivo de **async/await** e o modelo de middleware em cascata tornam o código mais legível, reduzem a dependência de callbacks aninhados e fortalecem o controle de fluxo e tratamento de erros de forma mais natural e previsível.

## A criação do Koa

### Sobre os criadores

O Koa foi lançado em **2014** por **TJ Holowaychuk** e sua equipe — os mesmos desenvolvedores que criaram o Express.js, framework que até hoje é um dos mais populares do ecossistema Node.js. TJ Holowaychuk é uma figura reconhecida na comunidade JavaScript, tendo criado diversas bibliotecas e ferramentas amplamente utilizadas, como Mocha (framework de testes), Commander (parser de linha de comando) e Jade (agora Pug, template engine).

A decisão de criar um novo framework, mesmo já tendo o Express consolidado, não foi arbitrária. Ela nasceu de limitações reais e de uma visão clara sobre como o desenvolvimento web em Node.js poderia evoluir com as novas funcionalidades da linguagem JavaScript.

### Problemas com o modelo tradicional de callbacks

Quando o Node.js e o Express surgiram, o JavaScript ainda não possuía suporte nativo para Promises ou async/await. O modelo dominante era o de **callbacks**, funções que são passadas como argumentos para serem executadas quando uma operação assíncrona é concluída.

Esse modelo funciona bem em cenários simples, mas em aplicações complexas, com múltiplas operações assíncronas encadeadas, rapidamente se transforma no que a comunidade passou a chamar de **"callback hell"** (inferno de callbacks) — código profundamente aninhado, difícil de ler, manter e debugar.

```javascript
// Exemplo de callback hell
app.get('/user/:id', function(req, res) {
  db.getUser(req.params.id, function(err, user) {
    if (err) return res.status(500).send(err);
    
    db.getUserPosts(user.id, function(err, posts) {
      if (err) return res.status(500).send(err);
      
      db.getPostComments(posts[0].id, function(err, comments) {
        if (err) return res.status(500).send(err);
        
        res.json({ user, posts, comments });
      });
    });
  });
});
```

Além da legibilidade comprometida, esse modelo também torna o tratamento de erros inconsistente. Cada callback precisa verificar erros manualmente, e a ausência de um mecanismo unificado aumenta o risco de falhas silenciosas.

### A chegada do async/await

Com a evolução do JavaScript, especialmente a partir do **ES2015 (ES6)** e **ES2017**, a linguagem ganhou suporte nativo para **Promises** e **async/await**. Essas funcionalidades permitiram escrever código assíncrono de forma mais próxima à lógica síncrona tradicional, eliminando a necessidade de callbacks aninhados e centralizando o tratamento de erros com `try/catch`.

O mesmo exemplo anterior, reescrito com async/await, fica significativamente mais simples e legível:

```javascript
// Código moderno com async/await
app.get('/user/:id', async (req, res) => {
  try {
    const user = await db.getUser(req.params.id);
    const posts = await db.getUserPosts(user.id);
    const comments = await db.getPostComments(posts[0].id);
    
    res.json({ user, posts, comments });
  } catch (err) {
    res.status(500).send(err);
  }
});
```

O Express, por ter sido criado antes dessas funcionalidades existirem, foi construído sobre o modelo de callbacks. Embora seja possível usar async/await no Express, o framework não foi projetado com essa abordagem em mente desde o início, o que resulta em uma experiência menos natural e idiomática.

### Koa como resposta a essas limitações

Foi nesse contexto que o Koa surgiu. Em vez de tentar adaptar o Express para o novo paradigma, TJ Holowaychuk e sua equipe decidiram criar um framework completamente novo, projetado desde a base para aproveitar ao máximo as capacidades modernas do JavaScript.

O Koa não é apenas "Express com async/await". Ele representa uma reformulação conceitual de como middlewares devem funcionar, de como o contexto de requisição e resposta deve ser tratado, e de como o desenvolvedor interage com o ciclo de vida de uma requisição HTTP.

## A filosofia do Koa

### Minimalismo e núcleo enxuto

O Koa segue uma filosofia radicalmente minimalista. Enquanto o Express já inclui funcionalidades como roteamento, parsing de requisições e handling de cookies por padrão, o Koa entrega apenas o **núcleo essencial** — um sistema de middlewares e o objeto de contexto.

Isso não significa que o Koa seja menos capaz. Na verdade, é justamente o contrário: ao não impor decisões arquiteturais ou incluir funcionalidades que podem não ser necessárias, o Koa oferece maior **flexibilidade** e **controle** ao desenvolvedor. Quer usar um roteador específico? Escolha o que preferir. Precisa de validação de dados? Integre a biblioteca que melhor se adequa ao seu projeto.

Essa abordagem resulta em um framework com tamanho reduzido — o core do Koa tem aproximadamente **550 linhas de código** e **~500KB** após instalação, comparado aos vários megabytes de um Express com suas dependências.

### Configuração explícita

Outra característica importante do Koa é a preferência por **configuração explícita** em vez de comportamentos implícitos ou "mágicos". No Express, por exemplo, é comum que comportamentos sejam definidos globalmente através de middlewares que afetam todas as rotas. No Koa, a tendência é que cada comportamento seja declarado de forma clara e localizada.

Isso não elimina a possibilidade de usar middlewares globais, mas incentiva uma arquitetura onde decisões críticas — como autenticação, validação ou timeout — sejam visíveis no ponto onde realmente importam.

## Pré-requisitos e instalação

Antes de começar com o Koa, é importante garantir que o ambiente de desenvolvimento esteja preparado. O Koa depende do **Node.js**, o runtime JavaScript que permite a execução de código JavaScript fora do navegador.

### Requisitos do sistema

O Koa requer **Node.js versão 18.0.0 ou superior**. Isso se deve ao uso de funcionalidades modernas do JavaScript, especialmente async functions. Para 2026, recomenda-se utilizar as versões LTS 20.x ou 22.x, que garantem maior estabilidade e compatibilidade.

Para verificar se o Node.js está instalado e qual versão está ativa:

```bash
node --version
```

Caso seja necessário gerenciar múltiplas versões do Node.js, ferramentas como **nvm** (Node Version Manager) facilitam esse processo:

```bash
nvm install 20
nvm use 20
```

### Criando um projeto

O ponto de partida é criar um diretório para o projeto e inicializá-lo como uma aplicação Node.js:

```bash
mkdir projeto-koa
cd projeto-koa
npm init -y
```

O comando `npm init -y` cria o arquivo `package.json`, que organiza as dependências e metadados do projeto. Em seguida, o Koa pode ser instalado:

```bash
npm install koa
```

Esse comando adiciona o core do Koa ao projeto. Para funcionalidades adicionais, como roteamento e parsing de requisições, outras bibliotecas podem ser instaladas conforme necessário:

```bash
npm install @koa/router koa-bodyparser
```

A partir desse momento, o projeto já possui tudo o que é necessário para criar um servidor funcional.

## Estrutura de um projeto básico em Koa

Com o ambiente configurado e o Koa instalado, o próximo passo é entender como construir um servidor básico. Diferente de soluções que exigem estruturas complexas desde o início, o Koa permite começar de forma simples, evoluindo conforme a aplicação cresce.

### Criando o servidor

No Koa, o servidor é o elemento central da aplicação. Ele é responsável por escutar requisições, executar middlewares e orquestrar o ciclo de vida de cada requisição HTTP.

Um exemplo mínimo de servidor pode ser criado em um arquivo `index.js`:

```javascript
const Koa = require('koa');
const app = new Koa();

app.use(async (ctx) => {
  ctx.body = 'Hello World';
});

app.listen(3000, () => {
  console.log('Servidor rodando na porta 3000');
});
```

Neste exemplo, quando uma requisição chega ao servidor, o middleware definido é executado. O objeto `ctx` (contexto) encapsula tanto a requisição quanto a resposta, e o middleware define o corpo da resposta como "Hello World".

Para executar o servidor:

```bash
node index.js
```

Acessando `http://localhost:3000` no navegador, a resposta "Hello World" será exibida.

### Entendendo o contexto (ctx)

O objeto de contexto é um dos conceitos mais importantes do Koa. Ele encapsula os objetos de requisição e resposta do Node.js, oferecendo uma interface mais limpa e direta para interagir com a requisição HTTP.

Em vez de trabalhar com `req` e `res` separadamente (como no Express), no Koa tudo está acessível através de `ctx`:

```javascript
app.use(async (ctx) => {
  // Informações da requisição
  console.log(ctx.method);      // GET, POST, etc
  console.log(ctx.url);          // URL da requisição
  console.log(ctx.headers);      // Cabeçalhos HTTP
  
  // Definindo a resposta
  ctx.status = 200;              // Status HTTP
  ctx.body = { message: 'OK' };  // Corpo da resposta
});
```

Além disso, o contexto oferece métodos auxiliares úteis:

```javascript
app.use(async (ctx) => {
  // Lançar erro HTTP
  if (!ctx.query.id) {
    ctx.throw(400, 'ID é obrigatório');
  }
  
  // Manipular cookies
  const userId = ctx.cookies.get('user_id');
  ctx.cookies.set('session', 'abc123');
  
  // Estado compartilhado entre middlewares
  ctx.state.user = { id: 1, name: 'João' };
});
```

O campo `ctx.state` é especialmente útil para passar informações entre middlewares, como dados de autenticação processados em um middleware anterior.

## Conceitos fundamentais

### Middlewares e o modelo em cascata

O conceito de middleware não é exclusivo do Koa — ele existe em praticamente todos os frameworks web. Um middleware é essencialmente uma função que fica no meio do caminho entre a requisição do cliente e a resposta do servidor. Ele pode executar código, modificar a requisição ou resposta, e decidir se a execução deve continuar ou ser interrompida.

No Express, middlewares são executados em sequência linear. Cada middleware chama `next()` para passar o controle para o próximo, mas não há uma forma natural de executar código após todos os middlewares downstream terem sido processados.

O Koa introduz o conceito de **middleware em cascata** (cascade middleware). Nesse modelo, quando um middleware chama `await next()`, a execução é pausada, os middlewares seguintes são executados, e então a execução retorna ao ponto onde foi pausada. Isso cria um fluxo bidirecional — **downstream** (descendo a cadeia) e **upstream** (subindo de volta).

#### Visualizando o fluxo em cascata

```
Requisição chega ao servidor
        ↓
  Middleware 1 (antes do await next())
        ↓
  Middleware 2 (antes do await next())
        ↓
  Middleware 3 (antes do await next())
        ↓
  Middleware 4 (executa e define resposta)
        ↓
  Middleware 3 (depois do await next())
        ↓
  Middleware 2 (depois do await next())
        ↓
  Middleware 1 (depois do await next())
        ↓
Resposta enviada ao cliente
```

Esse modelo permite implementar padrões que seriam complexos ou verbosos em outros frameworks. Por exemplo, medir o tempo de execução de uma requisição:

```javascript
app.use(async (ctx, next) => {
  const start = Date.now();
  
  await next();  // Executa os próximos middlewares
  
  const duration = Date.now() - start;
  console.log(`${ctx.method} ${ctx.url} - ${duration}ms`);
});
```

Neste exemplo, o middleware registra o momento inicial, passa o controle adiante, e quando todos os middlewares posteriores terminam, calcula e registra o tempo total de execução. Isso só é possível porque o código após `await next()` é executado quando a resposta já foi processada.

### Tratamento de erros

O uso de async/await torna o tratamento de erros mais natural e previsível. No Koa, erros podem ser capturados usando blocos `try/catch` padrão do JavaScript:

```javascript
app.use(async (ctx, next) => {
  try {
    await next();
  } catch (err) {
    ctx.status = err.status || 500;
    ctx.body = {
      error: err.message
    };
    
    // Log do erro
    console.error('Erro capturado:', err);
  }
});
```

Esse middleware atua como um **error boundary** global, capturando qualquer erro lançado pelos middlewares subsequentes e tratando-o de forma centralizada.

O Koa também oferece um mecanismo de eventos para tratamento de erros:

```javascript
app.on('error', (err, ctx) => {
  console.error('Erro no servidor:', err);
  // Aqui você pode enviar logs para serviços externos,
  // notificar equipes, etc.
});
```

Além disso, o método `ctx.throw()` permite lançar erros HTTP de forma conveniente:

```javascript
app.use(async (ctx) => {
  const { id } = ctx.query;
  
  if (!id) {
    ctx.throw(400, 'O parâmetro ID é obrigatório');
  }
  
  const user = await db.findUser(id);
  
  if (!user) {
    ctx.throw(404, 'Usuário não encontrado');
  }
  
  ctx.body = user;
});
```

## Construindo uma aplicação real

Para demonstrar como esses conceitos se aplicam na prática, vamos construir uma aplicação funcional com rotas, validação e tratamento de erros.

### Adicionando roteamento

O core do Koa não inclui um sistema de rotas. Isso é intencional — permite que o desenvolvedor escolha a solução que melhor se adequa ao projeto. A biblioteca oficial `@koa/router` é a opção mais comum:

```bash
npm install @koa/router
```

Com o router instalado, podemos definir rotas de forma clara e organizada:

```javascript
const Koa = require('koa');
const Router = require('@koa/router');

const app = new Koa();
const router = new Router();

// Rota GET simples
router.get('/', async (ctx) => {
  ctx.body = { message: 'Bem-vindo à API Koa' };
});

// Rota com parâmetros
router.get('/users/:id', async (ctx) => {
  const { id } = ctx.params;
  ctx.body = { 
    userId: id, 
    name: 'João Silva' 
  };
});

// Rota POST
router.post('/users', async (ctx) => {
  const userData = ctx.request.body;
  ctx.status = 201;
  ctx.body = { 
    id: Date.now(), 
    ...userData,
    created_at: new Date()
  };
});

// Registrar as rotas no app
app.use(router.routes());
app.use(router.allowedMethods());

app.listen(3000);
```

O método `router.allowedMethods()` adiciona tratamento automático para métodos HTTP não permitidos, respondendo com status 405 quando apropriado.

### Parsing de requisições

Para processar dados enviados no corpo de requisições POST ou PUT, precisamos de um middleware para fazer o parsing. O `koa-bodyparser` é a solução mais utilizada:

```bash
npm install koa-bodyparser
```

Ele deve ser registrado antes das rotas:

```javascript
const Koa = require('koa');
const Router = require('@koa/router');
const bodyParser = require('koa-bodyparser');

const app = new Koa();
const router = new Router();

// Importante: bodyParser deve vir antes das rotas
app.use(bodyParser());

router.post('/users', async (ctx) => {
  const { name, email } = ctx.request.body;
  
  // Agora os dados do body estão disponíveis
  ctx.body = { name, email };
});

app.use(router.routes());
app.listen(3000);
```

### Validação de dados

Validar dados de entrada é fundamental para a segurança e consistência da aplicação. Uma abordagem comum é usar bibliotecas como **Zod** ou **Joi**. Vamos usar o Zod como exemplo:

```bash
npm install zod
```

```javascript
const { z } = require('zod');

// Definir o schema de validação
const userSchema = z.object({
  name: z.string().min(3, 'Nome deve ter pelo menos 3 caracteres'),
  email: z.string().email('Email inválido'),
  age: z.number().int().min(18, 'Idade mínima é 18 anos')
});

router.post('/users', async (ctx) => {
  try {
    // Validar os dados recebidos
    const userData = userSchema.parse(ctx.request.body);
    
    // Se chegou aqui, os dados são válidos
    ctx.status = 201;
    ctx.body = {
      id: Date.now(),
      ...userData,
      created_at: new Date()
    };
  } catch (err) {
    // Dados inválidos
    ctx.status = 400;
    ctx.body = {
      error: 'Dados inválidos',
      details: err.errors
    };
  }
});
```

### Exemplo completo

Reunindo todos os conceitos apresentados, um servidor Koa funcional ficaria assim:

```javascript
const Koa = require('koa');
const Router = require('@koa/router');
const bodyParser = require('koa-bodyparser');
const { z } = require('zod');

const app = new Koa();
const router = new Router();

// Middleware de tratamento de erros
app.use(async (ctx, next) => {
  try {
    await next();
  } catch (err) {
    ctx.status = err.status || 500;
    ctx.body = {
      error: err.message
    };
    app.emit('error', err, ctx);
  }
});

// Middleware de logging
app.use(async (ctx, next) => {
  const start = Date.now();
  await next();
  const duration = Date.now() - start;
  console.log(`${ctx.method} ${ctx.url} - ${ctx.status} - ${duration}ms`);
});

// Body parser
app.use(bodyParser());

// Schema de validação
const userSchema = z.object({
  name: z.string().min(3),
  email: z.string().email()
});

// Rotas
router.get('/', async (ctx) => {
  ctx.body = { message: 'API Koa funcionando' };
});

router.get('/users/:id', async (ctx) => {
  const { id } = ctx.params;
  
  // Simular busca no banco de dados
  const user = { id, name: 'João Silva', email: 'joao@example.com' };
  
  ctx.body = user;
});

router.post('/users', async (ctx) => {
  const userData = userSchema.parse(ctx.request.body);
  
  ctx.status = 201;
  ctx.body = {
    id: Date.now(),
    ...userData,
    created_at: new Date()
  };
});

// Registrar rotas
app.use(router.routes());
app.use(router.allowedMethods());

// Tratamento de erros global
app.on('error', (err, ctx) => {
  console.error('Erro no servidor:', err);
});

app.listen(3000, () => {
  console.log('Servidor rodando na porta 3000');
});
```

Este exemplo demonstra:
- Middleware de tratamento de erros centralizado
- Logging de requisições com medição de tempo
- Parsing de corpo de requisições
- Validação de dados com Zod
- Rotas parametrizadas e manipulação de contexto
- Tratamento de eventos de erro

## Express vs Koa — uma comparação conceitual

Entender as diferenças entre Express e Koa vai além de comparar linhas de código ou performance. São frameworks com filosofias distintas, cada um adequado a diferentes contextos e necessidades.

### Filosofia e design

O **Express** segue uma filosofia de "bateria incluída". Ele oferece funcionalidades prontas para uso imediato, como roteamento integrado, parsing de requisições e serving de arquivos estáticos. Isso torna o Express uma escolha rápida para começar projetos, especialmente para desenvolvedores iniciantes.

O **Koa**, por outro lado, adota uma filosofia minimalista. O core é extremamente pequeno, e funcionalidades adicionais são adicionadas apenas quando necessárias. Isso resulta em maior controle e flexibilidade, mas exige que o desenvolvedor tome mais decisões arquiteturais.

### Modelo de middlewares

No **Express**, middlewares são executados em sequência linear. Uma vez que `next()` é chamado, não há retorno natural ao middleware que o invocou:

```javascript
// Express
app.use((req, res, next) => {
  console.log('Antes');
  next();
  // Este código é executado, mas a resposta pode já ter sido enviada
  console.log('Depois');
});
```

No **Koa**, o modelo em cascata permite controle explícito sobre quando executar código antes e depois dos middlewares subsequentes:

```javascript
// Koa
app.use(async (ctx, next) => {
  console.log('Antes');
  await next();
  // Este código é executado SEMPRE depois de todos os middlewares seguintes
  console.log('Depois');
});
```

Essa diferença torna padrões como logging, medição de tempo, transações de banco de dados e controle de cache mais naturais no Koa.

### Async/await

Embora seja possível usar async/await no Express, o framework não foi projetado com isso em mente. É comum encontrar problemas com tratamento de erros em funções assíncronas, exigindo wrappers ou bibliotecas adicionais.

O Koa foi construído desde o início para async/await. Todo o ciclo de vida da requisição é assíncrono por padrão, e o tratamento de erros funciona naturalmente com `try/catch`.

### Quando usar cada um

**Use Express quando:**
- Você precisa começar rapidamente com convenções estabelecidas
- O projeto é pequeno ou médio e não requer customização profunda
- A equipe já tem experiência consolidada com Express
- Você valoriza o ecossistema maduro e a grande quantidade de middlewares disponíveis

**Use Koa quando:**
- Você deseja controle fino sobre o comportamento da aplicação
- O projeto valoriza código limpo e moderno (async/await nativo)
- Você prefere escolher explicitamente cada componente da stack
- O modelo de middleware em cascata beneficia seus casos de uso

| Aspecto | Express | Koa |
|---------|---------|-----|
| Filosofia | Completo, com baterias incluídas | Minimalista, núcleo enxuto |
| Tamanho | Médio (~1MB com deps) | Pequeno (~500KB) |
| Middlewares | Lineares, unidirecionais | Cascata, bidirecionais |
| Async/await | Suporte posterior, não nativo | Nativo, projetado para isso |
| Contexto | `req` e `res` separados | `ctx` unificado |
| Curva de aprendizado | Menor, mais popular | Média, conceitos novos |
| Ecossistema | Muito maduro e extenso | Crescente, mais moderno |
| Uso ideal | Apps full-featured, MVCs | APIs modernas, microserviços |

## Middlewares populares no ecossistema Koa

Embora o core do Koa seja minimalista, existe um ecossistema crescente de middlewares que estendem suas funcionalidades.

### Stack recomendada para produção

```bash
npm install @koa/router koa-bodyparser @koa/cors koa-helmet koa-compress koa-jwt
```

Cada um desses middlewares adiciona funcionalidades essenciais:

- **@koa/router**: Sistema de rotas completo
- **koa-bodyparser**: Parsing de JSON e form data
- **@koa/cors**: Configuração de CORS
- **koa-helmet**: Headers de segurança HTTP
- **koa-compress**: Compressão de respostas (gzip)
- **koa-jwt**: Autenticação via JSON Web Tokens

### Exemplo de integração completa

```javascript
const Koa = require('koa');
const Router = require('@koa/router');
const bodyParser = require('koa-bodyparser');
const cors = require('@koa/cors');
const helmet = require('koa-helmet');
const compress = require('koa-compress');

const app = new Koa();

// Segurança: adiciona headers HTTP seguros
app.use(helmet());

// Compressão de resposta
app.use(compress());

// CORS: permite requisições cross-origin
app.use(cors());

// Body parsing
app.use(bodyParser());

// Suas rotas
const router = new Router();
router.get('/api/status', (ctx) => {
  ctx.body = { status: 'ok' };
});

app.use(router.routes());
app.listen(3000);
```

## Casos de uso reais

O Koa é especialmente adequado para certos tipos de aplicações e contextos de desenvolvimento.

### APIs REST e microserviços

O design minimalista e o controle fino sobre o comportamento da aplicação tornam o Koa ideal para construir APIs REST limpas e microserviços eficientes. A facilidade de adicionar apenas os componentes necessários resulta em aplicações enxutas e performáticas.

### Integração com bancos de dados

O Koa se integra naturalmente com ORMs modernos como **Prisma** e **TypeORM**, que também são projetados com async/await em mente:

```javascript
router.get('/users/:id', async (ctx) => {
  const user = await prisma.user.findUnique({
    where: { id: ctx.params.id }
  });
  
  if (!user) {
    ctx.throw(404, 'Usuário não encontrado');
  }
  
  ctx.body = user;
});
```

### Performance e benchmarks

Segundo benchmarks do TechEmpower (2025), o Koa apresenta performance sólida:

- **Koa**: ~20.000 requisições/segundo
- **Express**: ~15.000 requisições/segundo  
- **Fastify**: ~30.000+ requisições/segundo

O Koa oferece excelente balanço entre performance e simplicidade de código, posicionando-se como uma escolha intermediária para quem valoriza código limpo sem sacrificar demais a velocidade.

## Conclusão

O Koa representa uma visão moderna de como frameworks web em Node.js devem ser construídos. Em vez de tentar ser tudo para todos, ele foca em entregar um núcleo sólido, pequeno e bem projetado, sobre o qual aplicações complexas podem ser construídas.

Suas principais contribuições ao ecossistema Node.js são:

- O modelo de **middleware em cascata**, que permite padrões mais expressivos e controlados
- A adoção completa de **async/await** desde o início, resultando em código mais limpo e tratamento de erros mais natural
- A filosofia de **configuração explícita**, que torna o comportamento da aplicação mais previsível
- O **núcleo minimalista**, que dá ao desenvolvedor liberdade para escolher exatamente os componentes que precisa

O Koa não é necessariamente melhor ou pior que Express ou Fastify — ele é diferente, com propósitos e públicos distintos. Para desenvolvedores que valorizam controle, modernidade e código limpo, e que não se importam em montar sua própria stack de componentes, o Koa é uma escolha natural e recompensadora.

## Referências

1. **Koa - Next Generation Web Framework for Node.js**  
   Documentação oficial. Disponível em: https://koajs.com/

2. **Holowaychuk, T. J. (2014)**  
   Koa: Express.js next generation web framework.  
   GitHub Repository. Disponível em: https://github.com/koajs/koa

3. **Node.js Foundation**  
   Documentação oficial do Node.js. Disponível em: https://nodejs.org/docs/

4. **MDN Web Docs**  
   Async/Await em JavaScript. Disponível em: https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Asynchronous

5. **TechEmpower**  
   Web Framework Performance Benchmarks. Disponível em: https://www.techempower.com/benchmarks/
