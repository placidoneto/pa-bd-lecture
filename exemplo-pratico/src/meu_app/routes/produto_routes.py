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
