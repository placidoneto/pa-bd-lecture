# API REST FastAPI Python

## Alunos responsáveis

- Felipe Alves
- João Roberto
- Débora
- Walber
- Ester

## 📌 Conteúdos

- [O que é o FastAPI?](#-o-que-é-o-fastapi)
- [Comparativo: FastAPI vs Django Rest Framework](#-comparativo-fastapi-vs-django-rest-framework)
- [Dependências do FastAPI](#-dependências-do-fastapi)
- [Criando a primeira API](#-criando-a-sua-primeira-api)
- [Conectando nossa API ao PostgreSQL](#-baixando-dependências)
- [Atividade prática](#-atividade-prática)

---

## 🔍 O que é o **FastAPI**?

FastAPI é um framework web moderno e **rápido** para construir APIs com Python, utilizando o mínimo de bibliotecas externas. Seus principais benefícios incluem:

✅ **Alto desempenho** (comparável ao Node.js e Go)  
✅ **Código conciso e intuitivo**  
✅ **Validação automática de dados com Pydantic**  
✅ **Documentação interativa embutida (Swagger e Redoc)**  
✅ **Suporte nativo para requisições assíncronas**

### 🌎 Quem usa o FastAPI?

<div style="display: flex; gap: 20px;">
    <img src="images/image-1.png" alt="Empresa 1" width="150"/>
    <img src="images/image-8.png" alt="Empresa 2" width="150"/>
    <img src="images/image-9.png" alt="Empresa 3" width="150"/>
</div>

---

## ⚖ Comparativo: FastAPI vs Django Rest Framework
<!--
<div style="display: flex; align-items: center; gap: 20px;">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/fastapi/fastapi-original.svg" width="80px" />
    <strong>VS</strong>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/djangorest/djangorest-line.svg" width="90px" />
</div>
-->

| Característica                    | FastAPI | Django REST Framework |
| :-------------------------------- | :------ | :-------------------- |
| 🔥 **Performance**                | ✅      | ❌                    |
| 🌍 **Comunidade**                 | ❌      | ✅                    |
| 📄 **Documentação automática**    | ✅      | ❌                    |
| ⚡ **Suporte a processos assíncronos** | ✅  | ❌                    |
| 🛠 **ORM nativo**                 | ❌      | ✅                    |
| 🔐 **Sistema robusto de autenticação** | ❌  | ✅                    |

### 💡 Qual o melhor? Depende!

💨 **Precisa de uma API veloz e escalável?** → Escolha **FastAPI**! Ideal para microserviços assíncronos com validação automática.

🛠 **Já usa Django e precisa de algo robusto?** → Escolha **Django REST Framework**! Perfeito para sistemas integrados ao Django ORM.

---

## Criando e Ativando Ambiente Virtual
```sh
python -m venv venv
venv\Scripts\activate
```

## ⚙ Dependências do FastAPI

Para instalar o FastAPI, use:

```sh
pip install "fastapi[standard]"
```

---

## 🚀 Criando a sua primeira API

Crie um arquivo `main.py` com o seguinte código:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}
```

Execute com:
```sh
fastapi dev main.py
```

A saída será similar a essa:
```sh
   FastAPI   Starting development server 🚀
 
             Searching for package file structure from directories with 
             __init__.py files
             Importing from /home/joaoroberto/Desktop/first-api-fastapi
 
    module   🐍 main.py
 
      code   Importing the FastAPI app object from the module with the 
             following code:
 
             from main import app
 
       app   Using import string: main:app
 
    server   Server started at http://127.0.0.1:8000
    server   Documentation at http://127.0.0.1:8000/docs
 
       tip   Running in development mode, for production use: fastapi run
 
             Logs:
 
      INFO   Will watch for changes in these directories: 
             ['/home/joaoroberto/Desktop/first-api-fastapi']
      INFO   Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
      INFO   Started reloader process [26061] using WatchFiles
      INFO   Started server process [26064]
      INFO   Waiting for application startup.
      INFO   Application startup complete.
```

Acesse `http://127.0.0.1:8000` e veja sua API rodando! 🎉 <br>
A partir desse caminho, você verá o retorno do caminho raíz definido no seu arquivo `main.py` e no decorator `@app.get("/")`


## 💾 Baixando dependências
É necessário instalar o sqlalchemy através do pip install:
```sh
pip install sqlalchemy psycopg2-binary alembic
```
No FastAPI, vamos criar um exmeplo de lista de tarefas como modelos no nosso arquivo `models.py`, antes, precisamos configurar nosso arquivo de conexão com o banco de dados. Esse arquivo ficará separado em `database.py`:
```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:senha@localhost:5432/fast"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```
## Criando os modelos e migrando com Alembic
```python
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from database import Base
from sqlalchemy.orm import relationship


class ListaTarefas(Base):
    __tablename__ = "listas"
    id = Column(Integer, primary_key=True)
    descricao = Column(String(255))
    tarefas = relationship("Tarefa", back_populates="lista", cascade="all, delete-orphan")
class Tarefa(Base):
    __tablename__ = "tarefas"
    id = Column(Integer, primary_key=True)
    titulo = Column(String(255))
    prioridade = Column(String(225), default="média")
    finalizado = Column(Boolean, default=False)
    lista_id = Column(Integer, ForeignKey("listas.id", ondelete="CASCADE"), nullable=False)

    lista = relationship("ListaTarefas", back_populates="tarefas")
```

Para migrar com o Alembic, precisamos fazer algumas configurações para realizar as migrações da forma correta. Primeiro vamos fazer iniciar o alembic com o comando:
```sh
alembic init alembic
```
Isso cria a pasta alembic/. Agora, edite alembic/env.py e altere:
```python
from database import Base
from models import *

...
target_metadata = Base.metadata
...
```

O target_metada fica para ser substitúido no comentário "add your model's MetaData object here", você o troca pelo que está desconmentado.

E ainda precisamos substituir o caminho para o nooso banco no arquivo `alembic.ini`:
```python
sqlalchemy.url =  postgresql://postgres:senha@localhost:5432/fast
```

Agora estamos prontos para nossas migrações:
```sh
alembic revision --autogenerate -m "Criando tabelas"
alembic upgrade head
```

## Criando nosso primeiro endpoint

Em `main.py`, adicione as novas importações:

```python
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
````

Agora vamos criar um get para listas de tarefas:
```python
@app.get("/listas/", response_model=list[schemas.ListaTarefasResponse], tags=["Listas"])
def listar_listas_de_tarefas(db: Session = Depends(get_db)):
    return db.query(models.ListaTarefas).all()
```

E agora vamos criar o arquivo `schemas.py` e adicionar os schemas responsáveis pela serialização dos dados e resposta dos endpoints
```python
from pydantic import BaseModel
from typing import List, Optional


class TarefaBase(BaseModel):
    titulo: str
    prioridade: str
    finalizado: bool = False

class TarefaResponse(TarefaBase):
    id: int
    lista_id: Optional[int]

    class Config:
        from_attributes = True

class ListaTarefasBase(BaseModel):
    descricao: str

class ListaTarefasResponse(ListaTarefasBase):
    id: int
    tarefas: List[TarefaResponse] = []

    class Config:
        from_attributes = True
```

Ao executar o endpoint pelo swagger, ele apresenta uma lista vazia, pois não existe nenhuma lista de tarefas criada.
Vamos criar um endpoit POST para criação de uma nova lista de tarefas.
```python
@app.post("/listas/", response_model=schemas.ListaTarefasResponse, tags=["Listas"])
def criar_lista(lista: schemas.ListaTarefasBase, db: Session = Depends(get_db)):
    db_lista = models.ListaTarefas(descricao=lista.descricao)
    db.add(db_lista)
    db.commit()
    db.refresh(db_lista)
    return db_lista
```

Dessa forma, é possível criar uma nova lisra de tarefas conectado com o banco de dados e serializado pelos Schemas.

Faremos da mesma forma para as Tarefas.

```python
@app.get("/tarefas/", response_model=list[schemas.TarefaResponse], tags=["Tarefas"])
def listar_tarefas(db: Session = Depends(get_db)):
    return db.query(models.Tarefa).all()


@app.post("/listas/{lista_id}/tarefas/", response_model=schemas.TarefaResponse, tags=["Tarefas"])
def criar_tarefa(lista_id: int, tarefa: schemas.TarefaBase, db: Session = Depends(get_db)):
    lista = db.query(models.ListaTarefas).filter(models.ListaTarefas.id == lista_id).first()
    if not lista:
        raise HTTPException(status_code=404, detail="Lista não encontrada")

    db_tarefa = models.Tarefa(**tarefa.model_dump(), lista_id=lista_id)
    db.add(db_tarefa)
    db.commit()
    db.refresh(db_tarefa)
    return db_tarefa
```

Temos nossos endpoints de Lista de Tarefas Criadas com suas respectivas Tarefas. 

## 📝 Atividade Prática
Nesta atividade, você irá explorar um projeto FastAPI que implementa um sistema de **Gerenciador de Contatos**, utilizando SQLAlchemy para modelagem do banco de dados e Alembic para migrações.

### 🎯 Objetivo:
Compreender como as rotas e os modelos interagem com o banco de dados. Criar, listar, atualizar e excluir contatos e grupos de contatos.

### Modelos do Banco de Dados
### Modelo: **Contato**
| Modelo      | Campo      | Tipo de Dado | Restrições              |
|-------------|------------|--------------|-------------------------|
| Contato     | id         | Integer      | Chave Primária (PK)     |
|             | nome       | String (255) | Obrigatório             |
|             | telefone   | String (20)  | Obrigatório             |
|             | email      | String (255) | Opcional                |
|             | endereco   | String (255) | Opcional                |

### Modelo: **Grupo**
| Modelo      | Campo      | Tipo de Dado | Restrições              |
|-------------|------------|--------------|-------------------------|
| Grupo       | id         | Integer      | Chave Primária (PK)     |
|             | nome       | String (255) | Obrigatório             |
|             | descricao  | String (500) | Opcional                |
|             | contatos   | Relacionamento | Um grupo pode ter vários contatos (1:N) |

## Endpoints da API

### Contatos
| Método HTTP | Rota                    | Descrição                                    | Parâmetros de Entrada         | Resposta Esperada                        |
|-------------|-------------------------|----------------------------------------------|--------------------------------|------------------------------------------|
| POST        | /contatos/              | Criar um novo contato                        | nome, telefone, email, endereco | id, nome, telefone, email, endereco     |
| GET         | /contatos/              | Listar todos os contatos                     | Nenhum                         | Lista de contatos                       |
| GET         | /contatos/{contato_id}  | Obter um contato pelo ID                     | contato_id (Integer)           | id, nome, telefone, email, endereco     |
| PUT         | /contatos/{contato_id}  | Atualizar um contato                         | nome, telefone, email, endereco | id, nome, telefone, email, endereco     |
| DELETE      | /contatos/{contato_id}  | Deletar um contato pelo ID                   | contato_id (Integer)           | Mensagem de sucesso                     |

### Grupos
| Método HTTP | Rota                       | Descrição                                    | Parâmetros de Entrada | Resposta Esperada                        |
|-------------|----------------------------|----------------------------------------------|------------------------|------------------------------------------|
| POST        | /grupos/                   | Criar um novo grupo de contatos              | nome, descricao        | id, nome, descricao                      |
| GET         | /grupos/                   | Listar todos os grupos                       | Nenhum                 | Lista de grupos                          |
| GET         | /grupos/{grupo_id}         | Obter um grupo pelo ID                       | grupo_id (Integer)     | id, nome, descricao                      |
| PUT         | /grupos/{grupo_id}         | Atualizar um grupo                           | nome, descricao        | id, nome, descricao                      |
| DELETE      | /grupos/{grupo_id}         | Deletar um grupo pelo ID                     | grupo_id (Integer)     | Mensagem de sucesso                      |
| POST        | /grupos/{grupo_id}/contatos/ | Adicionar um contato a um grupo             | contato_id (Integer)   | Mensagem de sucesso                      |
| DELETE      | /grupos/{grupo_id}/contatos/{contato_id} | Remover um contato de um grupo         | contato_id (Integer)   | Mensagem de sucesso                      |

## Referências:
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [SQLAlchemy Docs](https://www.sqlalchemy.org/)
- [Alembic Docs](https://alembic.sqlalchemy.org/en/latest/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Pydantic Docs](https://docs.pydantic.dev/latest/)
