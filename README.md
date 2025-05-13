# Relacionamento entre Modelos ORM em Django Rest Framework

## Objetivo

O objetivo deste documento é apresentar como é possível criar relacionamentos entre modelos ORM em Django Rest Framework. 

## Introdução

Django Rest Framework é uma biblioteca que facilita a criação de APIs REST em Django. Uma das funcionalidades mais importantes do Django Rest Framework é a serialização de objetos. A serialização é o processo de converter um objeto em um formato que pode ser facilmente armazenado ou transmitido. No caso do Django Rest Framework, a serialização é usada para converter objetos de modelos ORM em JSON.

## Modelos ORM

O Django é um framework web que utiliza o padrão de arquitetura MVC (Model-View-Controller). No Django, o modelo é responsável por representar os dados da aplicação. O Django utiliza o ORM (Object-Relational Mapping) para mapear os modelos para tabelas em um banco de dados relacional. Isso significa que cada modelo é representado por uma tabela no banco de dados e cada instância do modelo é representada por uma linha na tabela.

Modelos ORM são classes que representam tabelas em um banco de dados. No Django, os modelos ORM são definidos em arquivos `models.py`. Cada modelo ORM é uma classe que herda da classe `models.Model`. Os atributos da classe representam os campos da tabela. Por exemplo, o modelo Cliente abaixo representa uma tabela com os campos `nome`, `email`, `telefone` e `data_cadastro`:

```python
class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    data_cadastro = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return f'{self.nome} - {self.email} - {self.telefone}'
```

## Relacionamentos entre Modelos ORM

Os modelos ORM podem ter relacionamentos entre si. Existem três tipos de relacionamentos em Django: ForeignKey, OneToOneField e ManyToManyField.

### Relacionamento 1 - N (ForeignKey)

O relacionamento ForeignKey é usado para representar uma relação de muitos para um. Por exemplo, suponha que temos um modelo `Endereço` que tem um campo `cliente` que se refere a um objeto do modelo `Cliente`:

```python
class Endereco(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True, null=True)
    rua = models.CharField(max_length=100)
    numero = models.CharField(max_length=10)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=50)
    estado = models.CharField(max_length=2) 
    cep = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.rua}, {self.numero} - {self.bairro}, {self.cidade}/{self.estado} - {self.cep}'
```

Perceba que existe um campo `cliente` que é uma chave estrangeira para o modelo `Cliente`. Isso significa que um endereço está associado a um único cliente. Esse tiop de relacionamento é conhecido como relação de muitos para um. Isso porque um cliente pode ter vários endereços, mas um endereço pertence a um único cliente. O Django Rest cria automaticamente um campo `cliente_id` na tabela `Endereco` para armazenar a chave estrangeira. Isso é feito para garantir a integridade referencial do banco de dados. Após a criação no novo modelo é necessário rodar o comando `python manage.py makemigrations` e `python manage.py migrate` para criar a tabela no banco de dados.


#### Exemplo de Formas de Pagamento

O relacionamento entre o modelo `FormaPagamento` e o modelo `Pedido` é um exemplo de relacionamento de muitos para um. Isso significa que um pedido pode ter apenas uma forma de pagamento, mas uma forma de pagamento pode estar associada a vários pedidos. O Django Rest cria automaticamente um campo `forma_pagamento_id` na tabela `Pedido` para armazenar a chave estrangeira. Isso é feito para garantir a integridade referencial do banco de dados. Após a criação no novo modelo é necessário rodar o comando `python manage.py makemigrations` e `python manage.py migrate` para criar a tabela no banco de dados.

```python
class FormaPagamento(models.Model):
    nome = models.CharField(max_length=50)
    descricao = models.CharField(max_length=100)
    taxa = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.nome} - {self.descricao} - {self.taxa}'
```

```python
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    endereco_entrega = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    itens = models.ManyToManyField(Item)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    data_entrega = models.DateTimeField()
    
    def __str__(self): 
        return f'{self.cliente} - {self.vendedor} - {self.data_pedido}'
```

```python
class Vendedor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    data_cadastro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nome} - {self.email} - {self.telefone}'
```


### Relacionamento 1 - 1 (OneToOneField)

O relacionamento OneToOneField é usado para representar uma relação de um para um. Por exemplo, suponha que temos um modelo `Perfil` que tem um campo `cliente` que se refere a um objeto do modelo `Cliiente`:

