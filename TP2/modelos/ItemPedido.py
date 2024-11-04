class ItemPedido:
    def __init__(self, id, pedido_id, item_id, quantidade, preco_unitario):
        self._id = id
        self._pedido_id = pedido_id
        self._item_id = item_id
        self._quantidade = quantidade
        self._preco_unitario = preco_unitario

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def pedido_id(self):
        return self._pedido_id

    @pedido_id.setter
    def pedido_id(self, pedido_id):
        self._pedido_id = pedido_id

    @property
    def item_id(self):
        return self._item_id

    @item_id.setter
    def item_id(self, item_id):
        self._item_id = item_id

    @property
    def quantidade(self):
        return self._quantidade

    @quantidade.setter
    def quantidade(self, quantidade):
        self._quantidade = quantidade

    @property
    def preco_unitario(self):
        return self._preco_unitario

    @preco_unitario.setter
    def preco_unitario(self, preco_unitario):
        self._preco_unitario = preco_unitario
        
    def __str__(self):
        return f"ItemPedido: {self._id} - Pedido: {self._pedido_id} - Item: {self._item_id} - Quantidade: {self._quantidade} - Preço unitário: R${self._preco_unitario}"    