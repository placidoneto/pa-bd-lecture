# FLASK

## Introdução

Flask é um microframework Python criado por Armin Ronacher e lançado oficialmente em 2010. Ele é conhecido por sua simplicidade, flexibilidade e extensibilidade.

Embora seja classificado como "micro", Flask é robusto e permite construir desde pequenos serviços até APIs RESTful completas e escaláveis. O termo micro significa que o framework não impõe uma estrutura rígida e inclui apenas o essencial — roteamento, servidor web embutido, sistema de templates e extensões opcionais.

## Principais Características

- Leve e modular: você escolhe somente o que deseja utilizar;

- Roteamento simples com decorators (@app.route());

- Servidor de desenvolvimento integrado com recarregamento automático;

- Suporte nativo a JSON: ideal para APIs;

- Extensível: ORM, autenticação, formulários, migrações, testes etc;

- Ecoa o princípio do Python: "simplicidade antes da complexidade".

A proposta do Flask é oferecer o núcleo mínimo necessário e permitir que o próprio desenvolvedor defina a arquitetura e escolha as bibliotecas adicionais.

## Arquitetura em camadas (Organização recomendada)

O Flask não impõe uma estrutura padrão, mas a comunidade adota uma arquitetura organizada similar à usada em outros frameworks web:

### 1. Routes (Camada de Entrada)

responsável por:

- Receber requisições HTTP;
- Definir endpoints;
- Realizar validações iniciais;
- Delegar ao serviço correspondente.

Normalmente ficam em arquivos como routes.py ou separados por módulos.

### 2. Services (Lógica de negócio)

responsável por:

- Aplicar a lógica de negócio;
- Implementar as regras do domínio;
- Transformar ou validar dados.

Serviços ajudam a manter as rotas enxutas e facilitar testes unitários.

### 3. Models (Modelo de negócio)

representação do domínio:

- Entidades do sistema;
- Estrutura dos dados;
- Regras essenciais.

### 4. Repository (Acesso aos dados)

responsável por:

- Consultar, salvar e alterar dados no banco;
- Isolar detalhes de persistência;
- Evitar SQL dentro de rotas e serviços.

### 5. DTOs e Serialização

Em Flask, é comum usar:

- Marshmallow para serialização / validação;
- Pydantic para validação estruturada;

Servem para garantir que a API não exponha diretamente as entidades internas.

## Princípios RESTful com Flask

Uma API RESTful em Flask segue conceitos bem consolidados:

### 1. Recursos e Endpoints

Cada rota representa um recurso:

    GET /users
    POST /users
    GET /users/<id>

### 2. Uso semântico de métodos HTTP

    GET → buscar

    POST → criar

    PUT/PATCH → atualizar

    DELETE → remover

### 3. Retorno de JSON

Flask oferece:

    from flask import Flask, jsonify

    app = Flask(__name__)

    @app.route("/status", methods=["GET"])
    def status():
        response = {
            "message": "API funcionando corretamente",
            "status": "ok",
            "version": "1.0.0"
        }
        return jsonify(response), 200 


A função jsonify() ajusta headers e serializa dados automaticamente.

### 4. Códigos de Status HTTP

Utilização adequada dos códigos:

    200 → OK

    201 → Created

    400 → Bad Request

    404 → Not Found

    500 → Internal Server Error

### 5. Tratamento de Erros padrão

Flask permite handlers globais:

    @app.errorhandler(404)
    def not_found(e):
        return jsonify(error="Recurso não encontrado"), 404

## Ecossistema e Extensões (Ponto Forte do Flask)

### Flask brilha pela grande quantidade de extensões:

#### Persistência

    Flask-SQLAlchemy (ORM popular)

    Peewee

    SQLModel (da comunidade FastAPI)

#### Migrações

    Flask-Migrate (baseado em Alembic)

    Autenticação e Segurança

    Flask-JWT-Extended

    Flask-Login

#### Serialização

    Marshmallow

    Pydantic

#### Testes

    Suporte integrado (pytest + Flask.testing)

#### Outras

    Flask-Caching

    Flask-CORS

    Flask-RESTful / Flask-API (camadas extras para APIs)

## Comparativo com outros framework Python

| Framework              | Característica           | Performance  | Complexidade    | Ideal para             |
|------------------------|--------------------------|--------------|-----------------|------------------------|
| **Flask**              | Micro, flexível          | Alta         | Baixa           | APIs pequenas/médias   |
| **FastAPI**            | Tipagem + performance    | Muito alta   | Média           | APIs modernas, async   |
| **Django Rest Framework** | Completo e robusto    | Média        | Alta            | Grandes sistemas       |

## Melhores práticas com Flask

- Estruturar o projeto em módulos (routes, services, models, repositories);
- Usar Blueprints para separar funcionalidade;
- Centralizar erros em handlers globais;
- Criar ambientes (dev, test, prod) com diferentes configs;
- Utilizar extensões de forma controlada (evitar inflar o projeto);
- Usar .env + python-dotenv para configurações sensíveis;
- Evitar lógica de negócio nas rotas — delegar aos services.








