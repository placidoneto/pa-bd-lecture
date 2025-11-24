# Autenticação em Django Rest Framework Usando Perfil de Usuário
## Estudo de Caso usando JWT

O JSON Web Token (JWT) é um padrão de autenticação amplamente utilizado em aplicações modernas, especialmente em arquiteturas de APIs RESTful. No Django Rest Framework, o JWT oferece uma alternativa robusta e escalável aos tokens tradicionais baseados em sessão. Diferentemente dos tokens de sessão que são armazenados no banco de dados, o JWT é um token autocontido que carrega informações codificadas sobre o usuário, como seu identificador e permissões, eliminando a necessidade de consultas constantes ao banco de dados para validação. A biblioteca `djangorestframework-simplejwt` facilita a implementação do JWT no Django, fornecendo endpoints prontos para geração de tokens de acesso e refresh. O token de acesso tem vida curta (geralmente 5 a 15 minutos) e é usado para autenticar requisições, enquanto o token de refresh permite obter novos tokens de acesso sem exigir que o usuário faça login novamente. Esta abordagem proporciona maior segurança, pois reduz a exposição do token de acesso, além de melhorar a performance da aplicação ao minimizar operações de leitura no banco de dados durante a autenticação.

```bash
# Criar pasta do projeto
mkdir autenticacao_jwt
cd autenticacao_jwt

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# No Linux/Mac:
source venv/bin/activate
# No Windows:
# venv\Scripts\activate

# Instalar dependências
pip install django djangorestframework djangorestframework-simplejwt django-cors-headers
```



```bash
# Criar projeto
django-admin startproject oficina .

# Criar app
python manage.py startapp auth
```

Os comandos acima são fundamentais para estruturar o projeto Django. O comando `django-admin startproject oficina .` cria a estrutura básica do projeto Django chamado "oficina" no diretório atual, indicado pelo ponto (`.`). Isso gera arquivos essenciais como `manage.py`, que é a interface de linha de comando do projeto, além da pasta de configurações contendo `settings.py`, `urls.py` e `wsgi.py`. Em seguida, o comando `python manage.py startapp auth` cria uma aplicação Django denominada "auth", que funcionará como um módulo específico dentro do projeto. Esta aplicação será responsável por toda a lógica relacionada à autenticação de usuários, perfis e permissões, mantendo o código organizado e modular.

```python
from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
   
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Perfil(models.Model):
    
    TIPO_PERFIL_CHOICES = [
        ('GERENTE', 'Gerente'),
        ('CLIENTE', 'Cliente'),
        ('MECANICO', 'Mecânico'),
    ]
    
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='perfil'
    )
    tipo = models.CharField(
        max_length=20, 
        choices=TIPO_PERFIL_CHOICES
    )
    telefone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()}"
```

O código acima define dois modelos para o sistema de autenticação com perfis de usuário. A classe `Usuario` estende `AbstractUser`, que é a classe abstrata do Django contendo todos os campos básicos de autenticação (username, password, email, etc.). Ao estender `AbstractUser`, criamos um modelo de usuário personalizado que substitui o modelo padrão do Django, permitindo adicionar campos customizados. Neste caso, o campo `email` foi redefinido com a restrição `unique=True`, garantindo que cada usuário tenha um email único no sistema. O método `__str__` retorna o nome de usuário para facilitar a identificação do objeto.

A classe `Perfil` implementa um relacionamento one-to-one (um-para-um) com o modelo `Usuario`, ou seja, cada usuário possui exatamente um perfil associado. O campo `usuario` utiliza `OneToOneField` com `on_delete=models.CASCADE`, o que significa que quando um usuário for deletado, seu perfil também será removido automaticamente. O parâmetro `related_name='perfil'` permite acessar o perfil a partir do usuário usando `usuario.perfil`. O campo `tipo` armazena o tipo de perfil do usuário (Gerente, Cliente ou Mecânico) utilizando `choices`, que restringe os valores possíveis apenas às opções definidas em `TIPO_PERFIL_CHOICES`. O campo `telefone` é opcional (`blank=True`), permitindo que o perfil seja criado sem a informação de telefone. O método `get_tipo_display()` usado no `__str__` retorna automaticamente a versão legível do tipo (ex: "Gerente" ao invés de "GERENTE"), facilitando a apresentação dos dados.




