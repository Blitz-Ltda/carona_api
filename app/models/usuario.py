from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.shared.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    genero = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    matricula = Column(String, unique=True, nullable=False)
    status = Column(String, nullable=False, default="inativo")  # Ex: "ativo", "inativo"
    nome_emergencia = Column(String, nullable=True)
    telefone_emergencia = Column(String, nullable=True)
    descricao = Column(String, nullable=True)
    cnh = Column(String, nullable=True)
    categoria_cnh = Column(String, nullable=True)
    data_validade_cnh = Column(String, nullable=True)

    # Relacionamentos
    viagens = relationship("Viagem", back_populates="motorista")
    veiculos = relationship("Veiculo", back_populates="motorista")
    reservas = relationship("Reserva", back_populates="passageiro")
    avaliacoes = relationship("Avaliacao", foreign_keys="Avaliacao.passageiro_id", back_populates="passageiro")
    avaliacoes_motorista = relationship("Avaliacao", foreign_keys="Avaliacao.motorista_id", back_populates="motorista")
    