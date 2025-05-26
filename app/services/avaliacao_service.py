from sqlalchemy.orm import Session
from app.schemas.avaliacao import AvaliacaoRequest, AvaliacaoResponse
from app.models.avaliacao import Avaliacao
from app.shared.dependencies import get_email_service
from app.services.usuario_service import get_usuario
from app.repositories import AvaliacaoRepository as repo

def create_avaliacao(db: Session, avaliacao: AvaliacaoRequest) -> AvaliacaoResponse:
    nova_avaliacao = Avaliacao(**avaliacao.model_dump())
    avaliacao = repo(db).save(nova_avaliacao)

    # passageiro_db = get_usuario(usuario_id=nova_avaliacao.passageiro_id, db=db)

    # get_email_service().send_email(
    #     to_address=passageiro_db.email,
    #     subject="Avaliação Recebida",
    #     body=f"Agradecemos pela sua avaliação: {avaliacao.comentario}"
    # )

    return nova_avaliacao

def get_avaliacoes(db: Session, motorista_id: int, skip: int = 0, limit: int = 100) -> list[AvaliacaoResponse]:
    return repo(db).get_by_motorista(motorista_id=motorista_id)

def get_nota_media(db: Session, motorista_id: int) -> float:
    avaliacoes = repo(db).get_by_motorista(motorista_id=motorista_id)
    if not avaliacoes:
        return 0.0
    
    return sum(avaliacao.nota for avaliacao in avaliacoes) / len(avaliacoes)