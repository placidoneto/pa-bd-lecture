# L02 - Introdução a Django Rest Framework - Models and ORM

## Aplicação de Gerenciamento de Pedidos com PostgreSQL com Django Rest Framework

Imagine uma aplicação web que permite a compra de itens na internet. Essa aplicação seria construída com uma interface intuitiva, onde os usuários podem:

- Cadastrar um novo cliente/usuário
- Cadastrar um novo vendedor
- Cadastrar um novo item
- Visualizar os itens disponíveis
- Adicionar itens para comprar
- Adicionar endereço de entrega
- Realizar um pedido
- Incluir uma forma de pagamento
- Visualizar os pedidos realizados
- Visualizar os itens comprados
- Visualizar os itens vendidos por um vendedor
- Visualizar os itens comprados por um cliente
- Realizar/escolher a forma de pagamento
- etc...

Esse tipo de aplicação é comum em sites de e-commerce, onde os usuários podem comprar produtos e serviços.
Nas aulas anteriores vimos como criar as tabelas e manipular os dados com SQL. Agora vamos aprender a criar uma aplicação web com Django Rest Framework para manipular os dados de uma aplicação de compra de itens na Internet.

### Estrutura da Aplicação Web com Django Rest para a aplicação de Compra de Itens na Internet

Vamos implementar uma simples aplicação usando Django Rest para manipular os dados de venda.

Estrutura de Diretórios
```
/amazon
    /static
    /templates
    __init__.py
    asgi.py
    settings.py
    urls.py
    wsgi.py
manage.py
```

### Passo a Passo
1. **Configuração Inicial**

   - Crie um novo projeto Django:

```
django-admin startproject amazon
cd amazon
```

   - Crie um novo aplicativo dentro do projeto:
```
python manage.py startapp backend
```

   - Adicione o aplicativo ao *INSTALLED_APPS* no arquivo *amazon/settings.py*:

```python
INSTALLED_APPS = [
    ...
    'backend',
]
```

2. **Configuração do PostgreSQL**
      - Instale o driver do PostgreSQL:
```
pip install psycopg2-binary
```
- Configure o banco de dados PostgreSQL no arquivo *amazon/settings.py*:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nome_do_banco',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **Modelos (Models)**

- Edite o arquivo *core/models.py* para definir as tabelas:

```python
from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.nome

class Veiculo(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.marca} {self.modelo}"

class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data_venda = models.DateTimeField(auto_now_add=True)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venda de {self.veiculo} para {self.cliente}"
```

4. **Serializers**

- Crie o arquivo *core/serializers.py* e adicione os serializers:

```python
from rest_framework import serializers
from .models import Cliente, Veiculo, Venda

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = '__all__'

class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'
```

5. **Views**

- Edite o arquivo *core/views.py* para adicionar as views:

```python
from rest_framework import viewsets
from .models import Cliente, Veiculo, Venda
from .serializers import ClienteSerializer, VeiculoSerializer, VendaSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

```

6. **URLs**

- Edite o arquivo *venda_veiculos/urls.py* para incluir as rotas:

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views

router = DefaultRouter()
router.register(r'clientes', views.ClienteViewSet)
router.register(r'veiculos', views.VeiculoViewSet)
router.register(r'vendas', views.VendaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
```
7. **Configurações Finais**

- Adicione *rest_framework* e *core* ao *INSTALLED_APPS* no arquivo *venda_veiculos/settings.py*:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'backend',
]
```

- Execute as migrações para criar as tabelas no banco de dados:

```python
python manage.py makemigrations
python manage.py migrate

```

8. **Testar a Aplicação**
- Inicie environment python para testar a aplicação:
  
```python
python3 -m venv env
source env/bin/activate

pip install django djangorestframework
pip install markdown       
pip install django-filter  
pip install psycopg2-binary
```

- Inicie o servidor de desenvolvimento:

```python
python manage.py runserver
```
- Acesse *http://127.0.0.1:8000/api/* para ver as APIs funcionando.


