# Hapi

## Introdução

O **Hapi** é um framework **open-source para Node.js** voltado para a criação de aplicações backend **poderosas, escaláveis e organizadas**, com baixa sobrecarga e foco na simplicidade. Ele oferece uma **funcionalidade completa pronta para uso**, permitindo que o desenvolvedor concentre seus esforços na resolução dos problemas do negócio, e não nos detalhes da ferramenta. Sua arquitetura fornece um conjunto sólido de **APIs centrais** e um sistema de **plugins extensíveis**, tornando-o uma escolha confiável para aplicações de **nível empresarial**.

## A criação do Hapi

### Sobre o criador

O **Hapi não surgiu do nada**. Ele é resultado direto de problemas reais enfrentados em ambientes corporativos de grande escala. Seu criador, **Eran Hammer**, é um engenheiro e executivo de tecnologia com mais de trinta anos de experiência, tendo passado por empresas como **Yahoo, Citi e Walmart eCommerce**, onde atuou como diretor de serviços móveis. Diferente do perfil tradicional da área, Hammer possui formação em **cinema e estudos audiovisuais**, o que contribuiu para uma visão mais estrutural e narrativa sobre sistemas — pensando menos em “código isolado” e mais em **arquiteturas coerentes e previsíveis**.

Além disso, Hammer foi um dos **coautores do OAuth**, um protocolo amplamente utilizado para **autenticação e autorização na web** (ou seja, definir quem é o usuário e o que ele pode acessar). Essa experiência com padrões de segurança influenciou profundamente o design do Hapi, que nasceu com uma filosofia **“security-first” (segurança em primeiro lugar)**.

> No Hapi, comportamentos críticos não ficam escondidos ou implícitos: tudo é **configurado de forma explícita**, reduzindo erros e aumentando a previsibilidade da aplicação. Em vez disso, o framework incentiva que essas regras sejam configuradas de forma explícita, diretamente nos pontos onde elas realmente importam. Isso significa que decisões como exigir autenticação, validar dados de entrada ou aplicar restrições de segurança são declaradas de maneira clara e centralizada, evitando que essas regras fiquem espalhadas pelo código.

#### Exemplo comum no Express (implícito)

```js
app.use(authMiddleware);
app.use(validationMiddleware);

app.post("/users", (req, res) => {
  // lógica de criação do usuário
});
```

#### O mesmo cenário no Hapi (explícito)

```js
server.route({
  method: "POST",
  path: "/users",
  options: {
    auth: "jwt", // autenticação explícita
    validate: {
      payload: {
        name: Joi.string().required(),
        email: Joi.string().email().required()
      }
    }
  },
  handler: (request, h) => {
    // lógica de criação do usuário
    return { success: true };
  }
});
```

### Problemas com o Express

Inicialmente, o Hapi **não foi pensado como um framework público**. A equipe do Walmart Labs tentou usar o **Express.js**, que na época era o framework Node.js mais popular. 

O Express é um framework **minimalista**, inspirado no Sinatra (Ruby), cujo principal mecanismo de extensão é o uso de **middlewares**. Middlewares podem ser aplicados de forma **global, por grupo de rotas** ou **rota a rota**, e o comportamento final da aplicação depende da **ordem em que esses middlewares são registrados**. 

Isso significa que regras importantes não ficam declaradas junto da rota, mas espalhadas pelo código, exigindo que o desenvolvedor conheça toda a cadeia de execução para entender o que realmente acontece em uma requisição.

> Um middleware é, de forma simples, uma **função que fica no meio do caminho entre a requisição do usuário e a resposta do servidor**. Ele pode verificar autenticação, validar dados, registrar logs ou modificar a requisição antes que ela chegue à lógica principal da aplicação. Esse modelo é poderoso, mas também traz desafios quando utilizado em larga escala.

```js
app.use(authMiddleware);
app.use(validationMiddleware);

app.post("/users", (req, res) => {
  // lógica de criação do usuário
});
```
Nesse exemplo, não é possível saber apenas olhando para a rota:
- se ela exige autenticação ou não
- quais dados estão sendo validados
- em que ponto essas regras são aplicadas

Para entender o comportamento completo, é necessário:
- localizar os middlewares
- entender sua lógica interna
- verificar a ordem em que foram registrados

