from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.avaliacao import AvaliacaoRequest, AvaliacaoResponse
from app.services.avaliacao_service import create_avaliacao, get_avaliacoes
from app.shared.dependencies import get_db

router = APIRouter()

@router.post('/', response_model=AvaliacaoResponse, status_code=201)
def create_avaliacao_view(avaliacao: AvaliacaoRequest, db: Session = Depends(get_db)):
    return create_avaliacao(db=db, avaliacao=avaliacao)

@router.get('/{viagem_id}', response_model=list[AvaliacaoResponse])
def get_avaliacoes_view(viagem_id: int, db: Session = Depends(get_db)):
    return get_avaliacoes(db, viagem_id)