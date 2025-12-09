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
