# Trabalho Prático: API REST de Cardápio com Autenticação JWT

**Professor:** Prof. Plácido Neto  
**Assignment:** https://classroom.github.com/a/JbLH7aUd
**Período:** 2025.2

## Objetivo

O objetivo desta atividade é desenvolver uma API REST completa para gerenciamento de cardápio de restaurante utilizando Django REST Framework com autenticação JWT (JSON Web Token). A aplicação deve implementar diferentes níveis de permissão para usuários (Clientes, Garçons e Gerentes) e garantir a segurança das operações através de tokens JWT.

## Contexto do Problema

Você foi contratado para desenvolver o backend de um sistema de pedidos para um restaurante. O restaurante precisa de uma solução digital que permita:

- **Clientes** possam visualizar o cardápio completo e fazer seus pedidos de forma autenticada
- **Garçons** possam atualizar o status dos pedidos (pendente, em preparo, pronto, entregue)
- **Gerentes** possam gerenciar o cardápio (adicionar, editar e remover itens)
- Cada cliente deve ter acesso apenas aos seus próprios pedidos
- Todas as operações devem ser protegidas por autenticação JWT

O sistema deve registrar todas as transações e permitir rastreamento completo dos pedidos, desde a criação até a entrega.

## Requisitos Funcionais

### 1. Gerenciamento de Usuários e Autenticação

- O sistema deve permitir o cadastro de usuários com informações como nome, email, telefone e tipo de usuário (Cliente, Garçom ou Gerente)
- O sistema deve implementar autenticação JWT com endpoints de login e refresh token
- O sistema deve validar as credenciais do usuário e retornar tokens de acesso e refresh
- O sistema deve permitir que usuários autenticados atualizem suas próprias informações
- Passwords devem ser armazenados de forma segura (hash)

### 2. Gerenciamento de Cardápio

- O sistema deve permitir o cadastro de categorias de items (Entrada, Prato Principal, Sobremesa, Bebida, etc.)
- O sistema deve permitir o cadastro de itens do cardápio com informações como nome, descrição, preço, categoria, disponibilidade e imagem (URL)
- **Apenas Gerentes** podem criar, editar ou excluir itens do cardápio
- **Todos os usuários autenticados** podem visualizar o cardápio completo
- O sistema deve permitir filtrar itens por categoria e disponibilidade

### 3. Gerenciamento de Pedidos

- O sistema deve permitir que **Clientes** criem pedidos selecionando itens do cardápio
- Cada pedido deve conter: cliente, data/hora, itens (com quantidade), valor total e status
- O status do pedido pode ser: PENDENTE, EM_PREPARO, PRONTO, ENTREGUE ou CANCELADO
- **Clientes** podem:
  - Criar novos pedidos
  - Visualizar apenas seus próprios pedidos
  - Cancelar pedidos com status PENDENTE
- **Garçons** podem:
  - Visualizar todos os pedidos
  - Atualizar o status de qualquer pedido
- **Gerentes** têm acesso total a todos os pedidos

### 4. Gerenciamento de Itens do Pedido

- Cada item do pedido deve registrar: item do cardápio, quantidade, preço unitário no momento do pedido e subtotal
- O sistema deve calcular automaticamente o valor total do pedido
- O sistema deve validar se os itens estão disponíveis antes de confirmar o pedido

## Requisitos Técnicos

### Modelo de Dados

Descrever o modelo de dados que atenda aos requisitos acima:

- Cada entidade do modelo deve ser descrita com seus respectivos atributos
- Cada entidade do modelo deve ser descrita com suas respectivas relações com outras entidades
- O modelo de dados deve incluir as seguintes entidades principais:
  - **Usuario** (estendendo AbstractUser do Django)
  - **Categoria**
  - **ItemCardapio**
  - **Pedido**
  - **ItemPedido**

### Implementação com Django ORM

- O modelo de dados deve ser implementado utilizando o Django ORM
- Os modelos devem ser implementados em um arquivo `models.py`
- Utilizar relacionamentos adequados (ForeignKey, ManyToManyField, etc.)
- Implementar métodos `__str__()` apropriados para cada modelo
- Adicionar validações necessárias nos modelos

### API REST com Django REST Framework

A API deve ser implementada utilizando o Django REST Framework com os seguintes componentes:

#### Autenticação JWT

- Implementar autenticação JWT usando `djangorestframework-simplejwt`
- Endpoints obrigatórios:
  - `POST /api/auth/registro/` - Registro de novos usuários
  - `POST /api/auth/login/` - Login (obter tokens)
  - `POST /api/auth/token/refresh/` - Renovar token de acesso
  - `GET /api/auth/usuario/` - Obter informações do usuário autenticado

#### Serializers

- Criar serializers apropriados para cada modelo em `serializers.py`
- Implementar validações customizadas nos serializers
- Usar serializers aninhados onde apropriado (ex: ItemPedido dentro de Pedido)
- Implementar diferentes serializers para leitura e escrita quando necessário

#### Views e ViewSets

- Implementar ViewSets para cada recurso em `views.py`
- Utilizar as classes apropriadas (ModelViewSet, ReadOnlyModelViewSet, etc.)
- Implementar actions customizadas quando necessário (ex: `@action` para cancelar pedido)
- Aplicar permissões específicas para cada operação

#### Permissões Customizadas

