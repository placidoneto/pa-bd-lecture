# Funções em Classes ViewSet do Django Rest Framework
## Construindo *endpoints* de API com Django Rest Framework

Após a construção dos modelos utilizando o Django ORM, é necessário criar as *endpoints* de API para que os dados possam ser acessados e manipulados. Para isso, utilizaremos o Django Rest Framework, que é uma biblioteca que facilita a construção de APIs RESTful.

Essa biblioteca fornece uma série de classes que podem ser utilizadas para criar *endpoints* de API de forma rápida e eficiente. Uma dessas classes é a `ViewSet`, que é utilizada para agrupar as operações CRUD (Create, Read, Update, Delete) de um modelo em um único lugar.

No entanto nem sempre utilizamos apenas as operações de CRUD, muitas vezes precisamos de operações customizadas, como por exemplo, a criação de um método que retorna os objetos de um modelo que atendem a um determinado critério.

Neste aula, vamos aprender como criar *endpoints* de API utilizando `ViewSet` e como adicionar métodos customizados a esses *endpoints*.

### Criando um ViewSet

Para criar um `ViewSet`, basta criar uma classe que herda de `ViewSet` e definir os métodos que serão utilizados para realizar as operações CRUD. Por exemplo, para criar um `ViewSet` para o modelo `Servico` ou `Cliente` (considerando o exemplo visto na última aula), podemos fazer o seguinte:

```python
from rest_framework import viewsets
from .models import Servico
from .serializers import ServicoSerializer

class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer
```

Neste exemplo, criamos um `ViewSet` chamado `ServicoViewSet` que utiliza o modelo `Servico` e o serializador `ServicoSerializer`. Com isso, o `ViewSet` já possui as operações CRUD implementadas e podemos utilizá-lo para criar os *endpoints* de API.

### Adicionando métodos customizados

Além das operações CRUD, podemos adicionar métodos customizados a um `ViewSet` para realizar operações específicas. Por exemplo, podemos adicionar um método que retorna os serviços de um cliente específico:

```python
from rest_framework import viewsets
from .models import Servico
from .serializers import ServicoSerializer
from .models import Cliente
from .serializers import ClienteSerializer

from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.models import Count, Max, Min, Sum

class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer

    @action(detail=False, methods=['get'])
    def servicos_cliente(self, request):
        cliente_id = request.query_params.get('cliente_id')
        servicos = Servico.objects.filter(cliente_id=cliente_id)
        serializer = ServicoSerializer(servicos, many=True)
        return Response(serializer.data)
```

No exemplo acima, adicionamos um método chamado `servicos_cliente` que utiliza o parâmetro `cliente_id` para filtrar os serviços de um cliente específico. Para isso, utilizamos o método `filter` do Django ORM para realizar a consulta no banco de dados e o serializador `ServicoSerializer` para serializar os dados.

A instrução `@action` é utilizada para definir o método como um *endpoint* específico da API. O parâmetro `detail=False` indica que o método não é relacionado a um objeto específico, ou seja, não é uma operação CRUD. O parâmetro `methods=['get']` indica que o método apenas pode ser chamado com o método HTTP GET.

### Registrando o ViewSet

Para que o `ViewSet` seja utilizado como um *endpoint* de API, é necessário registrá-lo em um `Router`. O `Router` é responsável por mapear os *endpoints* de API para as URLs da aplicação. Por exemplo, para registrar o `ViewSet` `ServicoViewSet`, podemos fazer o seguinte:

```python
from rest_framework.routers import DefaultRouter
from .views import ServicoViewSet
from django.urls import path, include
from rest_framework import routers
from django.urls import path, include

router = DefaultRouter()
router.register(r'servicos', ServicoViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```
Nesse exemplo, estamos criando um `Router` chamado `router` e registrando o `ViewSet` `ServicoViewSet` com o nome de URL `servicos`. Em seguida , estamos incluindo as URLs do `Router` no `urlpatterns` da aplicação. Isso fará com que as URLs do `ViewSet` sejam acessíveis na aplicação. Por exemplo, a URL `http://localhost:8000/servicos/` será mapeada para o `ViewSet` `ServicoViewSet`. 

