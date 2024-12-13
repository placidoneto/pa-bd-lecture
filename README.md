# Django Rest - ListAPIView

## ListAPIView

O pacote `rest_framework.generics` fornece uma classe chamada `ListAPIView` que é uma classe genérica de API de visualização que fornece uma funcionalidade de listagem básica para um modelo. Esta classe fornece um método `get` que retorna uma resposta de lista de objetos.

Imagine que eu tenha um modelo chamado `Aluno`, outro modelo chamado `Curso` e por fim um modelo chamado `Matricula`. O modelo `Matricula` é uma tabela de relacionamento entre `Aluno` e `Curso`. A classe `ListAPIView` pode ser usada para listar todas as matrículas de um aluno.

Antes de criar a classe que utiliza a `ListAPIView`, é necessário criar os modelos e os serializers.
O conteúdo dos serializers é mostrado abaixo. Perceba que a classe `ListarMatriculasAlunoSerializer` é uma subclasse de `serializers.ModelSerializer` e possui um método `get_periodo` que retorna o período da matrícula. A subclasse `Meta` é usada para definir o modelo e os campos que serão serializados. Para isso é o modelo da classe `Meta` é o modelo `Matricula` e os campos são `curso` e `periodo`. O campo `curso` é um campo somente leitura e o campo `periodo` é um campo que chama o método `get_periodo`. O método `get_periodo` retorna o período da matrícula.  


```python
from rest_framework import serializers
from escola.models import Aluno, Curso, Matricula

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        exclude = [id]
        fields = '__all__'

class ListarMatriculasAlunoSerializer(serializers.ModelSerializer):
    curso = serializers.ReadOnlyField(source='curso.descricao')
    periodo = serializers.SerializerMethodField()

    class Meta:
        model = Matricula
        fields = ['curso', 'periodo']

    def get_periodo(self, obj):
        return obj.get_periodo_display()
```

Uma vez criado o serializer, é necessário criar a classe que utiliza a `ListAPIView`. O conteúdo da classe é mostrado abaixo. A classe `ListarMatriculasAluno` é uma subclasse de `ListAPIView` e possui um método `get_queryset` que retorna todas as matrículas de um aluno específico. O método `get_queryset` recebe o id do aluno e retorna todas as matrículas do aluno. O método `get_queryset` é chamado pelo método `get` que retorna uma resposta de lista de objetos. Perceba que o argumento `pk` é passado para o método `get_queryset` através do atributo `kwargs`. O atributo `kwargs` é um dicionário que contém os argumentos passados para a view. O argumento `pk` é passado para a view através da URL.

```python

from rest_framework.generics import ListAPIView
from escola.models import Matricula
from escola.serializer import ListarMatriculasAlunoSerializer

class ListarMatriculasAluno(ListAPIView):
    "Listando as matrículas de um aluno específico"
    serializer_class = ListarMatriculasAlunoSerializer

    def get_queryset(self):
        aluno_id = self.kwargs['pk']
        return Matricula.objects.filter(aluno_id=aluno_id)

```

Uma vez criado a classe que utiliza a `ListAPIView`, é necessário criar a URL que mapeia a view. O conteúdo da URL é mostrado abaixo. A URL mapeia a view `ListarMatriculasAluno` para a URL `alunos/<int:pk>/matriculas/`. O argumento `pk` é passado para a view através da URL.

```python
from django.contrib import admin
from django.urls import path
from escola.views import AlunoModelViewSet, CursoModelViewSet, MatriculaModelViewSet, ListaMatriculasAluno
from escola.models import Aluno, Curso, Matricula
from rest_framework import routers
from django.urls import include

router = routers.DefaultRouter()
router.register(r'alunos', AlunoModelViewSet, basename='Alunos')
router.register(r'cursos', CursoModelViewSet, basename='Cursos')
router.register(r'matriculas', MatriculaModelViewSet, basename='Matriculas')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('escola/', include(router.urls)),    
    path('aluno/<int:pk>/matriculas/', ListaMatriculasAluno.as_view()), 

]
```

Agora se quisermos saber informação dos alunos matriculados em um curso específico, podemos criar uma nova view chamada `ListaAlunosMatriculadosCurso` que é uma subclasse de `ListAPIView`. O conteúdo da classe é mostrado abaixo. A classe `ListaAlunosMatriculadosCurso` é uma subclasse de `ListAPIView` e possui um método `get_queryset` que retorna todos os alunos matriculados em um curso específico. O método `get_queryset` recebe o id do curso e retorna todos os alunos matriculados no curso. O método `get_queryset` é chamado pelo método `get` que retorna uma resposta de lista de objetos. Perceba que o argumento `pk` é passado para o método `get_queryset` através do atributo `kwargs`. O atributo `kwargs` é um dicionário que contém os argumentos passados para a view. O argumento `pk` é passado para a view através da URL.

```python

from rest_framework.generics import ListAPIView
from escola.models import Matricula
from escola.serializer import ListarMatriculasAlunoSerializer

class ListaAlunosMatriculadosCurso(ListAPIView):
    "Listando os alunos matriculados em um curso específico"
    serializer_class = ListarMatriculasAlunoSerializer

    def get_queryset(self):
        curso_id = self.kwargs['pk']
        return Matricula.objects.filter(curso_id=curso_id)

```

É necessário também criar o serializer `ListarAlunosMatriculadosCursoSerializer` que é uma subclasse de `serializers.ModelSerializer` e possui um método `get_nome` que retorna o nome do aluno. A subclasse `Meta` é usada para definir o modelo e os campos que serão serializados. Para isso é o modelo da classe `Meta` é o modelo `Matricula` e os campos são `aluno` e `nome`. O campo `aluno` é um campo somente leitura e o campo `nome` é um campo que chama o método `get_nome`. O método `get_nome` retorna o nome do aluno.  

```python

class ListarMatriculasAlunoSerializer(serializers.ModelSerializer):
    curso = serializers.ReadOnlyField(source='curso.descricao')
    periodo = serializers.SerializerMethodField()

    class Meta:
        model = Matricula
        fields = ['curso', 'periodo']

    def get_periodo(self, obj):
        return obj.get_periodo_display()
```


Uma vez criado a classe que utiliza a `ListAPIView`, é necessário criar a URL que mapeia a view. O conteúdo da URL é mostrado abaixo. A URL mapeia a view `ListaAlunosMatriculadosCurso` para a URL `cursos/<int:pk>/matriculas/`. O argumento `pk` é passado para a view através da URL.

```python

from django.contrib import admin
from django.urls import path
from escola.views import AlunoModelViewSet, CursoModelViewSet, MatriculaModelViewSet, ListaMatriculasAluno, ListaAlunosMatriculadosCurso

from rest_framework import routers
from django.urls import include

...


urlpatterns = [
    path('admin/', admin.site.urls),
    path('escola/', include(router.urls)),    
    path('aluno/<int:pk>/matriculas/', ListaMatriculasAluno.as_view()), 
    path('curso/<int:pk>/matriculas/', ListaAlunosMatriculadosCurso.as_view()),

]
```



## Conclusão

A classe `ListAPIView` é uma classe genérica de API de visualização que fornece uma funcionalidade de listagem básica para um modelo. Esta classe fornece um método `get` que retorna uma resposta de lista de objetos. A classe `ListAPIView` pode ser usada para listar todas as matrículas de um aluno ou para listar todos os alunos matriculados em um curso específico.

## Referências

[Documentação Oficial do Django Rest Framework](https://www.django-rest-framework.org/)

[Documentação Oficial do Django](https://www.djangoproject.com/)

[Python Brasil](https://python.org.br/)