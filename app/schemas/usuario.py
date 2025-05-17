from pydantic import BaseModel, EmailStr
from typing import Optional

class UsuarioRequest(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    genero: str
    telefone: str
    contato_emergencia: str
    descricao: Optional[str] = None

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr

    class Config:
        from_attributes = True
