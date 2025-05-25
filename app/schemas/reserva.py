from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReservaBase(BaseModel):
    viagem_id: int
    passageiro_id: int
    quantidade_vagas: int
    local_partida: str
    observacao: Optional[str] = None

class ReservaRequest(ReservaBase):
    pass

class ReservaResponse(ReservaBase):
    id: int
    status: str  # Ex: "pendente", "confirmada", "cancelada"

    class Config:
        from_attributes = True