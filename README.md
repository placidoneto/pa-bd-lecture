# Atividade Fixação Autenticação

## Objetivo
Desenvolver uma API REST  usando Django REST Framework para gerenciar usuários, projetos e tarefas, incluindo um cliente CLI em Python para consumir os endpoints.

## Descrição do Sistema

O sistema deve permitir que usuários gerenciem seus projetos e tarefas através de uma API REST. Cada usuário pode criar múltiplos projetos, e cada projeto pode conter várias tarefas.

### Hierarquia de Dados
```
Usuario
  └── Projeto (1:N)
       └── Tarefa (1:N)
```

## Requisitos

### 1. Modelos Django

#### Modelo Usuario
- Utilizar o modelo de usuário padrão do Django (`AbstractUser` ou `User`)
- Campos personalizados (opcional):
  - `bio`: TextField
  - `data_cadastro`: DateTimeField (auto_now_add)

#### Modelo Projeto
- `nome`: CharField (max_length=200)
- `descricao`: TextField
- `usuario`: ForeignKey para Usuario
- `data_criacao`: DateTimeField (auto_now_add)
- `data_atualizacao`: DateTimeField (auto_now)
- `status`: CharField com choices (Planejamento, Em Andamento, Concluído)

#### Modelo Tarefa
- `titulo`: CharField (max_length=200)
- `descricao`: TextField
- `projeto`: ForeignKey para Projeto
- `concluida`: BooleanField (default=False)
- `prioridade`: CharField com choices (Baixa, Média, Alta)
- `data_criacao`: DateTimeField (auto_now_add)
- `data_conclusao`: DateTimeField (null=True, blank=True)

### 2. API REST

#### Autenticação
- Implementar autenticação via Token (TokenAuthentication)
- Endpoint de registro: `POST /api/auth/registro/`
- Endpoint de login: `POST /api/auth/login/`
- Endpoint de logout: `POST /api/auth/logout/`

#### Endpoints - Projetos
- `GET /api/projetos/` - Listar projetos do usuário autenticado
- `POST /api/projetos/` - Criar novo projeto
- `GET /api/projetos/{id}/` - Detalhes de um projeto
- `PUT /api/projetos/{id}/` - Atualizar projeto
- `DELETE /api/projetos/{id}/` - Deletar projeto

#### Endpoints - Tarefas
- `GET /api/projetos/{projeto_id}/tarefas/` - Listar tarefas de um projeto
- `POST /api/projetos/{projeto_id}/tarefas/` - Criar nova tarefa
- `GET /api/tarefas/{id}/` - Detalhes de uma tarefa
- `PUT /api/tarefas/{id}/` - Atualizar tarefa
- `PATCH /api/tarefas/{id}/concluir/` - Marcar tarefa como concluída
- `DELETE /api/tarefas/{id}/` - Deletar tarefa

#### Serializers
- `UsuarioSerializer`
- `ProjetoSerializer`
- `TarefaSerializer`

#### Permissions
- Usuários só podem ver/editar/deletar seus próprios projetos
- Usuários só podem ver/editar/deletar tarefas de seus projetos

### 3. Cliente CLI Python

Desenvolver um CLI em Python puro (sem Django) que consuma a API.

#### Funcionalidades do CLI

**Autenticação:**
```bash
python cli.py registrar --username usuario --password senha --email email@example.com
python cli.py login --username usuario --password senha
python cli.py logout
```

**Projetos:**
```bash
python cli.py projetos listar
python cli.py projetos criar --nome "Meu Projeto" --descricao "Descrição" --status "Em Andamento"
python cli.py projetos ver --id 1
python cli.py projetos atualizar --id 1 --nome "Novo Nome"
python cli.py projetos deletar --id 1
```

**Tarefas:**
```bash
python cli.py tarefas listar --projeto_id 1
python cli.py tarefas criar --projeto_id 1 --titulo "Tarefa" --descricao "Desc" --prioridade "Alta"
python cli.py tarefas ver --id 1
python cli.py tarefas atualizar --id 1 --titulo "Novo Título"
python cli.py tarefas concluir --id 1
python cli.py tarefas deletar --id 1
```

#### Requisitos Técnicos do CLI
- Usar biblioteca `requests` para chamadas HTTP
- Armazenar token em arquivo local (ex: `.token`)
- Formatação de saída com `tabulate` ou `rich`
- Tratamento de erros adequado

## Estrutura de Pastas Sugerida

```
projeto_api/
├── manage.py
├── projeto_api/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── api/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   └── tests.py
├── requirements.txt
└── cli/
    ├── cli.py
    ├── api_client.py
    └── requirements.txt
```

## Etapas de Desenvolvimento

### Fase 1: Setup Inicial
1. Criar projeto Django
2. Instalar Django REST Framework
3. Configurar settings (REST_FRAMEWORK, AUTHENTICATION)
4. Criar app `api`

### Fase 2: Modelos e Admin
1. Criar modelos Usuario, Projeto e Tarefa
2. Fazer migrations
3. Registrar modelos no admin
4. Criar superuser para testes

### Fase 3: Serializers e Views
1. Criar serializers para cada modelo
2. Implementar ViewSets ou APIViews
3. Configurar URLs
4. Implementar permissions personalizadas

### Fase 4: Autenticação
1. Configurar TokenAuthentication
2. Criar endpoints de registro e login
3. Testar autenticação com Postman/curl

### Fase 5: Cliente CLI
1. Criar estrutura do CLI
2. Implementar cliente HTTP (api_client.py)
3. Implementar comandos com argparse
4. Adicionar formatação e tratamento de erros

### Fase 6: Testes
1. Escrever testes unitários para a API
2. Testar todos os endpoints
3. Testar permissões
4. Testar CLI em diferentes cenários

## Dependências

**Backend:**
```txt
Django==4.2
djangorestframework==3.14
```

**CLI:**
```txt
requests==2.31
```

## Entregáveis

1. Código fonte do backend Django
2. Código fonte do CLI Python
3. Arquivo requirements.txt para ambos
4. README com instruções de setup e uso
5. Exemplos de uso da API e CLI
6. (Opcional) Collection do Postman para testar a API

## Recursos Adicionais

- Documentação Django REST Framework: https://www.django-rest-framework.org/
- Tutorial de TokenAuthentication: https://www.django-rest-framework.org/api-guide/authentication/
- Documentação argparse: https://docs.python.org/3/library/argparse.html
