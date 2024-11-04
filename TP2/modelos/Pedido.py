class Pedido:
    def __init__(self, id, cliente_id, vendedor_id, data_pedido, endereco_entrega_id, forma_pagamento_id, status):
        self._id = id
        self._cliente_id = cliente_id
        self._vendedor_id = vendedor_id
        self._data_pedido = data_pedido
        self._endereco_entrega_id = endereco_entrega_id
        self._forma_pagamento_id = forma_pagamento_id
        self._status = status

    @property
    def id(self):
        return self._id

    @property
    def cliente_id(self):
        return self._cliente_id

    @property
    def vendedor_id(self):
        return self._vendedor_id

    @property
    def data_pedido(self):
        return self._data_pedido

    @property
    def endereco_entrega_id(self):
        return self._endereco_entrega_id

    @property
    def forma_pagamento_id(self):
        return self._forma_pagamento_id

    @property
    def status(self):
        return self._status
    
    @id.setter
    def id(self, id):
        self._id = id

    @cliente_id.setter
    def cliente_id(self, cliente_id):
        self._cliente_id = cliente_id

    @vendedor_id.setter
    def vendedor_id(self, vendedor_id):
        self._vendedor_id = vendedor_id

    @data_pedido.setter
    def data_pedido(self, data_pedido):
        self._data_pedido = data_pedido

    @endereco_entrega_id.setter
    def endereco_entrega_id(self, endereco_entrega_id):
        self._endereco_entrega_id = endereco_entrega_id

    @forma_pagamento_id.setter
    def forma_pagamento_id(self, forma_pagamento_id):
        self._forma_pagamento_id = forma_pagamento_id

    @status.setter
    def status(self, status):
        self._status = status
        
    def __str__(self):
        return f"Pedido: {self.id}, Cliente: {self.cliente_id}, Vendedor: {self.vendedor_id}, Data Pedido: {self.data_pedido}, Endereço de Entrega: {self.endereco_entrega_id}, Forma de Pagamento: {self.forma_pagamento_id}, Status: {self.status}"