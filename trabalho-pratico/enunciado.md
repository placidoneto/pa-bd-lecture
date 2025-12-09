# TP - Atividade prática: Gerenciamento de Álbuns - bemteouvi

## Objetivo
Aplicar os conceitos de desenvolvimento de APIs RESTful em Flask para construir um sistema de gerenciamento de álbuns musicais. A aplicação permite que músicos registrem seus álbuns, gerenciem suas informações, adicionem músicas aos álbuns e controlem a disponibilidade dos conteúdos no bemteouvi.

## Entidades de domínio

### Músico
- id (Long)
- nome_artistico (String)
- ativo (Boolean)

### Álbum
- id (Long)
- titulo (String)
- capa_do_album (String - caminho do arquivo)
- data_de_lancamento (Date)
- genero_musical (String)
- ativo (Boolean)
- data_criacao (DateTime – auto gerado)

### Música
- id (Long)
- album_id (Foreign Key)
- titulo (String)
- letra (Text)
- arquivo_audio (String - caminho do arquivo)
- genero (String)
- duracao (Integer - em segundos)
- ativo (Boolean)

### Estatística
- id (Long)
- musica_id (Foreign Key)
- play_count (Integer)
- curtidas_count (Integer)
- comentarios_count (Integer)
- data_ultima_atualizacao (DateTime – atualizado automaticamente)

## Regras de negócio

1. O músico deve existir e estar ativo para criar álbuns.
2. O álbum deve ter pelo menos um título e uma data de lançamento válida.
3. A data de lançamento não pode ser uma data futura.
4. Um álbum deve estar associado a um músico.
5. O gênero musical deve ser um dos gêneros válidos do sistema.
6. Um álbum pode ter múltiplas músicas, mas uma música pertence a um único álbum.
7. A capa do álbum é obrigatória.
8. Um álbum ativo não pode ter suas informações fundamentais alteradas (título, data de lançamento).
9. As estatísticas de uma música são inicializadas com zeros ao ser criada.
10. A data de criação do álbum é gerada automaticamente.
11. Não é permitido criar álbuns para músicos inativos.

## Configuração do Projeto

### 1. Criar e ativar um ambiente virtual

**Windows PowerShell:**
```powershell
# criar venv
python -m venv venv

# ativar
venv\Scripts\activate
```

**Linux/macOS (Bash):**
```bash
# criar venv
python3 -m venv venv

# ativar
source venv/bin/activate
```

### 2. Instalar dependências

**Windows PowerShell / Linux / macOS:**
```bash
pip install Flask
pip install flask_sqlalchemy
pip install psycopg2-binary
pip install Flask-Migrate
pip install flasgger
```

### 3. Configuração PostgreSQL

**Windows PowerShell:**
```powershell
$env:PGPASSWORD="postgres"; psql -U postgres -h localhost -c "CREATE DATABASE bemteouvi_album;"
```

**Linux/macOS (Bash):**
```bash
psql -U postgres -h localhost -c "CREATE DATABASE bemteouvi_album;"
```
(Será solicitada a senha do usuário postgres)

Configure o arquivo `config.py`:

```python
class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/bemteouvi_album"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 4. Estrutura de diretórios

```
bemteouvi_album/
│── app.py
│── config.py
│── models/
│   ├── musico_model.py
│   ├── album_model.py
│   ├── musica_model.py
│   └── estatistica_model.py
│── repositories/
│   ├── musico_repository.py
│   ├── album_repository.py
│   ├── musica_repository.py
│   └── estatistica_repository.py
│── services/
│   ├── musico_service.py
│   ├── album_service.py
│   ├── musica_service.py
│   └── estatistica_service.py
└── routes/
    ├── musico_routes.py
    ├── album_routes.py
    ├── musica_routes.py
    └── estatistica_routes.py
```

## Endpoints da API

### Músico

- `GET /musicos` - Retorna todos os músicos.
- `GET /musicos/{id}` - Retorna um músico específico.
- `POST /musicos` - Cria um novo músico.
- `GET /musicos/ativo` - Retorna músicos ativos no sistema.
- `PUT /musicos/{id}` - Atualiza dados de um músico.
- `DELETE /musicos/{id}` - Remove um músico.

### Álbum

- `GET /albums` - Retorna todos os álbuns.
- `GET /albums/{id}` - Retorna um álbum específico.
- `POST /albums` - Cria um novo álbum.
- `GET /albums/ativos` - Retorna apenas álbuns ativos.
- `GET /albums/genero/{genero}` - Busca álbuns por gênero musical.
- `GET /albums/musico/{musico_id}` - Busca álbuns de um músico específico.
- `PUT /albums/{id}` - Atualiza dados de um álbum.
- `DELETE /albums/{id}` - Remove um álbum.

### Música

- `GET /musicas` - Retorna todas as músicas.
- `GET /musicas/{id}` - Retorna uma música específica.
- `POST /musicas` - Cria uma nova música.
- `GET /musicas/album/{album_id}` - Busca músicas de um álbum.
- `GET /musicas/genero/{genero}` - Busca músicas por gênero.
- `PUT /musicas/{id}` - Atualiza dados de uma música.
- `DELETE /musicas/{id}` - Remove uma música.

### Estatística

- `GET /estatisticas` - Retorna todas as estatísticas.
- `GET /estatisticas/{id}` - Retorna estatística de uma música.
- `GET /estatisticas/musica/{musica_id}` - Busca estatísticas de uma música específica.
- `PUT /estatisticas/{id}/incrementar-play` - Incrementa contagem de plays.
- `PUT /estatisticas/{id}/incrementar-curtidas` - Incrementa contagem de curtidas.
- `PUT /estatisticas/{id}/incrementar-comentarios` - Incrementa contagem de comentários.

## Passo a Passo para Implementação

### Passo 1: Models (Entidades)

Crie as classes de domínio que representam as tabelas do banco de dados. Utilize SQLAlchemy para mapear as entidades.

### Passo 2: Repositories (Acesso ao banco)

Implemente as classes de repositório com métodos para SELECT, INSERT, UPDATE e DELETE para cada entidade.

### Passo 3: Services (Lógica de negócio)

Crie as classes de serviço que implementam as regras de negócio definidas, validando dados e coordenando operações entre repositórios.

### Passo 4: Routes (Endpoints)

Defina os endpoints REST que recebem requisições HTTP, chamam os serviços apropriados e retornam respostas em JSON.

### Passo 5: Arquivo principal (app.py)

Configure a aplicação Flask, registre os blueprints, inicialize o banco de dados e o Swagger.

### Passo 6: Criar as tabelas com migrações

**Windows PowerShell / Linux / macOS:**
```bash
flask db init
flask db migrate -m "Criando tabelas de álbum"
flask db upgrade
```

### Passo 7: Executar a aplicação

**Windows PowerShell / Linux / macOS:**
```bash
python app.py
```

A API estará disponível em: `http://127.0.0.1:5000`

E a documentação Swagger em: `http://127.0.0.1:5000/apidocs/`
