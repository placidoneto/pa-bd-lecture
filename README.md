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
    /backend
        /migrations
        __init__.py
        admin.py
        apps.py
        models.py
        serializers.py
        tests.py
        urls.py
        views.py
manage.py
```

   - Adicione o aplicativo ao *INSTALLED_APPS* no arquivo *amazon/settings.py*:

```python
INSTALLED_APPS = [
    ...
    'backend',
]
```

É necessário incluir o app *rest_framework* no arquivo *amazon/settings.py*, da mesma forma que foi feito com o app *backend*:



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

A configuração da base de dados postgres no django é feita da seguinte forma. Para definir o banco como padrão é necessário definir o *ENGINE* como *django.db.backends.postgresql* e informar o nome do banco, usuário, senha, host e porta. No exemplo acima, o banco de dados é *nome_do_banco*, o usuário é *seu_usuario* e a senha é *sua_senha* devem ser inseridos de acordo com a sua configuração de banco.

3. **Modelos (Models)**

- Edite o arquivo *backend/models.py* para definir os modelos que se transformarão em tabelas no banco de dados:

```python
from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)
    data_cadastro = models.DateTimeField(auto_now_add=True)    

    def __str__(self):
        return self.nome
```

Iniciamos com um exemplo super simples, onde temos um modelo *Cliente* com os campos *nome*, *email*, *telefone* e *data_cadastro*. O campo *data_cadastro* é do tipo *DateTimeField* e é preenchido automaticamente com a data e hora atuais quando um novo cliente é cadastrado. O método *__str__* é usado para retornar o nome do cliente quando ele é exibido em uma lista. Se for necessário retornar mais de um atributo, basta concatenar os atributos separados por vírgula, como por exemplo: *return f'{self.nome} - {self.email}'*.

```python
def __str__(self):
        return f'{self.nome} - {self.email}'
```


4. **Serializers**

- Crie o arquivo *backend/serializers.py* e adicione os serializers:

```python
from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__' 
```

O arquivo *serializers.py* é responsável por serializar os dados dos modelos para JSON. No exemplo acima, criamos um serializer para o modelo *Cliente* que inclui todos os campos do modelo. Se for necessário incluir apenas alguns campos, basta informar os campos desejados na lista *fields*, como por exemplo: *fields = ['nome', 'email']*.
A serialização é o processo de converter um objeto em uma sequência de bytes para ser armazenado ou transmitido para um banco de dados, arquivo ou outro meio de armazenamento. A deserialização é o processo inverso, onde a sequência de bytes é convertida de volta para um objeto.

Django Rest Framework fornece um conjunto de classes de serialização que permitem a serialização de objetos complexos, como modelos, consultas e listas de objetos. Os serializers do Django Rest Framework são semelhantes aos formulários do Django, mas são mais poderosos e flexíveis. Eles permitem a validação dos dados, a conversão de tipos de dados e a serialização de objetos complexos.  

5. **Views**

- Edite o arquivo *backend/views.py* para adicionar as views:

```python
from django.shortcuts import render
from rest_framework import viewsets
from .models import Cliente
from .serializers import ClienteSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer 

```

O arquivo *views.py* é responsável por definir as views que serão usadas para manipular os dados. No exemplo acima, criamos uma view *ClienteViewSet* que herda de *viewsets.ModelViewSet*. O *ModelViewSet* fornece ações CRUD (Create, Retrieve, Update, Delete) para um modelo específico. O *queryset* define a consulta que será usada para recuperar os objetos do banco de dados. O *serializer_class* define o serializer que será usado para serializar os objetos recuperados do banco de dados. 

O Django Rest Framework fornece um conjunto de classes de visualização que permitem a criação de APIs RESTful de forma rápida e fácil. As classes de visualização do Django Rest Framework são semelhantes às views do Django, mas são mais poderosas e flexíveis. Elas permitem a criação de APIs RESTful com CRUD (Create, Retrieve, Update, Delete) para modelos específicos, consultas personalizadas e operações complexas. 



1. **URLs**

- Edite o arquivo *amazon/urls.py* para incluir as rotas:

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend import views

router = DefaultRouter()
router.register(r'clientes', views.ClienteViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('amazon_api/', include(router.urls)),
]
```

O arquivo *urls.py* é responsável por definir as rotas que serão usadas para acessar as views. No exemplo acima, criamos um *DefaultRouter* que inclui a rota *clientes* para acessar a view *ClienteViewSet*. A rota *clientes* será mapeada para a view *ClienteViewSet* e fornecerá as ações CRUD (Create, Retrieve, Update, Delete) para o modelo *Cliente*.

O urlpatterns é uma lista de rotas que serão usadas para acessar as views. A rota *admin/* é usada para acessar o painel de administração do Django. A rota *amazon_api/* é usada para acessar a API RESTful criada com o Django Rest Framework. A função *include(router.urls)* é usada para incluir as rotas do *DefaultRouter* no urlpatterns.

PAra permitir os cadastros dos modelos no admin, é necessário registrar os modelos no arquivo *admin.py* do aplicativo:

```python
from django.contrib import admin
from .models import Cliente

admin.site.register(Cliente)
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

- Criando um super usuário no django:

```python
python manage.py createsuperuser
```

- Inicie o servidor de desenvolvimento:

```python
python manage.py runserver
```
- Acesse *http://127.0.0.1:8000/api/* para ver as APIs funcionando.