```python
# Adicionar aos INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Apps de terceiros
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    
    # Apps locais
    'auth',
]

# Adicionar middleware do CORS (no início da lista)
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Adicionar esta linha
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configurar modelo de usuário customizado
AUTH_USER_MODEL = 'auth.Usuario'

# Configurações do REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# Configurações do JWT
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# Configurações do CORS (permitir requisições do frontend)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite usa essa porta por padrão
    "http://127.0.0.1:5173",
]

CORS_ALLOW_CREDENTIALS = True
```

O código acima apresenta as configurações essenciais do arquivo `settings.py` do Django para habilitar a autenticação JWT com perfis de usuário. Na seção `INSTALLED_APPS`, são registradas todas as aplicações necessárias: os apps padrão do Django (`admin`, `auth`, `contenttypes`, etc.), os apps de terceiros instalados via pip (`rest_framework` para criar a API REST, `rest_framework_simplejwt` para implementar JWT, e `corsheaders` para permitir requisições cross-origin) e o app local `auth` que contém os modelos de usuário e perfil criados anteriormente.

Na configuração do `MIDDLEWARE`, o `CorsMiddleware` é adicionado no topo da lista, pois middlewares são executados em ordem e o CORS precisa processar requisições antes dos demais middlewares. Isso permite que o frontend React (rodando em uma porta diferente) faça requisições para a API Django sem ser bloqueado pela política de mesma origem do navegador.

A configuração `AUTH_USER_MODEL = 'auth.Usuario'` é crucial, pois informa ao Django para usar o modelo `Usuario` personalizado (criado anteriormente) ao invés do modelo `User` padrão. Isso deve ser definido antes de executar as migrações, caso contrário será necessário recriar o banco de dados.

A seção `REST_FRAMEWORK` define que a autenticação padrão da API será via JWT através da classe `JWTAuthentication`. Isso significa que todas as requisições autenticadas devem incluir um token JWT válido no cabeçalho Authorization.

As configurações do `SIMPLE_JWT` definem os tempos de vida dos tokens: `ACCESS_TOKEN_LIFETIME` de 60 minutos para o token de acesso (usado para autenticar requisições) e `REFRESH_TOKEN_LIFETIME` de 1 dia para o token de refresh (usado para obter novos tokens de acesso sem fazer login novamente). Esses valores podem ser ajustados conforme as necessidades de segurança da aplicação.

Por fim, as configurações de CORS (`CORS_ALLOWED_ORIGINS`) especificam as URLs permitidas para fazer requisições à API - neste caso, as portas locais onde o Vite executa o frontend React (5173). A configuração `CORS_ALLOW_CREDENTIALS = True` permite que cookies e credenciais sejam enviados nas requisições cross-origin, necessário para autenticação.





```python
from rest_framework import serializers
from .models import Usuario, Perfil

class PerfilSerializer(serializers.ModelSerializer):
    
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Perfil
        fields = ['tipo', 'tipo_display', 'telefone']


class UsuarioSerializer(serializers.ModelSerializer):
    
    perfil = PerfilSerializer(read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'perfil']


class RegistroSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    tipo_perfil = serializers.ChoiceField(
        choices=Perfil.TIPO_PERFIL_CHOICES,
        write_only=True
    )
    telefone = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'tipo_perfil', 'telefone'
        ]
    
    def validate(self, data):
        """
        Validar se as senhas coincidem
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'As senhas não coincidem.'
            })
        return data
    
    def create(self, validated_data):
        """
        Criar usuário e perfil associado
        """
        # Remover campos que não fazem parte do modelo Usuario
        validated_data.pop('password_confirm')
        tipo_perfil = validated_data.pop('tipo_perfil')
        telefone = validated_data.pop('telefone', '')
        
        # Criar usuário
        usuario = Usuario.objects.create_user(**validated_data)
        
        # Criar perfil associado
        Perfil.objects.create(
            usuario=usuario,
            tipo=tipo_perfil,
            telefone=telefone
        )
        
        return usuario
```

