from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ViagemBase(BaseModel):
    vagas: int
    valor: float
    trajeto: str
    data_hora: datetime
    tipo_reserva: str
    observacao: Optional[str] = None
    status: str  # Ex: "pendente", "confirmada", "cancelada", "finalizada"
    motorista_id: int
    veiculo_id: int

class ViagemRequest(ViagemBase):
    pass

class ViagemResponse(ViagemBase):
    id: int

    class Config:
        from_attributes = True
