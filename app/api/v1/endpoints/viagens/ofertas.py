from app.schemas.viagem import ViagemRequest, ViagemResponse
from app.services.viagem_service import *
from app.services.usuario_service import get_usuario
from app.shared.exception import NotFoundError
from app.shared.dependencies import get_db, get_email_service
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.get("/", response_model=List[ViagemResponse])
def get_viagens_view(db: Session = Depends(get_db)):
    return get_viagens(db=db)

@router.post("/", status_code=201)
def create_viagem_view(oferta: ViagemRequest, db: Session = Depends(get_db)):
    return create_viagem(db=db, viagem=oferta)

@router.put("/{viagem_id}", status_code=200)
def update_viagem_view(viagem_id: int, viagem: ViagemRequest, db: Session = Depends(get_db)):
    viagem_db = _get_viagem_by_id(viagem_id=viagem_id, db=db)
    return update_viagem(viagem_db=viagem_db, db=db, viagem=viagem)

@router.delete("/{viagem_id}", status_code=204)
def delete_viagem_view(viagem_id: int, db: Session = Depends(get_db)):
    viagem_db = _get_viagem_by_id(viagem_id=viagem_id, db=db)
    return delete_viagem(viagem_db=viagem_db, db=db)

@router.put("/finalizar_viagem/{id}", status_code=200)
def finalizar_viagem_view(id: int, db: Session = Depends(get_db)):
    viagem_db = _get_viagem_by_id(viagem_id=id, db=db)
    usuario_db = get_usuario(usuario_id=viagem_db.motorista_id, db=db)


    send_viagem_finalizada_email(to_address=usuario_db.email, viagem_id=id)

    return finalizar_viagem(viagem_db=viagem_db, db=db)

def send_viagem_finalizada_email(to_address: str, viagem_id: int) -> bool:
    subject = "Viagem Finalizada"
    body = f"""
    <html>
        <body>
            <h1>Viagem Finalizada</h1>
            <p>Sua viagem com ID {viagem_id} foi finalizada com sucesso.</p>
        </body>
    </html>
    """
    
    return get_email_service().send_email(to_address, subject, body)


def _get_viagem_by_id(viagem_id: int, db: Session = Depends(get_db)):
    viagem = get_viagem(viagem_id=viagem_id, db=db)
    if not viagem:
        raise NotFoundError("Viagem")
    
    return viagem