```python
class Perfil(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    foto = models.ImageField(upload_to='fotos/')
    data_nascimento = models.DateField()
    genero = models.CharField(max_length=1, choices=(('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')))
    cpf = models.CharField(max_length=14)
    tipo = models.CharField(max_length=1, choices=(('F', 'Física'), ('J', 'Jurídica')))

    def __str__(self):
        return f'{self.cliente.nome} - {self.genero} - {self.data_nascimento}'
```   

Perceba que existe um campo `cliente` que é uma chave estrangeira para o modelo `Cliente`. Isso significa que um perfil está associado a um único cliente. Esse tipo de relacionamento é conhecido como relação de um para um. Isso porque um cliente tem um único perfil e um perfil pertence a um único cliente. O Django Rest cria automaticamente um campo `cliente_id` na tabela `Perfil` para armazenar a chave estrangeira. Isso é feito para garantir a integridade referencial do banco de dados. Após a criação no novo modelo é necessário rodar o comando `python manage.py makemigrations` e `python manage.py migrate` para criar a tabela no banco de dados.

### Relacionamento N - N (ManyToManyField)

O relacionamento ManyToManyField é usado para representar uma relação de muitos para muitos. Por exemplo, suponha que temos um modelo `Pedido` que tem um campo `itens` que se refere a um objeto do modelo `Item`. Nesse caso, um pedido pode ter vários itens e um item pode estar em vários pedidos:

```python
class Item (models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=100)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    estoque = models.IntegerField()
    
    def __str__(self):
        return f'{self.nome} - {self.descricao} - R$ {self.preco} - Estoque: {self.estoque}'


class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.CASCADE)
    endereco_entrega = models.ForeignKey(Endereco, on_delete=models.CASCADE)
    itens = models.ManyToManyField(Item)
    forma_pagamento = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    data_entrega = models.DateTimeField()
    
    def __str__(self): 
        return f'{self.cliente} - {self.vendedor} - {self.data_pedido}'
```

Perceba que existe um campo `itens` que é uma chave estrangeira para o modelo `Item`. Isso significa que um pedido pode ter vários itens e um item pode estar em vários pedidos. Esse tipo de relacionamento é conhecido como relação de muitos para muitos. O Django Rest cria automaticamente uma tabela intermediária para armazenar os relacionamentos entre os pedidos e os itens. Isso é feito para garantir a integridade referencial do banco de dados. Após a criação no novo modelo é necessário rodar o comando `python manage.py makemigrations` e `python manage.py migrate` para criar a tabela no banco de dados.

É possível utilizar o argumento `through` para especificar o nome da tabela intermediária. Por exemplo, se quisermos que a tabela intermediária seja chamada `PedidoItem`, podemos fazer o seguinte:

```python
class Pedido(models.Model):
    ...
    itens = models.ManyToManyField(Item, through='PedidoItem')
    ...

class PedidoItem(models.Model):

    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=8, decimal_places=2)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f'{self.pedido} - {self.item} - {self.quantidade} - R$ {self.subtotal}'
``` 


## Serialização de Objetos

Como já vimos nas aulas anteriores, a serialização de objetos é o processo de converter um objeto em um formato que pode ser facilmente armazenado ou transmitido. No caso do Django Rest Framework, a serialização é usada para converter objetos de modelos ORM em JSON. Para serializar um objeto, é necessário criar uma classe de serialização que herda da classe `serializers.ModelSerializer`. Por exemplo, a classe de serialização para o modelo `Cliente` é a seguinte:

```python
from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'
```

para todos os novos modelos criados é necessário criar uma classe de serialização para cada modelo. Para serializar um objeto, basta passá-lo como argumento para a classe de serialização.

## Conclusão

Apresentamos como é possível criar relacionamentos entre modelos ORM em Django Rest Framework. Vimos que é possível criar relacionamentos de muitos para um, um para um e muitos para muitos. Esses relacionamentos são úteis para modelar a estrutura de um banco de dados e facilitar a serialização de objetos em JSON.

## Referências

- [Django Rest Framework](https://www.django-rest-framework.org/)

- [Django Models](https://docs.djangoproject.com/en/3.2/topics/db/models/)

- [Django Model Relationships](https://docs.djangoproject.com/en/3.2/topics/db/models/#relationships)