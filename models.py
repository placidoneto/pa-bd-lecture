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


