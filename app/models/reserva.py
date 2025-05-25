from app.shared.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.orm import relationship

reserva_status_enum = SQLEnum(
    "pendente", "confirmada", "cancelada", "finalizada",
    name="reservastatus"
)

class Reserva(Base):
    __tablename__ = "reservas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    viagem_id = Column(Integer, ForeignKey("viagens.id"), nullable=False)
    passageiro_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    quantidade_vagas = Column(Integer, nullable=False, default=1)
    local_partida = Column(String, nullable=False)
    observacao = Column(String, nullable=True)
    status = Column(reserva_status_enum, nullable=False, default="pendente")

    viagem = relationship("Viagem", back_populates="reservas")
    passageiro = relationship("Usuario", back_populates="reservas")
    
