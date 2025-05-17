from sqlalchemy.orm import Session
from app.models.usuario import Usuario
from app.shared.security import verificar_senha, criar_token_jwt

def autenticar_usuario(db: Session, email: str, senha: str):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
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