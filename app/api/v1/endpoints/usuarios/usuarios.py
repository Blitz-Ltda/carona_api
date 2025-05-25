from app.shared.dependencies import get_db
from app.schemas.usuario import UsuarioRequest, UsuarioResponse, PerfilCompletoResponse
from app.services.usuario_service import *
from app.shared.exception import NotFoundError
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.get('/', response_model=List[UsuarioResponse])
def get_usuarios_view(db: Session = Depends(get_db)):
    return get_usuarios(db=db)

@router.get('/{usuario_id}/perfil_completo', response_model=PerfilCompletoResponse)
def get_perfil_completo_view(usuario_id: int, db: Session = Depends(get_db)):
    perfil_completo = get_perfil_completo(usuario_id=usuario_id, db=db)

    if not perfil_completo:
        raise NotFoundError("Perfil completo do usuário")

    return perfil_completo

@router.post('/', status_code=201, response_model=UsuarioResponse)
def create_usuario_view(usuario: UsuarioRequest, db: Session = Depends(get_db)):
    return create_usuario(db=db, usuario=usuario)

@router.put('/{usuario_id}', status_code=200 ,response_model=UsuarioResponse)
def update_usuario_view(usuario_id: int, usuario: UsuarioRequest, db: Session = Depends(get_db)):
    usuario_db = _get_usuario_by_id(usuario_id=usuario_id, db=db)

    return update_usuario(usuario_db=usuario_db, db=db, usuario=usuario)

@router.delete('/{usuario_id}', status_code=204)
def delete_usuario_view(usuario_id: int, db: Session = Depends(get_db)):
    usuario_db = _get_usuario_by_id(usuario_id=usuario_id, db=db)

    return delete_usuario(usuario_db=usuario_db, db=db)

def _get_usuario_by_id(usuario_id: int, db: Session = Depends(get_db)):
    usuario = get_usuario(usuario_id=usuario_id, db=db)
    if not usuario:
        raise NotFoundError("Usuario")
    
    return usuario