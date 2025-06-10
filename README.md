# TP5 - Atividade Prática: API de Gerenciamento de Tarefas com Autenticação

**Objetivo:** Aplicar os conceitos do Django Rest Framework para construir uma API RESTful para um sistema de gerenciamento de tarefas, com foco na criação de endpoints CRUD e ações personalizadas (custom actions) em ViewSets em conjunto com autenticação.

Cada dupla deverá escolher um dos códigos do TP4 como base para o desenvolvimento da API para inclusão de autenticação. Antes de qualquer execução de criação de projeto ou tarefa, é necessário que o usuário esteja autenticado. A autenticação será feita utilizando o sistema de autenticação visto em sala de aula.

Cada dupla deverá implementar o front em Python, utilizando a biblioteca `requests` para interagir com a API desenvolvida. O front deve permitir que o usuário realize operações de CRUD e ações personalizadas, conforme especificado abaixo, mas para isso, a primeira operação a ser feita é a de autenticação do usuário. O usuário só poderá criar projetos e tarefas, bem como realizar as ações personalizadas, se estiver autenticado.


**Contexto do TP4 a ser considerado:**
Você foi encarregado de desenvolver o backend para um sistema simples de gerenciamento de tarefas. A API permitirá criar projetos, adicionar tarefas a esses projetos, atribuir tarefas a usuários e modificar o status das tarefas.

**Modelo de Dados (Django Models):**


- Usuario: Utilize o modelo `User` padrão do Django (`django.contrib.auth.models.User`).
- Projeto : Representa os projetos aos quais as tarefas pertencem.
  - nome (`CharField`)
  - descricao (`TextField`)
  - data_criacao (`DateTimeField, auto_now_add=True`)
  - proprietario (`ForeignKey para User, on_delete=models.CASCADE`)
- Tarefa: Representa as tarefas que podem ser atribuídas a usuários e associadas a projetos.
  - titulo (`CharField`)
  - descricao (`TextField, blank=True, null=True`)
  - status (`CharField, com escolhas: 'Pendente', 'Em Progresso', 'Concluída'`)
  - data_criacao (`DateTimeField, auto_now_add=True`)
  - data_conclusao (`DateTimeField, null=True, blank=True`)
  - projeto (`ForeignKey para Projeto, related_name='tarefas', on_delete=models.CASCADE`)
  - atribuido_a (`ForeignKey para User, null=True, blank=True, related_name='tarefas_atribuidas', on_delete=models.SET_NULL`)

## Configuração do Projeto e Criação dos Models (Django) 

- Crie um novo projeto Django e um app (ex: gestao_tarefas).
- Defina os modelos Projeto e Tarefa no arquivo `models.py` do seu app, conforme especificado acima.
- Adicione o `rest_framework` e seu app ao INSTALLED_APPS no `settings.py`.
- Crie e aplique as migrações (makemigrations e migrate).
- Crie alguns superusuários para testes.

## Criação dos Serializers (DRF) 

- Crie os serializers para seus modelos em um arquivo `serializers.py`:
  - `UserSerializer` 
  - `TarefaSerializer`
  - `ProjetoSerializer`

## Criação das Views e Endpoints (DRF ViewSets)

No arquivo `views.py`, crie ModelViewSets:

- `ProjetoViewSet`: Para gerenciar projetos. Fornecer operações CRUD padrão para Projetos.
  - Ação Personalizada 1: `tarefas_do_projeto`
    - Método: `GET`
    - Endpoint: `/projetos/{pk}/tarefas_do_projeto/`
    - Funcionalidade: Retornar uma lista de todas as tarefas associadas a um projeto específico.
  - Ação Personalizada 2: resumo_progresso
    - Método: `GET`
    - Endpoint: `/projetos/{pk}/resumo_progresso/`
    - Funcionalidade: Retornar um resumo do progresso do projeto, incluindo o número total de tarefas, tarefas pendentes, em progresso e concluídas. 
      - Ex: { `"total_tarefas": X, "concluidas": Y, "pendentes": Z `}
  - Ação Personalizada 3: `atribuir_proprietario`
    - Método: `POST`
    - Endpoint: `/projetos/{pk}/atribuir_proprietario/`
    - Funcionalidade: Atribuir um proprietário a um projeto, atualizando o campo `proprietario`.


