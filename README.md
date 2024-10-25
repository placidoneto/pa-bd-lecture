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

6. **URLs**

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

- Adicione *rest_framework* e *backend* ao *INSTALLED_APPS* no arquivo *amazon/settings.py*:

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
- Acesse *http://127.0.0.1:8000/amazon_api/* para ver as APIs funcionando.

Após rodar o servidor, acesse o painel de administração do Django em *http://localhost:8000/admin/* e faça login com o super usuário criado anteriormente. Você poderá adicionar, editar e excluir clientes no painel de administração. Essa forma de acessar os modelos é simples e mostra que os modelos estão funcionando e sendo salvos no banco de dados conforme o esperado. No entanto, para acessar os dados de forma mais estruturada, é necessário criar uma API RESTful com o Django Rest Framework. Os endpoints da API RESTful permitem acessar os dados de forma programática e realizar operações CRUD (Create, Retrieve, Update, Delete) nos modelos. Para acessar os endpoints, basta acessar a URL da API no navegador ou usar um cliente REST. Existem vários clientes REST como por exemplo o POSTMAN.

Caso você não queira usar um cliente REST, é possível acessar os endpoints da API RESTful diretamente no navegador. Por exemplo, para acessar a lista de clientes, basta acessar a URL *http://localhost:8000/amazon_api/clientes/* no navegador. Você verá uma lista de clientes em formato JSON. Para acessar um cliente específico, basta adicionar o ID do cliente à URL, por exemplo *http://localhost:8000/amazon_api/clientes/1/* para acessar o cliente com ID 1. Você verá os detalhes do cliente em formato JSON. Para criar um novo cliente, basta enviar uma requisição POST com os dados do cliente para a URL *http://localhost:8000/amazon_api/clientes/*. Alem de acessar pelo navegador é possível escrever um programa simples em python para acessar a API RESTful e manipular os dados dos modelos. 

```python
import requests

BASE_URL = 'http://localhost:8000/amazon_api/'

def get_clientes():
    response = requests.get(BASE_URL + 'clientes/')
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Exemplo de uso
if __name__ == '__main__':

    # Obter todos os clientes
    clientes = get_clientes()
    for cliente in clientes:
        print('Cliente:', cliente)
```

O exemplo acima mostra como acessar a API RESTful do Django Rest Framework para obter todos os clientes. A função *get_clientes* envia uma requisição GET para a URL *http://localhost:8000/amazon_api/clientes/* e retorna a lista de clientes em formato JSON. O programa principal mostra como usar a função *get_clientes* para obter e exibir todos os clientes. Você pode modificar o programa para realizar outras operações CRUD (Create, Retrieve, Update, Delete) nos modelos.

Perceba que é necessário importar a biblioteca `request`. Para instalar a biblioteca, basta rodar o comando `pip install requests`. 
A biblioteca `requests` é uma biblioteca HTTP para Python, que permite enviar requisições HTTP de forma simples e fácil. Ela fornece uma API simples e intuitiva para enviar e receber dados pela web. A biblioteca `requests` é amplamente utilizada para acessar APIs RESTful, fazer scraping de páginas web, além de poder realizar testes de integração.

Para facilitar o controle dos pacotes instalados no ambiente de execução do projeto, é possível criar um arquivo `requirements.txt` com os pacotes necessários para rodar o projeto. Para criar o arquivo, basta rodar o comando `pip freeze > requirements.txt`. O arquivo gerado conterá todos os pacotes instalados no ambiente de execução do projeto. Para instalar os pacotes listados no arquivo `requirements.txt`, basta rodar o comando `pip install -r requirements.txt`.

Para execução deste exemplo o arquivo `requirements.txt` pode ser criado com o seguinte conteúdo:

```
django
djangorestframework
djangorestframework-jwt
psycopg2-binary
requests
```

## Configurando o Swagger no Django Rest Framework

O Swagger é uma ferramenta de código aberto que permite documentar APIs RESTful de forma fácil e rápida. Ele fornece uma interface gráfica interativa para explorar e testar APIs RESTful. O Swagger é amplamente utilizado para documentar APIs RESTful em várias linguagens de programação, incluindo Python.

Para configurar o Swagger no Django Rest Framework, é necessário instalar o pacote `drf-yasg`. O `drf-yasg` é um pacote que fornece suporte para o Swagger no Django Rest Framework. Ele permite gerar automaticamente a documentação da API RESTful com base nos serializers, views e modelos do Django Rest Framework. O `drf-yasg` é fácil de usar e fornece uma interface gráfica interativa para explorar e testar APIs RESTful. Para instalar o `drf-yasg`, basta rodar o comando `pip install drf-yasg`.

Para configurar o Swagger no Django Rest Framework, é necessário adicionar o `drf-yasg` ao `INSTALLED_APPS` no arquivo `settings.py` do projeto:

```python
INSTALLED_APPS = [
    ...
    'drf_yasg',
]
```

Em seguida, é necessário adicionar as URLs do `drf-yasg` ao arquivo `urls.py` do projeto:

```python
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation with Swagger",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

O código acima define as URLs do Swagger e do ReDoc no Django Rest Framework. A URL `/swagger/` é usada para acessar a interface gráfica do Swagger, que permite explorar e testar a API RESTful. A URL `/redoc/` é usada para acessar a interface gráfica do ReDoc, que fornece uma documentação mais limpa e organizada da API RESTful. O `cache_timeout=0` é usado para desativar o cache das páginas do Swagger e do ReDoc, garantindo que as alterações na API sejam refletidas imediatamente.

Para acessar a interface gráfica do Swagger, basta acessar a URL `http://localhost:8000/swagger/` no navegador. Você verá a documentação da API RESTful gerada automaticamente com base nos serializers, views e modelos do Django Rest Framework. A interface gráfica do Swagger permite explorar e testar os endpoints da API RESTful de forma interativa. Você pode enviar requisições GET, POST, PUT e DELETE para os endpoints da API e ver as respostas em formato JSON. A interface gráfica do Swagger é uma ferramenta poderosa para documentar e testar APIs RESTful de forma fácil e rápida.

Para acessar a interface gráfica do ReDoc, basta acessar a URL `http://localhost:8000/redoc/` no navegador. Você verá a documentação da API RESTful gerada automaticamente com base nos serializers, views e modelos do Django Rest Framework. A interface gráfica do ReDoc fornece uma documentação mais limpa e organizada da API RESTful, facilitando a leitura e compreensão dos endpoints da API. O ReDoc é uma alternativa ao Swagger e fornece uma documentação mais amigável e visualmente atraente da API RESTful.
