class Item:
    def __init__(self, id, nome, descricao, preco, estoque):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._preco = preco
        self._estoque = estoque

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, descricao):
        self._descricao = descricao

    @property
    def preco(self):
        return self._preco

    @preco.setter
    def preco(self, preco):
        self._preco = preco

    @property
    def estoque(self):
        return self._estoque

    @estoque.setter
    def estoque(self, estoque):
        self._estoque = estoque