- TarefaViewSet: Para gerenciar tarefas. Fornecer operações CRUD padrão para Tarefas.
  - Ação Personalizada 1: `marcar_concluida`
    - Método: `POST`
    - Endpoint: `/tarefas/{pk}/marcar_concluida/`
    - Funcionalidade: Marcar uma tarefa como concluída, atualizando o campo `data_conclusao` e o status da tarefa.
  - Ação Personalizada 2: `atribuir_usuario`
    - Método: `POST`
    - Endpoint: `/tarefas/{pk}/atribuir_usuario/`
    - Funcionalidade: Atribuir uma tarefa a um usuário específico, atualizando o campo `atribuido_a`.
  - Ação Personalizada 3: `remover_usuario`
    - Método: `POST`
    - Endpoint: `/tarefas/{pk}/remover_usuario/`
    - Funcionalidade: Remover a atribuição de um usuário de uma tarefa, definindo o campo `atribuido_a` como `null`.
  - Ação Personalizada 4: `mudar_status`
    - Método: `POST`
    - Endpoint: `/tarefas/{pk}/mudar_status/`
    - Funcionalidade: Mudar o status de uma tarefa, recebendo o novo status no corpo da requisição.
  - Ação Personalizada 5: `tarefas_por_usuario`
    - Método: `GET`
    - Endpoint: `/tarefas/tarefas_por_usuario/`
    - Funcionalidade: Retornar todas as tarefas atribuídas a um usuário específico, recebendo o ID do usuário como parâmetro de consulta.
  - Ação Personalizada 6: `numero_tarefas_por_projeto`
    - Método: `GET`
    - Endpoint: `/tarefas/numero_tarefas_por_projeto/`
    - Funcionalidade: Retornar o número total de tarefas por projeto, agrupando as tarefas pelo projeto, contando-as em ordem crescente.

## Configuração das URLs (DRF Routers)

No arquivo `urls.py` do seu app, configure as URLs usando DRF Routers:

- Crie um `DefaultRouter` e registre os ViewSets:
  - `router.register(r'projetos', ProjetoViewSet, basename='projeto')`
  - `router.register(r'tarefas', TarefaViewSet, basename='tarefa')`

- Configure o Swagger (opcional, mas recomendado):
  - Instale o `drf-yasg` e configure o Swagger no seu projeto para documentar a API.  

## Testes e Validação

- Crei um aplicativo cliente simples em Python para testar os endpoints da API.
- A execução da aplicação teste deve apresentar um menu/submenu simples cada tipo de modelo/operação, permitindo ao usuário interagir com a API.

- Usuários:
  - Listar usuários: `GET /usuarios/`
  - Detalhar usuário: `GET /usuarios/{pk}/`
  - Criar usuário: `POST /usuarios/`

- Projetos:
  - Listar projetos: `GET /projetos/`
  - Criar projeto: `POST /projetos/`
  - Detalhar projeto: `GET /projetos/{pk}/`
  - Atualizar projeto: `PUT /projetos/{pk}/`
  - Deletar projeto: `DELETE /projetos/{pk}/`
  - Ação personalizada: `GET /projetos/{pk}/tarefas_do_projeto/`
  - Ação personalizada : `GET /projetos/{pk}/resumo_progresso/`
  - Ação personalizada : `POST /projetos/{pk}/atribuir_proprietario/`

- Tarefas:
  - Listar tarefas: `GET /tarefas/`
  - Criar tarefa: `POST /tarefas/`
  - Detalhar tarefa: `GET /tarefas/{pk}/`
  - Atualizar tarefa: `PUT /tarefas/{pk}/`
  - Deletar tarefa: `DELETE /tarefas/{pk}/`
  - Ação personalizada: `POST /tarefas/{pk}/marcar_concluida/`
  - Ação personalizada : `POST /tarefas/{pk}/atribuir_usuario/`
  - Ação personalizada : `POST /tarefas/{pk}/remover_usuario/`
  - Ação personalizada : `POST /tarefas/{pk}/mudar_status/`
  - Ação personalizada : `GET /tarefas/tarefas_por_usuario/`
  - Ação personalizada : `GET /tarefas/numero_tarefas_por_projeto/`  

- **Autenticação** (novos endpoints incluidos para o TP5):
  - Login: `POST /api/token/login/` (utilizando o sistema de autenticação visto em sala de aula)
  - Logout: `POST /api/token/logout/`
  - Verificar se o usuário está autenticado: `GET /api/token/verify/` 
  
## Considerações Finais

- Certifique-se de que a API esteja bem documentada, utilizando o Swagger para facilitar o entendimento dos endpoints.
- Link Assigment: [GitHub Classroom](https://classroom.github.com/a/u7wD4XzY)
- Para aqueles que já implementaram o TP4 com autenticação e entregou em 04/06 está dispensado do TP5.
- Data de Entrega: **11/06/2025 às 16:30**