# Django Rest - Basic Authentication

## Basic Authentication

O Django Rest Framework fornece uma autenticação básica que é uma forma simples de autenticação que é feita através de um nome de usuário e senha. A autenticação básica é feita através de um cabeçalho de autorização que é enviado com a requisição. O cabeçalho de autorização é formado pela palavra `Basic` seguida de um espaço e de um nome de usuário e senha codificados em base64. O nome de usuário e senha são separados por dois pontos. O cabeçalho de autorização é enviado com a requisição no formato `Authorization: Basic <nome de usuário:senha>`. O Django Rest Framework fornece uma classe chamada `BasicAuthentication` que é uma classe de autenticação básica. Esta classe é usada para autenticar um usuário através de um nome de usuário e senha.

Para usar a autenticação básica é necessário adicionar a classe `BasicAuthentication` à lista de autenticação padrão. A lista de autenticação padrão é uma lista de classes de autenticação que são usadas para autenticar um usuário. A lista de autenticação padrão é definida no arquivo de configuração `settings.py`. O conteúdo do arquivo `settings.py` é mostrado abaixo. A lista de autenticação padrão é definida pela variável `DEFAULT_AUTHENTICATION_CLASSES`. A variável `DEFAULT_AUTHENTICATION_CLASSES` é uma lista de classes de autenticação que são usadas para autenticar um usuário. A classe `BasicAuthentication` é adicionada à lista de autenticação padrão.

Então como usar esse tipo de autenticação para acessar as funções da `view`? 

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
```

A outra maneira de usar a autenticação básica é adicionar a classe `BasicAuthentication` à lista de autenticação de uma `view`. A lista de autenticação de uma `view` é uma lista de classes de autenticação que são usadas para autenticar um usuário. A lista de autenticação de uma `view` é definida no atributo `authentication_classes` da `view`. O conteúdo da `view` é mostrado abaixo. A classe `ListarAlunos` é uma subclasse de `ListAPIView` e possui um atributo `authentication_classes` que é uma lista de classes de autenticação. A classe `BasicAuthentication` é adicionada à lista de autenticação da `view`.

```python
...
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

...

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

```


## Conclusão

Nesta aula, vimos como usar a autenticação básica no Django Rest Framework. A autenticação básica é uma forma simples de autenticação que é feita através de um nome de usuário e senha. A autenticação básica é feita através de um cabeçalho de autorização que é enviado com a requisição. O cabeçalho de autorização é formado pela palavra `Basic` seguida de um espaço e de um nome de usuário e senha codificados em base64. O nome de usuário e senha são separados por dois pontos. O Django Rest Framework fornece uma classe chamada `BasicAuthentication` que é uma classe de autenticação básica. Esta classe é usada para autenticar um usuário através de um nome de usuário e senha. A autenticação básica pode ser usada adicionando a classe `BasicAuthentication` à lista de autenticação padrão ou adicionando a classe `BasicAuthentication` à lista de autenticação de uma `view`.

## Referências

[Documentação Oficial do Django Rest Framework](https://www.django-rest-framework.org/)

[Documentação Oficial do Django](https://www.djangoproject.com/)

[Python Brasil](https://python.org.br/)