from pydantic import BaseModel

class VeiculoBase(BaseModel):
    modelo: str
    marca: str
    ano: int
    cor: str
    placa: str
    renavam: str
    capacidade: int
    tipo: str
    motorista_id: int

class VeiculoRequest(VeiculoBase):
    pass

class VeiculoResponse(VeiculoBase):
    id: int

    class Config:
        from_attributes = True