Em projetos pequenos, isso raramente é um problema. Porém, em **ambientes corporativos**, com **múltiplas equipes trabalhando simultaneamente**, esse modelo tende a gerar inconsistências. Cada equipe pode criar seus próprios middlewares, aplicar regras de formas diferentes e organizar rotas segundo critérios próprios. Com o tempo, surgem **múltiplos padrões dentro do mesmo sistema**, dificultando manutenção, testes e auditorias de segurança.

Foi justamente essa falta de **estrutura clara e previsível**, aliada à necessidade de lidar com **grandes volumes de tráfego** e **requisitos rigorosos de segurança**, que levou à percepção de que o Express, embora excelente para projetos menores, não atendia às necessidades reais de um ambiente corporativo.

### Black Friday

Os problemas com o Express ficaram ainda mais evidentes em eventos de tráfego extremo, como a **Black Friday**. O Walmart precisava de sistemas capazes de lidar com **milhões de requisições simultâneas**, mantendo **segurança consistente, deploys confiáveis** e **facilidade de testes e auditoria**. Nesse cenário, depender de múltiplos middlewares de terceiros para funções críticas tornava o Express **inseguro, inconsistente e difícil de controlar**.

> Essa insegurança não vinha apenas do volume de tráfego, mas da dependência de múltiplos middlewares de terceiros para funções críticas. Cada middleware seguia padrões próprios, com níveis diferentes de maturidade e decisões de segurança independentes, fragmentando a proteção da aplicação. Em ambientes de alta carga, como a Black Friday, essa combinação de dependências externas, configurações distribuídas e ausência de um modelo de segurança centralizado aumentava significativamente o risco de falhas e vulnerabilidades.

## A consolidação do Hapi como framework

### Hapi como solução para problemas reais

Com os problemas claramente identificados e os objetivos bem definidos, o Hapi deixa de ser apenas uma solução pontual e passa a se estruturar como um **framework completo**. A partir desse momento, suas decisões deixam de ser reativas e passam a formar uma **arquitetura consistente**, guiada por princípios claros de organização, segurança e previsibilidade.

O foco do Hapi não era apenas resolver o problema imediato do alto volume de requisições, mas criar uma base capaz de **sustentar sistemas complexos ao longo do tempo**. Para isso, o framework consolida escolhas que evitam ambiguidades e reduzem a margem de erro humano, especialmente em ambientes com múltiplas equipes e ciclos frequentes de deploy.

Nesse estágio, o Hapi já não se posiciona como uma alternativa genérica dentro do ecossistema Node.js, mas como uma ferramenta com identidade própria, voltada a cenários onde **clareza arquitetural, segurança e controle** não são opcionais, mas requisitos fundamentais.

### Como o Hapi resolve esses problemas

O Hapi resolve as limitações observadas por meio de quatro decisões arquiteturais centrais: **configuração explícita, arquitetura baseada em plugins, segurança integrada ao núcleo do framework e escalabilidade**. Esses elementos não são recursos isolados, mas partes de um modelo coeso que define como uma aplicação deve se comportar desde o início.

#### Configuração explícita (configuração sobre código)

No Hapi, decisões críticas não ficam escondidas em middlewares globais ou na ordem de execução da aplicação. Em vez disso, o comportamento de cada rota é descrito de forma declarativa, diretamente em sua configuração. Autenticação, validação de dados, estratégias de cache e limites de requisição são definidos de maneira explícita, permitindo que qualquer pessoa entenda o funcionamento de uma rota apenas lendo sua definição.

```js
server.route({
  method: "POST",
  path: "/upload",
  options: {
    payload: {
      maxBytes: 1024 * 1024, // 1 MB
      timeout: 5000
    }
  },
  handler: () => ({ status: "recebido" })
});
```

Aqui, o comportamento da rota em relação ao tamanho do corpo da requisição e ao tempo limite é declarado diretamente na configuração da rota.

#### Arquitetura baseada em plugins

Outra forma pela qual o Hapi soluciona problemas de escala organizacional é por meio de uma arquitetura baseada em plugins. Em vez de concentrar lógica em arquivos centrais ou espalhar responsabilidades pelo código, funcionalidades são agrupadas em módulos independentes.

