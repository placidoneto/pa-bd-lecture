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