O código acima define três serializers essenciais para o sistema de autenticação com JWT. Os serializers no Django Rest Framework são responsáveis por converter objetos complexos (como modelos do Django) em tipos de dados Python nativos que podem ser facilmente renderizados em JSON, e vice-versa, além de validar dados de entrada.

### PerfilSerializer

A classe `PerfilSerializer` é responsável por serializar os dados do modelo `Perfil`. Ela herda de `ModelSerializer`, que automaticamente gera campos baseados no modelo especificado. O campo `tipo_display` utiliza `source='get_tipo_display'` para acessar o método automático do Django que retorna a versão legível do campo `tipo` (por exemplo, "Gerente" ao invés de "GERENTE"). O parâmetro `read_only=True` indica que esse campo é apenas para leitura e não pode ser modificado diretamente via API. A classe `Meta` define o modelo associado (`Perfil`) e os campos que serão incluídos na serialização: `tipo` (valor armazenado no banco), `tipo_display` (versão legível) e `telefone`.

### UsuarioSerializer

A classe `UsuarioSerializer` serializa os dados do modelo `Usuario` e inclui o perfil associado. O campo `perfil` utiliza o `PerfilSerializer` como serializer aninhado (nested serializer), permitindo que os dados do perfil sejam incluídos automaticamente na resposta JSON quando um usuário é serializado. O parâmetro `read_only=True` indica que o perfil não pode ser criado ou modificado através deste serializer - ele apenas será exibido nas respostas. A classe `Meta` define que serão serializados os campos: `id`, `username`, `email`, `first_name`, `last_name` e o objeto `perfil` completo. Este serializer é usado principalmente para listar e detalhar usuários existentes.

### RegistroSerializer

A classe `RegistroSerializer` é o mais complexo dos três e é responsável por registrar novos usuários com seus perfis. Os campos `password` e `password_confirm` utilizam `write_only=True`, garantindo que as senhas nunca sejam incluídas nas respostas da API (apenas aceitas na entrada). O parâmetro `min_length=6` estabelece uma validação mínima de 6 caracteres para as senhas. O campo `tipo_perfil` utiliza `ChoiceField` com as opções definidas em `TIPO_PERFIL_CHOICES`, restringindo os valores aceitos. O campo `telefone` tem `required=False` e `allow_blank=True`, tornando-o opcional.

O método `validate(self, data)` é um método de validação customizado que é executado automaticamente durante a validação dos dados. Ele recebe o dicionário `data` com todos os campos validados individualmente e permite validações que envolvem múltiplos campos. Neste caso, verifica se `password` e `password_confirm` são iguais. Se não forem, levanta um `ValidationError` com uma mensagem específica para o campo `password_confirm`. Este método é chamado antes de `create()` e garante a integridade dos dados.

O método `create(self, validated_data)` é responsável por criar o usuário e seu perfil associado. Primeiro, remove do dicionário `validated_data` os campos que não pertencem ao modelo `Usuario`: `password_confirm` (usado apenas para validação), `tipo_perfil` e `telefone` (que pertencem ao modelo `Perfil`). Em seguida, utiliza `Usuario.objects.create_user(**validated_data)` ao invés de `create()`, pois `create_user()` é um método especial que automaticamente faz o hash da senha antes de salvá-la no banco de dados, garantindo segurança. Após criar o usuário, cria o perfil associado utilizando `Perfil.objects.create()`, estabelecendo o relacionamento one-to-one entre usuário e perfil. Finalmente, retorna o objeto `usuario` criado, que será serializado e retornado na resposta da API.