O método `servicos_cliente` pode ser acessado através da URL `http://localhost:8000/servicos/servicos_cliente/?cliente_id=1`. Neste exemplo, estamos passando o parâmetro `cliente_id=1` para o método `servicos_cliente`, que irá retornar os serviços do cliente com o ID 1.

Uma pergunta importante, Como considerar o parâmetro `cliente_id` como um parâmetro de consulta? A resposta é que o Django ORM permite que você passe parâmetros de consulta como argumentos do método `filter`. Por exemplo, em vez de fazer `Servico.objects.filter(cliente_id=1)`, você pode fazer `Servico.objects.filter(cliente_id=cliente_id)`, onde `cliente_id` é o parâmetro passado para o método `servicos_cliente`.

Com isso, você pode criar *endpoints* de API com métodos customizados para realizar operações específicas nos seus modelos. Isso permite que você crie APIs RESTful poderosas e flexíveis com o Django Rest Framework.

Imagine que precisamos ainda de um endpoint para verificar os servicos pendentes de um cliente, para isso podemos criar outro método no nosso `ViewSet`

```python
class ServicoViewSet(viewsets.ModelViewSet):
  queryset = Servico.objects.all()
  serializer_class = ServicoSerializer

  @action(detail=False, methods=['get'])
  def servicos_cliente(self, request):
    cliente_id = request.query_params.get('cliente_id')
    servicos = Servico.objects.filter(cliente_id=cliente_id)
    serializer = ServicoSerializer(servicos, many=True
    return Response(serializer.data)

  @action(detail=False, methods=['get'])
  def servicos_pendentes(self, request):
    cliente_id = request.query_params.get('cliente_id')
    servicos = Servico.objects.filter(cliente_id=cliente_id, status='Pendente')
    serializer = ServicoSerializer(servicos, many=True
    return Response(serializer.data)

```

Neste exemplo, adicionamos um método chamado `servicos_pendentes` que utiliza o parâmetro `cliente_id` para filtrar os serviços pendentes de um cliente específico. Para isso, utilizamos o método `filter` do Django ORM para realizar a consulta no banco de dados e o serializador `ServicoSerializer` para serializar os dados.

O método `servicos_pendentes` pode ser acessado através da URL `http://localhost:8000/servicos/servicos_pendentes/?cliente_id=1`. Neste exemplo, estamos passando o parâmetro `cliente_id=1` para o método `servicos_pendentes`, que irá retornar os serviços pendentes do cliente com o ID 1.

Imagine ainda se precisarmos de um endpoint para saber os servicos considerando qualquer status. Para isso podemos criar outro método no nosso `ViewSet` que possa passar o parametro `status` para o método `filter` do Django ORM.

Para isso podemos criar um método no nosso `ViewSet` que possa passar o parametro `status` para o método `filter` do Django ORM.

Veja o exemplo abaixo:

```python

@action(detail=False, methods=['get'])
    def servicos_por_cliente_status(self, request):
        cliente_id = request.query_params.get('cliente_id')
        status = request.query_params.get('status')
        servicos = Servico.objects.filter(cliente_id=cliente_id, status=status)
        serializer = ServicoSerializer(servicos, many=True)
        return Response(serializer.data)
```

Neste exemplo, adicionamos um método chamado `servicos_por_cliente_status` que utiliza os parâmetros `cliente_id` e `status` para filtrar os serviços de um cliente específico com um status específico. Para isso, utilizamos o método `filter` do Django ORM para realizar a consulta no banco de dados e o serializador `ServicoSerializer` para serializar os dados.  O método `servicos_por_cliente_status` pode ser acessado através da URL `http://localhost:8000/servicos/servicos_por_cliente_status/?cliente_id=1&status=Pendente`. Neste exemplo, estamos passando os parâmetros `cliente_id=1` e `status=Pendente` para o método `servicos_por_cliente_status`, que irá retornar os serviços pendentes do cliente com o ID 1. 