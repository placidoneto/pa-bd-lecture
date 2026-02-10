# 📋 Trabalho Prático — Prova Final

## Programação e Administração de Banco de Dados

**Professor:** Plácido A. Souza Neto  
**Instituição:** IFRN — Instituto Federal de Educação, Ciência e Tecnologia do Rio Grande do Norte  
**Prazo de Entrega:** Quarta-feira, 11/02/2025, até 12h00 (meio-dia)

---

## 1. Objetivo

Desenvolver uma **API RESTful** utilizando **Django REST Framework** com banco de dados **PostgreSQL** que implemente uma **Agenda de Contatos** completa, com operações CRUD, organização por grupos e filtros avançados.

Este trabalho tem como finalidade avaliar a capacidade do aluno de:

- Modelar um banco de dados relacional adequado ao problema proposto.
- Implementar uma API REST funcional seguindo boas práticas.
- Configurar corretamente o Django REST Framework com PostgreSQL.
- Criar endpoints com filtros e consultas elaboradas ao banco de dados.
- Documentar e apresentar o projeto de forma clara.

---

## 2. Descrição do Projeto

A API deve funcionar como uma **agenda digital de contatos**, permitindo ao usuário gerenciar seus contatos pessoais organizados em grupos. O sistema deve oferecer recursos de busca e filtragem que facilitem a consulta das informações armazenadas.

---

## 3. Requisitos Funcionais

### 3.1 CRUD de Contatos

A API deve implementar as quatro operações básicas sobre contatos:

| Operação  | Método HTTP | Descrição                              |
|-----------|-------------|----------------------------------------|
| Criar     | `POST`      | Cadastrar um novo contato              |
| Listar    | `GET`       | Listar todos os contatos               |
| Detalhar  | `GET`       | Exibir os dados de um contato específico |
| Atualizar | `PUT/PATCH` | Atualizar dados de um contato existente |
| Remover   | `DELETE`    | Excluir um contato                     |

### 3.2 Dados do Contato

Cada contato deve conter, **no mínimo**, as seguintes informações:

- **Nome completo**
- **E-mail**
- **Data de nascimento (aniversário)**
- **Grupo** ao qual pertence
- **Telefone(s)** — cada contato pode possuir **mais de um número de telefone** (ex: celular pessoal, celular do trabalho, telefone fixo, etc.)

### 3.3 Grupos de Contatos

Os contatos devem estar organizados nos seguintes grupos:

| Grupo       | Descrição                        |
|-------------|----------------------------------|
| `escola`    | Contatos do ambiente escolar     |
| `familia`   | Contatos de familiares           |
| `trabalho`  | Contatos do ambiente profissional |

> **Observação:** O grupo pode ser implementado como um modelo separado (recomendado) ou como um campo de escolha (`choices`) no modelo de contato. A decisão de modelagem deve ser justificada no README.

### 3.4 Filtros e Consultas Avançadas

A API **deve obrigatoriamente** disponibilizar os seguintes endpoints/filtros:

| # | Filtro / Consulta | Descrição |
|---|-------------------|-----------|
| 1 | **Contatos por grupo** | Listar todos os contatos de um determinado grupo (ex: todos os contatos do grupo `familia`). |
| 2 | **Aniversariantes do mês** | Listar todos os contatos que fazem aniversário em um determinado mês. |
| 3 | **Aniversariantes do mês por grupo** | Listar os contatos que fazem aniversário em um determinado mês, filtrados por grupo. |
| 4 | **Grupo com mais contatos** | Retornar qual grupo possui o maior número de contatos cadastrados. |
| 5 | **Grupo com menos contatos** | Retornar qual grupo possui o menor número de contatos cadastrados. |
| 6 | **Contagem de contatos por grupo** | Retornar a quantidade de contatos em cada grupo. |

> **Dica:** Utilize os recursos do Django REST Framework como `filters`, `query_params`, `actions customizadas` ou endpoints dedicados para implementar essas consultas.

---

## 4. Requisitos Técnicos

### 4.1 Stack Tecnológica Obrigatória

