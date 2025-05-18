from app.shared.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Veiculo(Base):
    __tablename__ = "veiculos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    modelo = Column(String, nullable=False)
    marca = Column(String, nullable=False)
    ano = Column(Integer, nullable=False)
    cor = Column(String, nullable=False)
    placa = Column(String, unique=True, nullable=False)
    renavam = Column(String, unique=True, nullable=False)
    capacidade = Column(Integer, nullable=False)
    tipo = Column(String, nullable=False)
    motorista_id = Column(Integer, ForeignKey("usuarios.id"))

    motorista = relationship("Usuario", back_populates="veiculos")
    viagens = relationship("Viagem", back_populates="veiculo")