Plugins não representam um padrão arquitetural da aplicação, mas um **mecanismo do próprio framework para organizar e registrar comportamentos HTTP**. Eles funcionam como unidades de infraestrutura responsáveis por conectar partes da aplicação ao servidor.

> Um plugin pode registrar rotas, definir validações, configurar autenticação ou estender o ciclo de vida da requisição. Ele não substitui arquiteturas como camadas, MVC ou Clean Architecture — essas continuam existindo dentro da aplicação. O papel do plugin é apenas **encapsular como essas partes são expostas e configuradas no servidor**.

```cmd
Servidor Hapi
   │
   ├── Plugin Users
   │     └── registra rotas /users
   │
   ├── Plugin Auth
   │     └── registra autenticação
   │
   └── Plugin Health
         └── registra /health
```

Essa separação é especialmente útil em projetos grandes. Em vez de concentrar todas as rotas e configurações em arquivos centrais, cada módulo funcional pode registrar seu próprio comportamento de forma isolada. Isso reduz conflitos entre equipes, melhora a legibilidade do sistema e torna o crescimento da aplicação mais previsível.

#### Segurança integrada ao núcleo

Diferente do Express, onde segurança depende fortemente de middlewares externos, o Hapi trata autenticação, autorização e validação como partes fundamentais do framework. Estratégias de autenticação são registradas de forma centralizada e aplicadas explicitamente às rotas que precisam delas.

A validação de entrada é feita antes da execução da lógica de negócio, garantindo que dados inválidos não cheguem ao core da aplicação. Mensagens de erro, cabeçalhos HTTP, limites de payload e timeouts seguem padrões seguros por padrão, reduzindo o risco de falhas de configuração.

#### Escalabilidade e previsibilidade em alta carga

O Hapi foi projetado para escalar não apenas em volume de requisições, mas também em complexidade estrutural. Em vez de depender de convenções informais ou de cadeias dinâmicas de middlewares, o framework define um ciclo de vida de requisição bem estruturado, com pontos claros de extensão e comportamento determinístico. Isso garante que, mesmo sob milhões de requisições simultâneas, o fluxo de execução permaneça previsível e controlável.

Além disso, o Hapi oferece mecanismos nativos para controle de carga, como limites de payload, timeouts configuráveis, controle de concorrência e cache integrado, permitindo que a aplicação se proteja contra abuso e degradação de desempenho sem depender de soluções externas.

## Express vs Hapi — uma comparação conceitual

| Aspecto | Express.js | Hapi |
|---------|------------|------|
| Filosofia | Minimalista e flexível | Opinativo e estruturado |
| Organização | Definida pelo desenvolvedor | Definida pelo framework |
| Autenticação | Via middlewares externos | Integrada ao core |
| Validação de dados | Bibliotecas externas | Nativa e declarativa |
| Fluxo de execução | Dependente da ordem dos middlewares | Explícito e previsível |
| Escalabilidade organizacional | Difícil em equipes grandes | Pensado para ambientes corporativos |
| Auditoria e testes | Complexos em sistemas grandes | Facilitados pela centralização |

Essa comparação evidencia que o Hapi não tenta substituir o Express em todos os cenários, mas atender **a um tipo específico de problema**.


## Pré-requisitos e primeiro passo com Hapi

Antes de qualquer linha de código com Hapi, é importante entender o que sustenta o framework e o que é necessário para que ele funcione corretamente no ambiente de desenvolvimento.

O Hapi é construído sobre o **Node.js**, o runtime JavaScript que permite a execução de aplicações fora do navegador. Em outras palavras, o Hapi não funciona de forma isolada: ele depende diretamente do Node para existir. Sem o Node.js, não há servidor, não há rotas e não há aplicação — da mesma forma que não é possível executar Java sem a JVM.

Além do runtime, o Node.js já inclui o **npm**, que é o gerenciador de pacotes responsável por instalar bibliotecas, frameworks e plugins utilizados no projeto, incluindo o próprio Hapi. É por meio dele que o ecossistema Node se mantém organizado e reutilizável.

Por esse motivo, o primeiro requisito para trabalhar com Hapi é ter o Node.js instalado corretamente na máquina. Recomenda-se utilizar a versão **LTS** mais recente, disponível no site oficial, garantindo maior estabilidade e compatibilidade com o framework. O processo de instalação varia de acordo com o sistema operacional (Windows, macOS ou Linux).

