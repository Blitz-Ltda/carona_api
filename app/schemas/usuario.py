from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioBase(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    genero: str
    telefone: str
    contato_emergencia: str
    descricao: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    pass

class UsuarioResponse(UsuarioBase):
    id: int
    nome: str
    email: EmailStr

    class Config:
        from_attributes = False
