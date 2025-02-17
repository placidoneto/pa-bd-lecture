from http.client import HTTPException
from fastapi import FastAPI, Depends,HttpEx
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Criar Lista de Tarefas
# Obter todas as Listas de Tarefas
@app.get("/listas/", response_model=list[schemas.ListaTarefasResponse], tags=["Listas"])
def listar_listas_de_tarefas(db: Session = Depends(get_db)):
    return db.query(models.ListaTarefas).all()

@app.post("/listas/", response_model=schemas.ListaTarefasResponse, tags=["Listas"])
def criar_lista(lista: schemas.ListaTarefasBase, db: Session = Depends(get_db)):
    db_lista = models.ListaTarefas(descricao=lista.descricao)
    db.add(db_lista)
    db.commit()
    db.refresh(db_lista)
    return db_lista

# Obter todas as tarefas
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