- Criar classes de permissão customizadas para controlar acesso baseado no tipo de usuário
- Implementar as seguintes permissões:
  - `IsGerente` - apenas gerentes podem acessar
  - `IsGarcomOrGerente` - garçons e gerentes podem acessar
  - `IsClienteOrGarcom` - cliente pode acessar apenas seus próprios recursos, garçons acessam tudo

#### URLs

- Definir todos os endpoints em `urls.py`
- Utilizar routers do DRF para registrar ViewSets
- Organizar URLs de forma clara e RESTful

#### Documentação com Swagger

- Integrar `drf-yasg` para documentação automática
- Todas as operações devem ser testáveis via interface Swagger
- Adicionar descrições claras para cada endpoint
- Documentar os schemas de request/response

## Estrutura do Projeto

```
restaurante-api/
├── manage.py
├── requirements.txt
├── README.md
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── api/
    ├── __init__.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    ├── admin.py
    └── migrations/
```

## Endpoints da API

### Autenticação

- `POST /api/auth/registro/` - Registrar novo usuário
- `POST /api/auth/login/` - Login (obter tokens JWT)
- `POST /api/auth/token/refresh/` - Renovar access token
- `GET /api/auth/usuario/` - Dados do usuário autenticado
- `PUT /api/auth/usuario/` - Atualizar dados do usuário autenticado

### Categorias

- `GET /api/categorias/` - Listar todas as categorias
- `POST /api/categorias/` - Criar nova categoria (Gerente apenas)
- `GET /api/categorias/{id}/` - Detalhar categoria
- `PUT /api/categorias/{id}/` - Atualizar categoria (Gerente apenas)
- `DELETE /api/categorias/{id}/` - Deletar categoria (Gerente apenas)

### Itens do Cardápio

- `GET /api/cardapio/` - Listar itens do cardápio (com filtros)
- `POST /api/cardapio/` - Criar item (Gerente apenas)
- `GET /api/cardapio/{id}/` - Detalhar item
- `PUT /api/cardapio/{id}/` - Atualizar item (Gerente apenas)
- `PATCH /api/cardapio/{id}/` - Atualizar parcialmente (Gerente apenas)
- `DELETE /api/cardapio/{id}/` - Deletar item (Gerente apenas)

### Pedidos

- `GET /api/pedidos/` - Listar pedidos (Cliente vê apenas os seus)
- `POST /api/pedidos/` - Criar novo pedido (Cliente)
- `GET /api/pedidos/{id}/` - Detalhar pedido
- `PATCH /api/pedidos/{id}/` - Atualizar status (Garçom/Gerente)
- `POST /api/pedidos/{id}/cancelar/` - Cancelar pedido (Cliente, apenas PENDENTE)

## Critérios de Avaliação

A atividade será avaliada considerando os seguintes critérios:

### 1. Modelagem de Dados 

- Modelo conceitual bem definido e documentado no README
- Relacionamentos corretos entre entidades
- Atributos adequados para cada entidade
- Uso correto de tipos de dados

### 2. Implementação dos Models

- Implementação correta usando Django ORM
- Relacionamentos adequados (ForeignKey, ManyToMany, etc.)
- Validações implementadas
- Métodos auxiliares quando necessário

### 3. Autenticação JWT 

- Implementação correta do JWT
- Endpoints de autenticação funcionais
- Proteção adequada dos endpoints
- Tratamento correto de tokens expirados

### 4. Serializers e Validações

- Serializers bem estruturados
- Validações customizadas implementadas
- Tratamento adequado de dados aninhados
- Serializers diferentes para leitura/escrita quando apropriado

### 5. Views

- ViewSets corretamente implementados
- Permissões customizadas funcionando
- Actions customizadas quando necessário
- Filtragens implementadas


## Entrega

### Formato de Entrega

- O projeto deve ser entregue via **GitHub Classroom**
- Link do GitHub Classroom: [[A ser disponibilizado]](https://classroom.github.com/a/JbLH7aUd)
- O projeto pode ser realizado em **dupla**
- **Ambos os integrantes devem fazer commits** no repositório (critério de avaliação)

### Conteúdo a ser Entregue

1. Código fonte completo do projeto
2. Arquivo `requirements.txt` com todas as dependências
3. README.md com:
   - Descrição do modelo de dados
   - Instruções de instalação e execução
   - Exemplos de uso da API
   - Credenciais de teste para cada tipo de usuário
4. Arquivo `db.sqlite3` com dados de exemplo (pelo menos 3 usuários de cada tipo, 10 itens no cardápio, alguns pedidos)


## Dicas de Implementação

### 1. Começando pelo Modelo de Dados

Inicie definindo bem seus modelos. Pense nas relações:
- Um Pedido pertence a um Usuario (Cliente)
- Um Pedido tem vários ItemPedido
- Um ItemPedido referencia um ItemCardapio

### 2. Implementando JWT

```python
# settings.py
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

### 3. Criando Permissões Customizadas

```python
# permissions.py
from rest_framework import permissions

class IsGerente(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.tipo_usuario == 'GERENTE'
```

### 4. Usando Actions Customizadas

```python
# views.py
from rest_framework.decorators import action

class PedidoViewSet(viewsets.ModelViewSet):
    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        # Implementar lógica de cancelamento
        pass
```