```python
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistroSerializer, UsuarioSerializer

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registro_view(request):
    """
    Endpoint para registro de novos usuários
    POST /api/registro/
    
    Body esperado:
    {
        "username": "joao",
        "email": "joao@email.com",
        "password": "senha123",
        "password_confirm": "senha123",
        "first_name": "João",
        "last_name": "Silva",
        "tipo_perfil": "CLIENTE",
        "telefone": "84999999999"
    }
    """
    serializer = RegistroSerializer(data=request.data)
    
    if serializer.is_valid():
        usuario = serializer.save()
        
        # Gerar tokens JWT
        refresh = RefreshToken.for_user(usuario)
        
        return Response({
            'message': 'Usuário registrado com sucesso!',
            'user': UsuarioSerializer(usuario).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def usuario_atual_view(request):
    """
    Endpoint para obter dados do usuário autenticado
    GET /api/usuario/
    
    Header necessário:
    Authorization: Bearer <access_token>
    """
    serializer = UsuarioSerializer(request.user)
    return Response(serializer.data)
```

O código acima define duas views (funções de visualização) que implementam endpoints da API para registro de usuários e obtenção de dados do usuário autenticado. As views no Django Rest Framework são responsáveis por receber requisições HTTP, processar os dados e retornar respostas apropriadas.

### Imports e Dependências

As primeiras linhas importam os módulos necessários: `status` e `permissions` do `rest_framework` para gerenciar códigos de status HTTP e permissões; `api_view` e `permission_classes` são decoradores que transformam funções Python em endpoints da API; `Response` é usado para retornar respostas HTTP; `RefreshToken` do `rest_framework_simplejwt` gera tokens JWT; e os serializers `RegistroSerializer` e `UsuarioSerializer` são importados para validação e serialização de dados.

### registro_view

A função `registro_view` é decorada com `@api_view(['POST'])`, indicando que aceita apenas requisições do tipo POST. O decorador `@permission_classes([permissions.AllowAny])` permite que qualquer pessoa (autenticada ou não) acesse este endpoint, pois é usado para criar novos usuários. A docstring documenta o endpoint, mostrando a URL (`/api/registro/`) e o formato esperado do corpo da requisição em JSON.

Dentro da função, `serializer = RegistroSerializer(data=request.data)` cria uma instância do serializer com os dados recebidos na requisição. O método `serializer.is_valid()` valida todos os dados de acordo com as regras definidas no `RegistroSerializer`, incluindo a validação customizada que verifica se as senhas coincidem. Se os dados forem válidos, `serializer.save()` chama o método `create()` do serializer, criando tanto o usuário quanto seu perfil associado no banco de dados.

Após criar o usuário, a linha `refresh = RefreshToken.for_user(usuario)` gera automaticamente um par de tokens JWT (refresh e access) para o usuário recém-criado. O método `for_user()` cria tokens contendo informações do usuário codificadas. A resposta retorna três elementos: uma mensagem de sucesso, os dados do usuário serializado usando `UsuarioSerializer` (incluindo o perfil), e os tokens JWT. O token `refresh` tem vida longa (1 dia) e é usado para obter novos tokens de acesso, enquanto `refresh.access_token` tem vida curta (60 minutos) e é usado para autenticar requisições à API. O status `HTTP_201_CREATED` (código 201) indica que o recurso foi criado com sucesso.

Se os dados não forem válidos, a função retorna `serializer.errors` contendo as mensagens de erro específicas de cada campo, com status `HTTP_400_BAD_REQUEST` (código 400), indicando que há problemas nos dados enviados.

### usuario_atual_view

A função `usuario_atual_view` é decorada com `@api_view(['GET'])`, aceitando apenas requisições GET. O decorador `@permission_classes([permissions.IsAuthenticated])` exige que o usuário esteja autenticado para acessar este endpoint. Isso significa que a requisição deve incluir um token JWT válido no cabeçalho `Authorization: Bearer <access_token>`. O Django Rest Framework automaticamente valida o token e disponibiliza o usuário autenticado em `request.user`.

