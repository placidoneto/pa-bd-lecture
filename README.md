# Autenticação em Django Rest Framework Usando Perfil de Usuário Especializado

Até o momento vimos 2 maneiras de autenticar usuários em Django Rest Framework. A primeira foi usando o modelo de usuário padrão do Django e a segunda foi usando um modelo de usuário personalizado através de um perfil. Neste aula vamos ver uma **terceira maneira** de autenticar usuários em Django Rest Framework. Vamos usar um modelo de usuário personalizado através de um perfil de usuário especializado. 

## Modelo de Usuário Personalizado

Vamos criar um modelo de usuário personalizado através de um perfil de usuário especializado. O perfil de usuário especializado é um modelo de usuário que contém um campo de relacionamento com o modelo de usuário criado. O campo de relacionamento é uma chave estrangeira que relaciona o perfil de usuário com o usuário padrão do Django.

Neste exemplo vamos especializar o modelo de usuário criando um perfil de usuário para alunos e professores. O perfil de usuário para alunos e professores contém um campo de matrícula. O campo de matrícula é um campo de texto que armazena a matrícula.

O modelo de usuário personalizado é composto por 2 modelos: o modelo de usuário (`User`) que herda de `AbstractUser` e o modelo de perfil de usuário, que é um modelo DEF comum. O modelo de perfil de usuário é o modelo especializado que contém um campo de relacionamento com o modelo de usuário.

```python
class User(AbstractUser):
    PERFIL = (
        ('admin', 'Administrador'),
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
        ('coordenador', 'Coordenador'),
        ('diretor', 'Diretor'),
    )
    perfil = models.CharField(max_length=15, choices=PERFIL)

class Aluno(models.Model):    
    matricula = models.CharField(max_length=10, unique=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='aluno')    


class Professor(models.Model):    
    matricula = models.CharField(max_length=10, unique=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='professor')  
```

O serializer de usuário personalizado é composto por 2 serializers: o serializer de usuário (`UserSerializer`) e o serializer de perfil de usuário (`AlunoSerializer` e `ProfessorSerializer`). O serializer de perfil de usuário é o serializer especializado que contém um campo de relacionamento com o serializer de usuário.

```python
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'perfil', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['matricula', 'user']           
        extra_kwargs = {'password': {'write_only': True}}

    user = UserSerializer()
    

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)      
        user_serializer.is_valid(raise_exception=True)

        user = user_serializer.save()

        aluno = Aluno.objects.create(user=user, **validated_data)
        return aluno


class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['matricula', 'user']           
        extra_kwargs = {'password': {'write_only': True}}

    user = UserSerializer()
    

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)      
        user_serializer.is_valid(raise_exception=True)

        user = user_serializer.save()

        professor = Professor.objects.create(user=user, **validated_data)
        return professor
```

É possível verificar no código acima que tanto o Aluno como o Professor tem um método create. O método create é responsável por criar um usuário e um perfil de usuário. 
O usuario é recuperado da requisição e é passado para o serializer de usuário. O serializer de usuário é responsável por criar um usuário. após a criação do usuário, o perfil de usuário é criado. Para isso é necessário passar o usuário criado para o perfil de usuário como um campo de relacionamento.

A classe view precisa conter os métodos de registro e autenticacao para os 2 novos perfis de usuário. 

```python

class AlunoRegistrationView(APIView):
    def post(self, request):
        serializer = AlunoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlunoLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token.delete()  # Deleta o token antigo
                token = Token.objects.create(user=user)

            response_data = {
                'token': token.key,
                'username': user.username,
                'perfil': user.perfil,
            }

            if user.perfil == 'aluno':
                aluno = user.aluno  # Assumindo que a relação tem nome "aluno"
                if aluno is not None:
                    # Adiciona os dados do aluno ao response_data
                    aluno_data = AlunoSerializer(aluno).data
                    response_data['data'] = aluno_data

            return Response(response_data)
        else:
            return Response({'message': 'Usuário ou Senha Inválido'}, status=status.HTTP_401_UNAUTHORIZED)
```

Perceba que o método de registro e autenticação para o aluno é semelhante ao método de registro e autenticação para o usuário padrão do Django. A diferença é que o método de registro e autenticação para o aluno é especializado para o perfil de aluno. O método de registro e autenticação para o aluno é responsável por criar um usuário e um perfil de aluno.

Uma vez a estrutura de autenticacao e registro está definida, é necessário configurar o endpoint de acesso a essas funcionalidades. 

```python

    path('api/auth/registro/aluno/', AlunoRegistrationView.as_view(), name='registro-aluno'),
    path('api/auth/login/aluno/', AlunoLoginView.as_view(), name='login-aluno'),

    path('api/auth/registro/professor/', ProfessorRegistrationView.as_view(), name='registro-professor'),
    path('api/auth/login/professor/', ProfessorLoginView.as_view(), name='login-professor'),
```

## Testando a Autenticação

Para testar a autenticação de alunos e professores, vamos usar o Postman ou o Insomnia. O Postman e o Insomnia são ferramentas de teste de API que permitem testar a autenticação de usuários em Django Rest Framework. Abaixo apresentamos como o Postman pode ser usado para testar a autenticação de alunos e professores.

Primeiro o usuario precisa ser criado: `http://localhost:8000/api/auth/registro/professor/` ou `http://localhost:8000/api/auth/registro/aluno/`


```json
{
    "matricula": "789456",
    "user":
        {
            "username": "placidoneto",
            "email": "placidoneto.doe@test.com",
            "perfil": "professor",
            "password": "placidoneto"
        }
}
```

Para realizar o login, o usuário precisa acessar o endpoint de login: `http://localhost:8000/api/auth/login/professor/` ou `http://localhost:8000/api/auth/login/aluno/`. O cabeção da requisição deve conter o username e a senha do usuário.

```json
{        
    "username": "placidoneto",
    "password": "placidoneto"
}
```

Após a autenticação, o token e os dados do usuário são retornados como resposta da requisição. O token é um código de acesso que permite ao usuário acessar recursos protegidos. Os dados do usuário são os dados do usuário autenticado, como o username, o perfil e a matrícula.

```json
{
    "token": "f53679577fc8059b78c4f3fe628875b648b4552d",
    "username": "placidoneto",
    "perfil": "professor",
    "data": {
        "matricula": "789456",
        "user": {
            "username": "placidoneto",
            "email": "placidoneto.doe@test.com",
            "perfil": "professor"
        }
    }
}
```

A verificação de validade e de exclusão do token é semelhante ao método de autenticação para o usuário padrão do Django. O token é verificado e excluído se já existir. O token é criado se não existir. O token é retornado como resposta da requisição.



## Referências

- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Django](https://www.djangoproject.com/)
- [Postman](https://www.postman.com/)
- [Insomnia](https://insomnia.rest/)
- [Django Models](https://docs.djangoproject.com/en/3.2/topics/db/models/)
- [Django Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [Django Views](https://docs.djangoproject.com/en/3.2/topics/http/views/)
- [Django Authentication](https://docs.djangoproject.com/en/3.2/topics/auth/)
- [Django Tokens](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
  