Após a instalação, é possível verificar se o ambiente está pronto executando os seguintes comandos no terminal:

```bash
node -v   # exibe a versão instalada do Node.js
npm -v    # exibe a versão do npm
```

Com o ambiente configurado, o próximo passo é entender como nasce um projeto básico utilizando o framework. O ponto de partida é a criação de um diretório para o projeto. Esse diretório irá concentrar o código da aplicação, suas dependências e configurações.

```bash
mkdir projeto-hapi
cd projeto-hapi
```

Dentro desse diretório, o projeto deve ser inicializado como uma aplicação Node.js, criando o arquivo `package.json`, que será responsável por organizar as dependências e metadados do projeto:

```bash
npm init
```

Em seguida, o Hapi pode ser instalado como dependência do projeto:

```bash
npm install @hapi/hapi
```

Esse comando adiciona o core do Hapi ao package.json e torna possível começar a definir o servidor, as rotas e o sistema de plugins. A partir desse momento, o projeto já possui tudo o que é necessário para criar um servidor funcional.

## Estrutura de um projeto básico em Hapi

Com o ambiente configurado e o Hapi instalado, o próximo passo é entender como nasce um projeto básico utilizando o framework. Diferente de soluções que exigem estruturas complexas logo de início, o Hapi permite começar de forma simples, evoluindo conforme a aplicação cresce.

### Criando o servidor

No Hapi, o servidor é o elemento central da aplicação. Ele é responsável por escutar requisições, aplicar configurações globais e orquestrar rotas, plugins e políticas de segurança.

Um exemplo mínimo de criação de servidor pode ser feito em um arquivo como ```index.js```:

```js
'use strict';

const Hapi = require('@hapi/hapi');

const init = async () => {

    const server = Hapi.server({
        port: 3000,
        host: 'localhost'
    });

    await server.start();
    console.log('Server running on %s', server.info.uri);
};

process.on('unhandledRejection', (err) => {

    console.log(err);
    process.exit(1);
});

init();
```

Nesse trecho, o servidor é instanciado de forma explícita, informando a porta e o host em que a aplicação irá rodar. O uso de uma função assíncrona permite que o processo de inicialização seja controlado com segurança, tratando possíveis erros durante a execução.

Ao executar o arquivo com node ```index.js```, o servidor passa a escutar requisições na porta definida, mesmo sem ainda possuir rotas configuradas.

### Definindo rotas

Com o servidor criado, o próximo passo é definir rotas. No Hapi, as rotas são declaradas de forma explícita, associando método HTTP, caminho e lógica de tratamento em um único ponto. Isso reforça a filosofia do framework de tornar o comportamento da aplicação previsível e fácil de entender.

Um exemplo simples de rota pode ser adicionado ao mesmo arquivo:

```js
'use strict';

const Hapi = require('@hapi/hapi');

const init = async () => {

    const server = Hapi.server({
        port: 3000,
        host: 'localhost'
    });

    server.route({
        method: 'GET',
        path: '/',
        handler: (request, h) => {

            return 'Hello World!';
        }
    });

    await server.start();
    console.log('Server running on %s', server.info.uri);
};

process.on('unhandledRejection', (err) => {

    console.log(err);
    process.exit(1);
});

init();
```

Nesse exemplo, a rota é definida diretamente no servidor, deixando claro:
- qual método HTTP é aceito (GET)
- qual caminho será acessado (/)
- qual lógica será executada ao receber a requisição

Ao acessar ```http://localhost:3000```, o servidor responde com a mensagem Hello World!, confirmando que a aplicação está funcionando corretamente.

## Dependências

Ao utilizar o Hapi, é importante entender que o framework **não tenta controlar toda a stack da aplicação**. Seu papel principal é definir **como o servidor HTTP funciona**, como as requisições são processadas e onde regras importantes devem ser declaradas. O Hapi estabelece uma **arquitetura clara, explícita e previsível**, mas deixa ao desenvolvedor a liberdade de escolher as ferramentas que fazem sentido para o domínio do projeto — como banco de dados, ORM, cache ou filas. Nesse sentido, o Hapi atua como um **orquestrador do fluxo HTTP**, enquanto as demais bibliotecas entram como componentes especializados.

