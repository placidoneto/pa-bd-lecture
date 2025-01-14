# Autenticação em Django Rest Framework

## Objetivo

O objetivo deste documento é apresentar um exemplo simples de como funciona a autenticação em Django Rest Framework. 

## Formas de autenticação

O Django Rest Framework oferece várias formas de autenticação. As principais são:

- JWTAuthentication
- TokenAuthentication
- BasicAuthentication

## JWTAuthentication

Esse tipo de autenticação é baseado em tokens. O token é gerado quando o usuário faz login e é enviado no cabeçalho da requisição. O token é gerado a partir de um payload que contém informações sobre o usuário. O token é assinado com uma chave secreta que só o servidor conhece. O token é enviado no cabeçalho da requisição e o servidor verifica se o token é válido. Se o token for válido, o usuário é autenticado. O token é válido por um determinado período de tempo, após esse período de tempo o token expira e o usuário precisa fazer login novamente. O Django Rest Framework oferece uma forma de gerar tokens JWT. Para gerar um token JWT, você precisa instalar a biblioteca SimpleJWT. Para instalar a biblioteca SimpleJWT, você pode fazer isso da seguinte forma:

```bash
pip install djangorestframework_simplejwt
```

Depois de instalar a biblioteca SimpleJWT, você precisa configurar o Django Rest Framework para usar o JWTAuthentication. Para configurar o Django Rest Framework para usar o JWTAuthentication, você precisa adicionar o JWTAuthentication ao DEFAULT_AUTHENTICATION_CLASSES do Django Rest Framework. Para fazer isso, você pode fazer isso da seguinte forma:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

Depois de configurar o Django Rest Framework para usar o JWTAuthentication, você precisa criar uma view para gerar o token JWT. Para criar uma view para gerar o token JWT, você pode fazer isso da seguinte forma:


O modelo de usuário do Django possui os seguintes campos:

- username
- password
- email
- first_name
- last_name

Caso seja necessário adicionar mais campos ao modelo de usuário, você pode fazer isso da seguinte forma:

```python
from django.contrib.auth.models import AbstractUser

class MeuUsuario(AbstractUser):
    cpf = models.CharField(max_length=11)
    data_nascimento = models.DateField()
    idade = models.IntegerField()
    endereco = models.CharField(max_length=255)
  
```

O serializer para o modelo de usuário ficaria da seguinte forma:

```python
from rest_framework import serializers

class MeuUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
       
```

O serializer acima é um exemplo de como você pode criar um serializer para o modelo de usuário. O campo password é um campo que não deve ser exibido para o usuário, por isso ele é marcado como write_only.

A classe view para o modelo de usuário ficaria da seguinte forma:

```python

## Permissions
from rest_framework.decorators import authentication_classes, permission_classes # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework.authentication import TokenAuthentication, SessionAuthentication # type: ignore
from django.shortcuts import get_object_or_404 # type: ignore

class MeuUsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MeuUsuarioSerializer


    @api_view(['POST'])
    def login(request):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({'message': 'Not Found!'}, status=status.HTTP_400_BAD_REQUEST)
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = MeuUsuarioSerializer(instance=user)
        return Response({'token': token.key, 'user':serializer.data})

    @api_view(['POST'])
    def signup(request):
        serializer = MeuUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user':serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    @authentication_classes([TokenAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated])
    def test_token(request):
        return Response("passou para {}".format(request.user.email))
```

## Criando uma arquivo de teste de api

```python

POST http://localhost:8000/api/signup
Content-Type: application/json

{
    "username": "placido1",
    "password": "placido1",
    "email": "placido1@gmail.com",
    "cpf": "12345678945"
}

###


POST http://localhost:8000/api/login
Content-Type: application/json

{
    "username": "placido1",
    "password": "placido1"
}


GET http://localhost:8000/test_token
Content-Type: application/json
Authorization: Token d13f275a6a8d2adc023398c557ac224acdce709f

```