| Tecnologia | Utilização |
|---|---|
| **Python 3.10+** | Linguagem de programação |
| **Django 4+** | Framework web |
| **Django REST Framework** | Construção da API REST |
| **PostgreSQL** | Banco de dados relacional |
| **drf-yasg** ou **drf-spectacular** | Documentação automática com Swagger/OpenAPI |

### 4.2 Estrutura Esperada do Projeto

```
agenda-contatos/
├── manage.py
├── requirements.txt
├── README.md
├── core/                    # Projeto Django principal
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── contatos/                # App dos contatos
│   ├── models.py            # Modelos: Contato, Telefone, Grupo
│   ├── serializers.py       # Serializers da API
│   ├── views.py             # Views/ViewSets
│   ├── urls.py              # Rotas da API
│   ├── admin.py             # Configuração do Django Admin
│   ├── filters.py           # Filtros (opcional, mas recomendado)
│   └── ...
└── ...
```

### 4.3 Modelagem Sugerida

Abaixo está uma sugestão de modelagem. O aluno tem **liberdade para adaptar** conforme julgar mais adequado, desde que os requisitos funcionais sejam atendidos.

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    Grupo     │       │   Contato    │       │   Telefone   │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id           │◄──┐   │ id           │◄──┐   │ id           │
│ nome         │   └───│ grupo (FK)   │   └───│ contato (FK) │
│ descricao    │       │ nome         │       │ numero       │
│ created_at   │       │ email        │       │ tipo         │
└──────────────┘       │ data_nasc    │       │ created_at   │
                       │ created_at   │       └──────────────┘
                       │ updated_at   │
                       └──────────────┘
```

**Relacionamentos:**
- **Grupo → Contato:** Um grupo possui vários contatos (1:N).
- **Contato → Telefone:** Um contato possui vários telefones (1:N).

---

## 5. Entregáveis

O aluno deve entregar os seguintes itens:

### 5.1 Código-fonte no GitHub

Aceite o assignment e faça o push do código no repositório gerado:

🔗 **Link do Assignment:** [https://classroom.github.com/a/KjRFYhMc](https://classroom.github.com/a/KjRFYhMc)

O repositório deve conter:

- [ ] **Modelos** (`models.py`) — com todos os modelos necessários.
- [ ] **Serializers** (`serializers.py`) — com serializers para cada modelo, incluindo serializers aninhados quando necessário (ex: telefones dentro do contato).
- [ ] **Views** (`views.py`) — ViewSets ou APIViews com todas as operações CRUD e filtros.
- [ ] **Rotas** (`urls.py`) — configuração das rotas da API (preferencialmente com `DefaultRouter`).
- [ ] **Admin** (`admin.py`) — configuração do Django Admin para gerenciar os dados pelo painel administrativo.
- [ ] **Swagger** — documentação da API acessível via navegador (ex: `/swagger/` ou `/docs/`).
- [ ] **README.md** — documentação completa do projeto (veja seção 5.2).
- [ ] **requirements.txt** — lista de dependências do projeto.

### 5.2 Documentação (README.md)

O `README.md` do repositório deve conter, **no mínimo**:

1. **Título e descrição** do projeto.
2. **Explicação dos modelos** utilizados e a justificativa das decisões de modelagem (ex: por que criou um modelo separado para Grupo, por que o Telefone é um modelo à parte, etc.).
3. **Diagrama ou descrição dos relacionamentos** entre os modelos.
4. **Lista dos endpoints** da API com exemplos de uso.
5. **Instruções de como executar o projeto** localmente (instalação, configuração do banco, migrations, etc.).
6. **Informações sobre a documentação Swagger** (como acessar).

### 5.3 Vídeo Explicativo

- **Duração:** entre **5 e 10 minutos**.
- **Conteúdo:** O aluno deve apresentar e explicar o que foi desenvolvido, demonstrando a API funcionando (via Swagger, Postman, ou navegador da API do DRF).
- **Entrega:** O vídeo deve ser enviado por meio de um **link** (YouTube, Google Drive, Loom, etc.). O link pode ser incluído no README.md ou enviado separadamente.

---

## 6. Critérios de Avaliação

| Critério | Peso | Descrição |
|---|---|---|
| **Modelagem do Banco** | 10% | Modelos bem estruturados, relacionamentos corretos, uso adequado de tipos de campo. |
| **CRUD Completo** | 20% | Todas as operações (Create, Read, Update, Delete) funcionando corretamente. |
| **Filtros e Consultas** | 20% | Implementação correta de todos os filtros exigidos (seção 3.4). |
| **Serializers e Views** | 15% | Uso adequado de serializers (incluindo aninhados) e organização das views. |
| **Swagger/Documentação da API** | 10% | Documentação interativa acessível e funcional. |
| **README e Documentação** | 10% | README completo, claro e bem organizado. |
| **Vídeo Explicativo** | 15% | Clareza na apresentação e demonstração da API funcionando. |

---

## 7. Exemplos de Endpoints Esperados

A tabela abaixo serve como **referência**. O aluno pode organizar as rotas conforme preferir, desde que todas as funcionalidades estejam disponíveis.

```
# CRUD de Contatos
GET    /api/contatos/                    → Lista todos os contatos
POST   /api/contatos/                    → Cria um novo contato
GET    /api/contatos/{id}/               → Detalha um contato
PUT    /api/contatos/{id}/               → Atualiza um contato (completo)
PATCH  /api/contatos/{id}/               → Atualiza um contato (parcial)
DELETE /api/contatos/{id}/               → Remove um contato

