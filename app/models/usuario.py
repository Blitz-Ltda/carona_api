from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    contato_emergencia = Column(String, nullable=False)
    descricao = Column(String, nullable=True)