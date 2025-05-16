from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from app.core.security import verificar_senha, criar_hash_da_senha

def create_usuario(db: Session, usuario: UsuarioCreate) -> Usuario:
    novo_usuario = Usuario(**usuario.model_dump())
    novo_usuario.senha = criar_hash_da_senha(usuario.senha)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

def get_usuario(db: Session, usuario_id: int) -> Usuario:
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100) -> list[Usuario]:
    return db.query(Usuario).offset(skip).limit(limit).all()

def get_usuarios_por_tipo(db: Session, tipo: str):
    return db.query(Usuario).filter(Usuario.tipo == tipo).all()