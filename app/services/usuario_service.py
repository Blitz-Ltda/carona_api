from sqlalchemy.orm import Session
from app.models import Usuario, Veiculo, Avaliacao
from app.repositories import UsuarioRepository, VeiculoRepository, AvaliacaoRepository
from app.schemas.usuario import UsuarioRequest
from app.shared.security import verificar_senha, criar_hash_da_senha

def create_usuario(db: Session, usuario: UsuarioRequest) -> Usuario:
    novo_usuario = Usuario(**usuario.model_dump())
    novo_usuario.senha = criar_hash_da_senha(usuario.senha)
    UsuarioRepository(db).save(novo_usuario)
    return novo_usuario

def get_usuario(usuario_id: int, db: Session) -> Usuario:
    return UsuarioRepository(db).get_by_id(usuario_id)

def get_usuarios(db: Session) -> list[Usuario]:
    return UsuarioRepository(db).get_all()

def get_perfil_completo(usuario_id: int, db: Session) -> dict:
    usuario = UsuarioRepository(db).get_by_id(usuario_id)
    if not usuario:
        return {}

    avaliacoes = AvaliacaoRepository(db).get_by_motorista(motorista_id=usuario_id)
    if not avaliacoes:
        nota_media = 0.0
    else:
        nota_media = sum(avaliacao.nota for avaliacao in avaliacoes) / len(avaliacoes)
    
    veiculo = VeiculoRepository(db).get_by_motorista_id(motorista_id=usuario_id)
    if not veiculo:
        veiculo = None

    return {
        "usuario": usuario,
        "veiculo": veiculo,
        "nota_media": nota_media
    }

def update_usuario(usuario_db: Usuario, usuario: dict, db: Session) -> Usuario:
    for key, value in usuario.items():
        setattr(usuario_db, key, value)

    return UsuarioRepository(db).save(usuario_db)

def delete_usuario(usuario_db: Usuario, db: Session) -> Usuario:    
    return UsuarioRepository(db).delete(usuario_id=usuario_db.id)