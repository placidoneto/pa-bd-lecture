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
