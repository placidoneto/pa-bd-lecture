 # Exemplo prático

 ## 1. Criar e ativar um ambiente virtual

    # criar venv
    python -m venv venv

    # ativar (Linux / macOS)
    source venv/bin/activate

    # ativar (Windows PowerShell)
    venv\Scripts\activate

## 2. Instalar Flask

    pip install Flask
    pip install flask_sqlalchemy
    pip install Flask-Migrate
    pip install flasgger
    pip install psycopg2-binary (Caso queira usar PostgreSQL)

## 3. Estrutura inicial do projeto (Arquitetura em Camadas)

    meu_app/
    │── app.py
    │── config.py
    │── models/
    │     └── produto_model.py
    │── repositories/
    │     └── produto_repository.py
    │── services/
    │     └── produto_service.py
    └── routes/
        └── produto_routes.py

- Routes → Endpoints

- Services → Lógica de negócio

- Models → Estruturas das entidades

- Repository → Acesso ao banco

## 4. Arquivo de configuração

```python
class Config:
    # SQLALCHEMY_DATABASE_URI = "postgresql://flask_user:12345@localhost/flask_demo" (Caso queira usar PostgreSQL)
    SQLALCHEMY_DATABASE_URI = "sqlite:///meuappdb.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

## 5. Model (Entidade)

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Produto(db.Model):
    __tablename__ = "produtos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco
        }

```

## 6. Repository (Acesso ao banco)

```python
from models.produto_model import db, Produto

class ProdutoRepository:

    @staticmethod
    def criar(produto):
        db.session.add(produto)
        db.session.commit()
        return produto

    @staticmethod
    def listar():
        return Produto.query.all()

```

## 7. Service (Lógica de negócio)

```python
from models.produto_model import Produto
from repositories.produto_repository import ProdutoRepository

class ProdutoService:

    @staticmethod
    def criar_produto(data):
        produto = Produto(nome=data["nome"], preco=data["preco"])
        return ProdutoRepository.criar(produto)

    @staticmethod
    def listar_produtos():
        return ProdutoRepository.listar()
```

## 8. Routes (Entrada da API)

```python
from flask import Blueprint, request, jsonify
from services.produto_service import ProdutoService

produto_bp = Blueprint("produto", __name__)

@produto_bp.route("/produtos", methods=["POST"])
def criar_produto():
    """
    Cria um novo produto
    ---
    tags:
      - Produtos
    parameters:
      - in: body
        name: body
        required: true
        schema:
          id: Produto
          required:
            - nome
            - preco
          properties:
            nome:
              type: string
              example: Teclado Gamer
            preco:
              type: number
              example: 150.99
    responses:
      201:
        description: Produto criado com sucesso
    """
    data = request.json
    novo = ProdutoService.criar_produto(data)
    return jsonify(novo.to_dict()), 201


@produto_bp.route("/produtos", methods=["GET"])
def listar_produtos():
    """
    Lista todos os produtos
    ---
    tags:
      - Produtos
    responses:
      200:
        description: Lista de produtos
    """
    produtos = ProdutoService.listar_produtos()
    return jsonify([p.to_dict() for p in produtos]), 200
```

## 9. Arquivo principal da aplicação

```python
from flask import Flask
from config import Config
from models.produto_model import db
from routes.produto_routes import produto_bp
from flask_migrate import Migrate
from flasgger import Swagger

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

# Inicializar Swagger
swagger = Swagger(app)

# Blueprints
app.register_blueprint(produto_bp)

@app.route("/status")
def status():
    """
    Verifica o status da API
    ---
    tags:
      - Status
    responses:
      200:
        description: API funcionando
    """
    return {"status": "ok", "version": "1.0.0"}, 200

if __name__ == "__main__":
    app.run(debug=True)
```

## 10. Criar as tabelas com migrações

no diretório raiz do seu projeto(neste caso: meu_app) rode:

    flask db init
    flask db migrate -m "Criando tabela produtos"
    flask db upgrade

## 11. Executar a aplicação

no diretório raiz do seu projeto(neste caso: meu_app) rode:

    python app.py

A API estará disponível em: http://127.0.0.1:5000

E o Swagger em: http://127.0.0.1:5000/apidocs/