As dependências a seguir são apenas exemplos de dependências possíveis de serem utilizadas no framework e podem ser instaladas com os seguintes comandos:

```bash
npm install @hapi/boom joi
npm install hapi-swagger @hapi/inert @hapi/vision
npm install sequelize pg pg-hstore
npm install --save-dev nodemon
```

### @hapi/hapi — *framework core*

O **@hapi/hapi** é o **núcleo arquitetural da aplicação**: é o framework inteiro que lida com o ciclo de requisição, roteamento, plugins e extensões. Diferente de micro-frameworks minimalistas, Hapi aplica uma filosofia “configuração sobre convenção”, incentivando que comportamentos de rota, segurança e validação sejam **declarados de forma explícita e previsível** no servidor.

Ele não é uma biblioteca de utilidades soltas, é um **framework completo orientado por configurações e plugins** que define como o servidor HTTP trata tudo que envolve requisições web.

### @hapi/boom — *erros HTTP consistentes*

**Boom** é uma biblioteca criada pelo mesmo ecossistema do Hapi para **padronizar erros HTTP**. Em vez de lançar exceções genéricas ou strings de erro com status confuso, Boom encapsula **status code, mensagem e payload estruturado**, alinhando os erros diretamente ao padrão HTTP.

Isso significa que a camada de negócio pode dizer simplesmente:

```js
throw Boom.notFound("Recurso não existe");
```

e o framework sabe como traduzir isso para uma resposta HTTP com status e corpo coerentes, mantendo a API previsível e fácil de auditar.

### hapi-swagger, @hapi/inert e @hapi/vision — *documentação e exposição da API*

O **hapi-swagger** é um plugin responsável por gerar **documentação automática da API no padrão OpenAPI**, utilizando as definições explícitas de rotas e validações feitas com Joi.

Para funcionar, ele depende de dois plugins oficiais do ecossistema Hapi:

* **@hapi/inert** — habilita o servidor a servir **arquivos estáticos**, necessários para a interface do Swagger UI;
* **@hapi/vision** — adiciona suporte à **renderização de templates**, usada para montar a interface visual da documentação.

Essas dependências **não participam da lógica de negócio nem do fluxo principal da API**. Elas existem exclusivamente para **expor, visualizar e inspecionar a API de forma interativa**, mantendo a documentação desacoplada do core da aplicação.

### joi — *validação declarativa e segura*

O **Joi** é uma **biblioteca de validação de esquemas** originalmente criada pelo mesmo grupo que desenvolve o Hapi. Ela permite definir **contratos rigorosos** para `payload`, `query`, `params` e `headers`, garantindo que entradas inválidas nunca alcancem a lógica principal.

A força do Joi está em:

* **validação declarativa** — você descreve o formato esperado com tipos, obrigatoriedade, ranges etc.;
* **mensagens de erro padronizadas** — integradas ao ciclo de requisição do Hapi;
* **segurança de entrada** — reduz riscos de ataques por dados malformados.

Com Joi, as rotas Hapi não dependem de middlewares externos para validação, a validação vira parte da definição da rota em si.

### Sequelize — *ORM relacional sofisticado*

O **Sequelize** é um **ORM** que traduz objetos JavaScript para tabelas e relações de um banco de dados relacional (como PostgreSQL). Sequelize abstrai a complexidade de se escrever SQL manual e vincula **lógica de dados fortemente ao domínio da aplicação**, melhorando a organização e a manutenção de grandes sistemas.

Ele traz conceitos como:

* **modelos que representam tabelas** (com tipos, restrições e relações);
* **associações entre modelos** (um-para-muitos, muitos-para-muitos);
* **transações e sincronização de esquema**;
* **consultas e CRUD usando API fluente em vez de SQL puro**.

### pg e pg-hstore — *driver Postgres e serialização*

Estes dois pacotes são **dependências de suporte para o Sequelize trabalhar com PostgreSQL**:

* **pg** — é o **driver PostgreSQL puro** em Node.js: ele implementa as conexões, queries, pooling e protocolo de comunicação com o banco.
* **pg-hstore** — é um utilitário que lida com **serialização de tipos JSON/HSTORE** no Postgres, permitindo que objetos JavaScript sejam armazenados em campos especiais no banco sem dor.

