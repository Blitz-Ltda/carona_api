from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AvaliacaoBase(BaseModel):
    viagem_id: int
    passageiro_id: int
    motorista_id: int
    nota: float = Field(..., ge=1, le=5)
    comentario: Optional[str] = None

class AvaliacaoRequest(AvaliacaoBase):
    pass

class AvaliacaoResponse(AvaliacaoBase):
    id: int
    criado_em: datetime

    class Config:
        from_attributes = True