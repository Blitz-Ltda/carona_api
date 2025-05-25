from app.schemas.veiculo import VeiculoResponse
from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    genero: str
    telefone: str
    matricula: str
    nome_emergencia: str
    telefone_emergencia: str
    descricao: Optional[str] = None
    cnh: Optional[str] = None
    categoria_cnh: Optional[str] = None
    data_validade_cnh: Optional[str] = None

class UsuarioRequest(UsuarioBase):
    pass

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        from_attributes = True

class MotoristaResponse(UsuarioResponse):
    cnh: Optional[str] = None
    categoria_cnh: Optional[str] = None
    data_validade_cnh: Optional[str] = None
    veiculo: Optional[VeiculoResponse] = None
    nota_media: Optional[float] = None

    class Config:
        from_attributes = True

class PerfilCompletoResponse(BaseModel):
    usuario: UsuarioBase
    veiculo: VeiculoResponse | None = None
    nota_media: float | None = None

    class Config:
        from_attributes = True