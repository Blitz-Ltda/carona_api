from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioRequest(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    genero: str
    telefone: str
    matricula: str
    nome_emergencia: str
    telefone_emergencia: str
    descricao: Optional[str] = None

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        from_attributes = True

class MotoristaRequest(UsuarioRequest):
    cnh: str
    categoria_cnh: str
    data_validade_cnh: str
