from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.services.usuario_service import create_usuario, get_usuarios
from typing import List

router = APIRouter()

@router.get('/', response_model=List[UsuarioResponse])
def get_passageiros(db: Session = Depends(get_db)):
    return get_usuarios(db=db)

@router.post('/', status_code=201, response_model=UsuarioResponse)
def create_passageiro(passageiro: UsuarioCreate, db: Session = Depends(get_db)):
    return create_usuario(db=db, usuario=passageiro)