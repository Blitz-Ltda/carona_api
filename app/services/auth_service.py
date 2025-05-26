from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.shared.security import verificar_senha, criar_token_jwt
from app.repositories import UsuarioRepository

def autenticar_usuario(db: Session, email: str, senha: str) -> Usuario | None:
    usuario = UsuarioRepository(db).get_by_email(email)
    if not usuario or not verificar_senha(senha, usuario.senha):
        return None
    return usuario

def login(db: Session, email: str, senha: str):
    usuario = autenticar_usuario(db, email, senha)
    if not usuario:
        return None
    return criar_token_jwt({"sub": usuario.email, "id": usuario.id})

def logout():
    pass