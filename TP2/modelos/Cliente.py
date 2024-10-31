class Cliente:
    def __init__(self, nome, email, telefone, data_cadastro):
        self._nome = nome        
        self._email = email
        self._telefone = telefone
        self._data_cadastro = data_cadastro

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        self._email = email

    @property        
    def telefone(self):
        return self._telefone
    
    @telefone.setter
    def telefone(self, telefone):
        self._telefone = telefone
    
    @property
    def data_cadastro(self):
        return self._data_cadastro
    
    @data_cadastro.setter
    def data_cadastro(self, data_cadastro):
        self._data_cadastro = data_cadastro
        
    def __str__(self):
        return f'Cliente: {self._nome}, {self._email}, {self._telefone}, {self._data_cadastro}'
    
    