A docstring documenta que este endpoint retorna os dados do usuário atualmente autenticado. Dentro da função, `serializer = UsuarioSerializer(request.user)` serializa os dados do usuário autenticado (obtido automaticamente do token JWT). Como `request.user` já é uma instância do modelo `Usuario` (não um dicionário de dados), passamos o objeto diretamente ao serializer sem o parâmetro `data=`. O serializer automaticamente inclui o perfil associado, graças ao nested serializer configurado. Por fim, `Response(serializer.data)` retorna os dados serializados em formato JSON com status HTTP 200 OK (padrão quando não especificado).

Este endpoint é útil para que o frontend obtenha informações do usuário logado, como nome, email e tipo de perfil, permitindo exibir esses dados na interface e implementar controle de acesso baseado no tipo de perfil.



#### Arquivo: `auth/urls.py` (criar este arquivo)

```python
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import registro_view, usuario_atual_view

urlpatterns = [
    # Endpoint de registro
    path('registro/', registro_view, name='registro'),
    
    # Endpoints de autenticação JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Endpoint para obter usuário atual
    path('usuario/', usuario_atual_view, name='usuario_atual'),
]
```

O código acima define as rotas (URLs) da aplicação de autenticação. O arquivo `auth/urls.py` mapeia URLs específicas para suas respectivas views e endpoints. A primeira linha importa a função `path` do Django para criar rotas, seguida pela importação de duas views prontas do `rest_framework_simplejwt`: `TokenObtainPairView` (para login e obtenção de tokens) e `TokenRefreshView` (para renovar tokens de acesso expirados). As views customizadas `registro_view` e `usuario_atual_view` também são importadas.

A lista `urlpatterns` define quatro endpoints principais. O endpoint `registro/` está mapeado para a view `registro_view`, permitindo que novos usuários se cadastrem. O endpoint `login/` utiliza `TokenObtainPairView.as_view()`, que é uma view baseada em classe fornecida pela biblioteca JWT - ela recebe username e password no corpo da requisição e retorna um par de tokens (access e refresh) se as credenciais forem válidas. O endpoint `token/refresh/` usa `TokenRefreshView.as_view()` para permitir que clientes renovem seus tokens de acesso enviando o token refresh válido, obtendo assim um novo token de acesso sem precisar fazer login novamente. Por fim, o endpoint `usuario/` mapeia para `usuario_atual_view`, retornando os dados do usuário autenticado. Cada rota possui um parâmetro `name` que permite referenciá-las de forma fácil em outras partes do código Django.

#### Arquivo: `config/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('auth.urls')),
]
```

O código acima configura as URLs principais do projeto Django no arquivo `config/urls.py` (ou `oficina/urls.py`, dependendo do nome dado ao projeto). Este arquivo serve como ponto central de roteamento de toda a aplicação. A função `include` é importada para permitir a inclusão de arquivos de URLs de outras aplicações.

A lista `urlpatterns` define duas rotas principais. A primeira, `path('admin/', admin.site.urls)`, configura o painel administrativo do Django, acessível em `/admin/`, onde é possível gerenciar usuários, perfis e outros modelos através de uma interface web. A segunda rota, `path('api/', include('auth.urls'))`, é crucial pois inclui todas as URLs definidas no arquivo `auth/urls.py` com o prefixo `/api/`. Isso significa que os endpoints ficam acessíveis como `/api/registro/`, `/api/login/`, `/api/token/refresh/` e `/api/usuario/`. O uso de `include()` permite organização modular, onde cada aplicação Django pode ter seu próprio arquivo de URLs, mantendo o código limpo e facilitando a manutenção em projetos maiores.

###  Configurar o Admin (opcional mas útil)

#### Arquivo: `auth/admin.py`

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Perfil

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff']
    
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'tipo', 'telefone']
    list_filter = ['tipo']
```

