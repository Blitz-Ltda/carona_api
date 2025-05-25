from sqlalchemy.orm import Session
from app.models import Usuario, Veiculo, Avaliacao
from app.schemas.usuario import UsuarioRequest
from app.shared.security import verificar_senha, criar_hash_da_senha

def create_usuario(db: Session, usuario: UsuarioRequest) -> Usuario:
    novo_usuario = Usuario(**usuario.model_dump())
    novo_usuario.senha = criar_hash_da_senha(usuario.senha)
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

def get_usuario(usuario_id: int, db: Session) -> Usuario:
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()

def get_usuarios(db: Session, skip: int = 0, limit: int = 100) -> list[Usuario]:
    return db.query(Usuario).offset(skip).limit(limit).all()

def get_perfil_completo(usuario_id: int, db: Session) -> dict:
    avaliacoes = db.query(Avaliacao).filter(Avaliacao.motorista_id == usuario_id).all()
    if not avaliacoes:
        nota_media = 0.0
    else:
        nota_media = sum(avaliacao.nota for avaliacao in avaliacoes) / len(avaliacoes)

    return {
        "usuario": db.query(Usuario).filter(Usuario.id == usuario_id).first(),
        "veiculo": db.query(Veiculo).filter(Veiculo.motorista_id == usuario_id).first(),
        "nota_media":  nota_media
    }

def update_usuario(usuario_db: Usuario, usuario: UsuarioRequest, db: Session) -> Usuario:
    for key, value in usuario.model_dump().items():
        setattr(usuario_db, key, value)

    db.commit()
    db.refresh(usuario_db)
    return usuario_db

def delete_usuario(usuario_db: Usuario, db: Session) -> Usuario:    
    db.delete(usuario_db)
    db.commit()

    return usuario_db