O Sequelize precisa desses dois para trabalhar com Postgres; sozinho ele não faz comunicação com o banco.

### nodemon — *reload automático no desenvolvimento*

**nodemon** não faz parte da lógica do servidor nem do runtime da aplicação, mas é uma **ferramenta de desenvolvimento** que observa arquivos e **reinicia o servidor automaticamente** quando algo muda.

Isso acelera o feedback de desenvolvimento e evita que você tenha que matar e reiniciar o processo manualmente após cada alteração de código.

## Arquitetura de diretórios:

Diferentemente de outros frameworks, **o Hapi não impõe uma arquitetura rígida** ou um padrão obrigatório de organização de código. Essa característica oferece maior liberdade ao desenvolvedor para estruturar a aplicação de acordo com suas necessidades, desde que respeitados os princípios de organização e responsabilidade.

Nesse contexto, a arquitetura adotada neste projeto explora uma das principais propostas do Hapi: **a organização da aplicação por meio de plugins**. Cada plugin pode encapsular funcionalidades específicas, como rotas, regras de negócio, integrações externas ou acesso a dados, promovendo baixo acoplamento e alta coesão.

**Dentro de cada plugin, o Hapi também não impõe uma estrutura interna fixa**, permitindo que o desenvolvedor escolha livremente como organizar seu código. Essa flexibilidade possibilita desde implementações mais simples, concentradas em poucos arquivos, até arquiteturas internas mais elaboradas, conforme a complexidade e as necessidades de cada módulo.

A seguir é apresentada uma sugestão de organização de diretórios, com o objetivo de exemplificar uma possível estrutura para a aplicação.

### Estrutura de Diretórios 

```
src/
│
├── handlers/
│   └── ← “Ponte HTTP” → recebe a requisição do Hapi e chama services
│
├── routes/
│   └── ← onde definimos as rotas HTTP, com método, path, validação Joi e handler
│
├── schemas/
│   └── ← contratos de entrada de dados (Joi) para validações explicitas
│
├── services/
│   └── ← lógica de negócio isolada (sem HTTP ou DB diretamente)
│
├── repository/
│   └── ← logica de acesso e manipulação dos dados
│
├── models/
│   └── ← representação das tabelas e relações (Sequelize)
│
├── utils/
│   └── ← código utilitário compartilhado (helpers, transformações, etc.)
│
└── index.js
    └── ← bootstrap da aplicação (servidor, plugins, rotas)
```

### Fluxo de responsabilidade:

```txt
HTTP Request
   ↓
routes/           ← Define: método + path + validações + handler
   ↓
schemas/          ← Valida entrada contra contrato Joi
   ↓
handlers/         ← Traduz a requisição para a chamada de serviço
   ↓
services/         ← Regras de negócio puras
   ↓
repository/       ← acesso aos dados
   ↓
models/           ← Persistência dos dados via Sequelize → banco SQL
   ↓
Database
```

### Como tudo se encaixa

#### /src/routes — *definição explícita de interface*

Cada arquivo nesta camada agrupa definições de rotas relacionadas, descrevendo para cada rota:

* método HTTP
* caminho (`path`)
* validações (via Joi)
* handler correspondente
* tags para Swagger

#### /src/schemas — *contratos de dados*

Esta camada armazena **schemas Joi** que descrevem formalmente o formato de dados aceitos:

* `payload` (corpo da requisição)
* `params` (segmentos de URL)
* `query` (parâmetros de consulta)

Eles são **contratos de entrada** que previnem dados inesperados de atravessarem a aplicação, reforçando a segurança.

#### /src/handlers — *gateway das requisições*

Os handlers são a **camada que conecta o Hapi ao domínio da aplicação**. Eles recebem o `request` e chamam serviços, retornando respostas. Não contém lógica de negócio pesada, sua função é **orquestrar chamadas** conforme a rota. É o equivalente **ao controlador HTTP puro**.

#### /src/services — *regra de negócio isolada*

Aqui está a **lógica do domínio**, separada do HTTP e da persistência. Os services:

* recebem dados validados
* aplicam regras
* interagem com modelos
* retornam resultados ou erros (Boom)

