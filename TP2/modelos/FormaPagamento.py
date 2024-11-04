class FormaPagamento:
    def __init__(self, id, descricao):
        self._id = id
        self._descricao = descricao

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, descricao):
        self._descricao = descricao
        
    def __str__(self):
        return f"Forma de pagamento: {self._descricao}"