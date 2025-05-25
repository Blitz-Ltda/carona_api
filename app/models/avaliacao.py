from app.shared.base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

class Avaliacao(Base):
    __tablename__ = 'avaliacoes'

    id = Column(Integer, primary_key=True, index=True)
    viagem_id = Column(Integer, ForeignKey('viagens.id'), nullable=False)
    passageiro_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    motorista_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    nota = Column(Float, nullable=False)
    comentario = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.now(pytz.timezone('America/Maceio')), nullable=False)

    viagem = relationship('Viagem')
    passageiro = relationship('Usuario', foreign_keys=[passageiro_id])
    motorista = relationship('Usuario', foreign_keys=[motorista_id])