Services não têm dependência de infraestrutura HTTP, isso permite testá-los isoladamente.

### /src/repositories — *acesso a dados abstraído*

O **Repository** é a camada que **isola a persistência** do resto do sistema. Ele funciona como um *adaptador* entre o domínio e o banco de dados.

Responsabilidades do repository:

* encapsular queries e operações de leitura/escrita
* traduzir intenções do domínio em operações no ORM
* esconder detalhes do Sequelize (ou qualquer outro ORM)
* fornecer uma API clara para os services

Isso permite:

* trocar ORM ou banco sem quebrar o domínio
* mockar acesso a dados em testes
* evitar services poluídos com `findAll`, `include`, `transaction`, etc.

#### /src/models — *representação de dados persistentes*

Nesta camada estão os **modelos Sequelize** que representam tabelas e relações no banco:

* cada arquivo define um modelo
* descreve campos, tipos e relacionamentos
* encapsula regras básicas de persistência

Modelos e services juntos formam o **núcleo de domínio** da aplicação no backend.

#### /src/utils — *funções transversais*

O utilitário armazena ferramentas reutilizáveis que não pertencem a um domínio específico, como helpers, formatação ou transformações comuns.

#### index.js — *bootstrapping*

O ponto de partida da aplicação, onde o servidor é **instanciado**, plugins registrados, rotas carregadas e a aplicação realmente começa a ouvir requisições.

Ele não deve conter lógica de negócio; sua função é **inicialização e composição das partes**.


### Porque essa arquitetura importa?

* **Clareza absoluta de responsabilidade** (cada pasta faz apenas uma coisa)
* **Testabilidade** (services podem ser testados sem servidor)
* **Escalabilidade** (cresce sem virar bagunça)
* **Observabilidade** (Swagger + validação explícita com Joi)
* **Separa HTTP ↔ Negócio ↔ Dados** (reduz acoplamento)

## Considerações finais

Ao longo deste material, foram apresentados os principais aspectos do Hapi, desde seu contexto histórico e consolidação no ecossistema Node.js até sua utilização prática, abordando conceitos como instalação, uso de dependências e organização arquitetural. A proposta foi oferecer uma visão clara e estruturada do framework, destacando sua flexibilidade, previsibilidade e adequação para aplicações que exigem organização, modularidade e controle. Com isso, espera-se que o leitor esteja apto a compreender o funcionamento do Hapi e utilizá-lo como base para o desenvolvimento de aplicações escaláveis e bem estruturadas.

## Referências

HAPI. **Hapi Tutorials**. Disponível em: [https://hapi.dev/tutorials/?lang=en_US](https://hapi.dev/tutorials/?lang=en_US). Acesso em: jan. 2026.

THE ORG. **Eran Hammer — Sideway Inc.** Disponível em: [https://theorg.com/org/sideway-inc/org-chart/eran-hammer](https://theorg.com/org/sideway-inc/org-chart/eran-hammer). Acesso em: jan. 2026.

STACKABUSE. **Hapi vs Express: Comparing Node.js Web Frameworks**. Disponível em: [https://stackabuse.com/hapi-vs-express-comparing-node-js-web-frameworks/](https://stackabuse.com/hapi-vs-express-comparing-node-js-web-frameworks/). Acesso em: jan. 2026.

PHAN, Alanna. **Choosing Between Open Source Frameworks: Express.js vs Hapi.js**. Medium, 2018. Disponível em: [https://medium.com/@phan.alanna/choosing-between-open-source-frameworks-express-js-vs-hapi-js-5c9b2131ba19](https://medium.com/@phan.alanna/choosing-between-open-source-frameworks-express-js-vs-hapi-js-5c9b2131ba19). Acesso em: jan. 2026.

SEQUELIZE. **Sequelize Documentation (v6)**. Disponível em: [https://sequelize.org/docs/v6/](https://sequelize.org/docs/v6/). Acesso em: jan. 2026.

MEZ, Jason. **Introduction to Hapi.js**. Medium, 2017. Disponível em: [https://medium.com/@jsonmez/introduction-to-hapi-js-c128f40bd919](https://medium.com/@jsonmez/introduction-to-hapi-js-c128f40bd919). Acesso em: jan. 2026.