O código acima configura o painel administrativo do Django para os modelos `Usuario` e `Perfil`. O arquivo `admin.py` é usado para customizar a interface administrativa, tornando a gestão de dados mais eficiente e intuitiva.

O decorador `@admin.register(Usuario)` registra o modelo `Usuario` no painel admin e associa a ele a classe de configuração `UsuarioAdmin`. Esta classe herda de `UserAdmin`, que é a classe de administração padrão para modelos de usuário do Django, fornecendo funcionalidades prontas como gestão de permissões, grupos e senhas. A propriedade `list_display` define quais campos serão exibidos na listagem de usuários no admin: username, email, first_name, last_name e is_staff (que indica se o usuário tem acesso ao admin). Isso facilita a visualização rápida das informações principais de cada usuário.

Similarmente, o decorador `@admin.register(Perfil)` registra o modelo `Perfil` e a classe `PerfilAdmin` herda de `ModelAdmin`, a classe base para administração de modelos no Django. A propriedade `list_display = ['usuario', 'tipo', 'telefone']` define que na listagem de perfis serão exibidos o usuário associado, o tipo de perfil e o telefone. A propriedade `list_filter = ['tipo']` adiciona um filtro lateral na interface admin permitindo filtrar perfis por tipo (Gerente, Cliente ou Mecânico), tornando mais fácil encontrar perfis específicos quando há muitos registros no sistema. Esta configuração é especialmente útil durante o desenvolvimento e para administradores que precisam gerenciar usuários manualmente.

###  Executar Migrações e Criar Superusuário

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário (para acessar o admin)
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver
```

Os comandos acima são essenciais para preparar e executar o projeto Django. O processo de migrações é fundamental para sincronizar os modelos Python com o banco de dados.

O comando `python manage.py makemigrations` analisa todos os modelos definidos nas aplicações instaladas (especialmente os modelos `Usuario` e `Perfil` criados anteriormente) e gera arquivos de migração Python na pasta `migrations/` de cada aplicação. Esses arquivos contêm instruções sobre as alterações necessárias no banco de dados, como criar novas tabelas, adicionar campos ou modificar estruturas existentes. É importante executar este comando sempre que houver mudanças nos modelos.

O comando `python manage.py migrate` aplica todas as migrações pendentes ao banco de dados, executando as instruções SQL necessárias para criar tabelas, índices e relacionamentos. Este comando deve ser executado após `makemigrations` e sempre que o banco de dados precisa ser atualizado. Ele também cria as tabelas padrão do Django, como as de autenticação, sessões e admin.

O comando `python manage.py createsuperuser` inicia um processo interativo que solicita username, email e password para criar um superusuário - um usuário com todas as permissões administrativas. Este superusuário é necessário para acessar o painel administrativo em `/admin/` e gerenciar usuários, perfis e outros dados através da interface web. Durante a criação, um perfil pode ser associado manualmente através do admin ou via código.

Por fim, o comando `python manage.py runserver` inicia o servidor de desenvolvimento do Django, geralmente na porta 8000 (acessível em `http://localhost:8000/` ou `http://127.0.0.1:8000/`). Este servidor é adequado apenas para desenvolvimento local, pois recarrega automaticamente quando arquivos são modificados, facilitando o processo de desenvolvimento. Para produção, deve-se usar servidores como Gunicorn ou uWSGI com Nginx.


### Testar os Endpoints (com curl ou Postman)

#### Teste 1: Registrar usuário

```bash
curl -X POST http://localhost:8000/api/registro/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "maria",
    "email": "maria@email.com",
    "password": "senha123",
    "password_confirm": "senha123",
    "first_name": "Maria",
    "last_name": "Santos",
    "tipo_perfil": "GERENTE",
    "telefone": "84988887777"
  }'
```

#### Teste 2: Fazer login

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "maria",
    "password": "senha123"
  }'
```

#### Teste 3: Obter dados do usuário autenticado

```bash
curl -X GET http://localhost:8000/api/usuario/ \
  -H "Authorization: Bearer <seu_access_token_aqui>"
```

