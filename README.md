# Atividade Prática de Fixação Relacionamentos usando DRF: 
**Sistema Kanban com Django REST Framework (DRF)**

Link Assignment (horário limite envio - 15:00): https://classroom.github.com/a/pQM4wCk_

## Objetivo
Criar uma API REST para um sistema de controle de tarefas estilo Kanban, praticando relacionamentos entre modelos usando Django REST Framework.

## Descrição do Sistema

Você vai construir uma API para gerenciar:
- **Projetos** 
- **Colunas**  - ex: "A Fazer", "Em Progresso", "Concluído"
- **Tarefas** 
- **Usuários** 
- **Comentários** 

## Estrutura dos Modelos e Relacionamentos

### 1. **Projeto** 
- nome
- descrição
- data de criação
- proprietário (ForeignKey → Usuario)
- membros (ManyToMany → Usuario)

### 2. **Comula** 
- título
- ordem (para ordenação)
- projeto (ForeignKey → Projeto)

### 3. **Tarefa** 
- título
- descrição
- coluna (ForeignKey → Coluna)
- responsável (ForeignKey → Usuario, nullable)
- criador (ForeignKey → Usuario)
- prioridade (choices: baixa, média, alta)
- data de criação
- data de conclusão
- tags (ManyToMany → Etiqueta)

### 4. **Etiqueta** 
- nome
- cor

### 5. **Comentario** 
- tarefa (ForeignKey → Tarefa)
- autor (ForeignKey → Usuario)
- texto
- data de criação

## Requisitos da Atividade

### **Parte 1: Modelagem (30 min)**
1. Crie os modelos com os relacionamentos descritos
2. Implemente os métodos `__str__()` apropriados


### **Parte 2: Serializers (45 min)**
Crie serializers que:

1. **ProjetoSerializer**
   - Mostre a lista de colunas aninhadas
   - Mostre os nomes dos membros
   - Inclua contagem de tarefas totais

2. **ColunaSerializer**
   - Mostre as tarefas da coluna aninhadas
   - Inclua o nome do projeto

3. **TarefaSerializer**
   - Mostre informações completas do responsável
   - Mostre tags como lista de nomes
   - Inclua contagem de comentários

4. **ComentarioSerializer**
   - Mostre todos os comentários aninhados

### **Parte 3: ViewSets e Rotas (30 min)**
1. Crie ViewSets para cada modelo
2. Configure as rotas usando Router
3. Implemente filtros básicos (ex: tarefas por prioridade, por coluna)


4. **Atribuir responsável**
```python
   @action(detail=True, methods=['post'])
   def atribuir(self, request, pk=None):
       # POST /api/tarefa/{id}/atribuir/
```

1. **Adicionar membro ao projeto**
```python
   @action(detail=True, methods=['post'])
   def add_membro(self, request, pk=None):
       # POST /api/projetos/{id}/adicionar/
       # Body: {"user_id": 5}
```

1. **Listar tarefas por usuário em um projeto**
```python
   @action(detail=True, methods=['get'])
   def minhas_tarefas(self, request, pk=None):
       # GET /api/projetos/{id}/minhas_tarefas/
```

## Entrega Esperada

1. Código dos models, serializers e views
2. Arquivo `urls.py` com as rotas configuradas
3. Exemplos de requisições (pode ser um arquivo README)

### Documentação Oficial
- [Django REST Framework - Serializer Relations](https://www.django-rest-framework.org/api-guide/relations/)
- [Django REST Framework - ViewSets](https://www.django-rest-framework.org/api-guide/viewsets/)
- [Django Models - Relationships](https://docs.djangoproject.com/en/stable/topics/db/models/#relationships)

### Estrutura de Pastas Sugerida
```
kanban_api/
├── manage.py
├── projeto_kanban/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── tarefas/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── admin.py
```

## Dicas

1. **Comece simples**: Implemente o CRUD básico antes de partir para as actions customizadas
2. **Teste no Admin**: Configure o Django Admin para visualizar os relacionamentos antes de criar os serializers
3. **Documente suas rotas**: Mantenha um arquivo com exemplos de requisições para cada endpoint
4. **Commits incrementais**: Faça commits a cada funcionalidade implementada

## Configuração Inicial (Lembrete)

```bash
# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install django djangorestframework django-filter

# Criar projeto
django-admin startproject projeto_kanban .
python manage.py startapp tarefas

# Adicionar ao INSTALLED_APPS
 'rest_framework',
 'django_filters',
 'tarefas',

# Criar migrations e migrar
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor
python manage.py runserver
```

## Exemplo de Dados para Teste

### Projeto
```json
{
  "nome": "Sistema de Vendas",
  "descricao": "Desenvolvimento do novo sistema de vendas online",
  "proprietario": 1
}
```

### Coluna
```json
{
  "titulo": "Em Progresso",
  "ordem": 2,
  "projeto": 1
}
```

### Tarefa
```json
{
  "titulo": "Implementar autenticação JWT",
  "descricao": "Adicionar sistema de autenticação usando JWT",
  "coluna": 2,
  "responsavel": 1,
  "criador": 1,
  "prioridade": "alta",
  "tags": [1, 2]
}
```

---
