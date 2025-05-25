from app.shared.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.types import Enum as SQLEnum
from sqlalchemy.orm import relationship

viagem_status_enum = SQLEnum(
    "pendente", "confirmada", "cancelada", "finalizada", "em_andamento",
    name="viagemstatus"
)

class Viagem(Base):
    __tablename__ = "viagens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vagas = Column(Integer, nullable=False)
    valor = Column(Float, nullable=False)
    trajeto = Column(String, nullable=False)  
    data_hora = Column(DateTime, nullable=False)
    tipo_reserva = Column(String, nullable=False) # Ex: "imediata", "agendada"
    observacao = Column(String, nullable=True)
    status = Column(viagem_status_enum, nullable=False, default="pendente")
    motorista_id = Column(Integer, ForeignKey("usuarios.id"))
    veiculo_id = Column(Integer, ForeignKey("veiculos.id"))

    motorista = relationship("Usuario", back_populates="viagens")
    veiculo = relationship("Veiculo", back_populates="viagens")
    reservas = relationship("Reserva", back_populates="viagem")
