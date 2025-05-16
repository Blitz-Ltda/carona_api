from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.db.base import Base

class Viagem(Base):
    __tablename__ = "viagens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    vagas = Column(Integer, nullable=False)
    valor = Column(Float, nullable=False)
    trajeto = Column(String, nullable=False)  
    data_hora = Column(String, nullable=False)
    tipo_reserva = Column(String, nullable=False)
    observacao = Column(String, nullable=True)
    status = Column(String, nullable=False)  # Ex: "ativa", "cancelada", "finalizada"
    motorista_id = Column(Integer, ForeignKey("usuarios.id"))
    veiculo_id = Column(Integer, ForeignKey("veiculos.id"))
