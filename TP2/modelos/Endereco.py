class Endereco:
    def __init__(self, id, id_cliente, rua, cidade, estado, cep):
        self.id = id
        self.id_cliente = id_cliente
        self.rua = rua        
        self.cidade = cidade
        self.estado = estado
        self.cep = cep
        
    def id(self):
        return self.id
    
    def id_cliente(self):
        return self.id_cliente
    
    def rua(self):
        return self.rua
    
    def cidade(self):
        return self.cidade
    
    def estado(self):
        return self.estado
    
    def cep(self):
        return self.cep
    
    def id(self, id):
        self.id = id
        
    def id_cliente(self, id_cliente):
        self._id_cliente = id_cliente
        
    def rua(self, rua):
        self._rua = rua
        
    def cidade(self, cidade):
        self._cidade = cidade
        
    def estado(self, estado):
        self._estado = estado
        
    def cep(self, cep):
        self._cep = cep
        
        
    def __str__(self):
        return f'Endereco: {self.id}, {self.id_cliente}, {self.rua}, {self.cidade}, {self.estado}, {self.cep}'
    
    