# CRUD de Grupos
GET    /api/grupos/                      → Lista todos os grupos
POST   /api/grupos/                      → Cria um novo grupo
GET    /api/grupos/{id}/                 → Detalha um grupo
PUT    /api/grupos/{id}/                 → Atualiza um grupo
DELETE /api/grupos/{id}/                 → Remove um grupo

# Filtros e Consultas
GET    /api/contatos/?grupo=familia      → Contatos de um grupo específico
GET    /api/contatos/?mes_aniversario=3  → Aniversariantes de março
GET    /api/contatos/?grupo=escola&mes_aniversario=6
                                         → Aniversariantes de junho do grupo escola
GET    /api/grupos/contagem/             → Contagem de contatos por grupo
GET    /api/grupos/mais-contatos/        → Grupo com mais contatos
GET    /api/grupos/menos-contatos/       → Grupo com menos contatos

# Documentação
GET    /swagger/                         → Documentação Swagger UI
GET    /redoc/                           → Documentação ReDoc (opcional)
```

---

## 8. Dicas e Orientações

- **Comece pela modelagem:** Antes de escrever código, planeje seus modelos e relacionamentos no papel ou em uma ferramenta de diagramação.
- **Use `django-filter`:** A biblioteca `django-filter` facilita bastante a implementação de filtros nos ViewSets.
- **Serializers aninhados:** Para retornar os telefones dentro do contato, utilize serializers aninhados (nested serializers) com suporte a escrita (writable nested serializers).
- **Teste seus endpoints:** Utilize o Swagger, o Postman, ou a interface navegável do DRF para testar cada endpoint antes de entregar.
- **Popule o banco:** Crie dados de teste suficientes para demonstrar todos os filtros funcionando (contatos em diferentes grupos, com diferentes meses de aniversário, etc.).
- **Commits frequentes:** Faça commits regulares com mensagens descritivas. Isso demonstra a evolução do trabalho.
- **Não deixe para a última hora:** O prazo é curto. Organize-se.

---

## 9. Informações de Entrega

| Item | Detalhes |
|---|---|
| **Repositório** | [https://classroom.github.com/a/KjRFYhMc](https://classroom.github.com/a/KjRFYhMc) |
| **Prazo** | **Quarta-feira, 11/02/2025 às 12h00 (meio-dia)** |
| **Vídeo** | Enviar via link (YouTube, Google Drive, Loom, etc.) |
| **Formato** | Push no repositório do GitHub Classroom |

> ⚠️ **Atenção:** Trabalhos entregues após o prazo **não serão aceitos**. Certifique-se de que o repositório contém todo o código e que o push foi realizado antes do horário limite.

---

**Bom trabalho! 🚀**