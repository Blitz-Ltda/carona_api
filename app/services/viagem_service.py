from sqlalchemy.orm import Session
from app.models.viagem import Viagem
from app.schemas.viagem import ViagemRequest, ViagemResponse

def create_viagem(db: Session, viagem: ViagemRequest) -> ViagemResponse:
    nova_viagem = Viagem(**viagem.model_dump())
    db.add(nova_viagem)
    db.commit()
    db.refresh(nova_viagem)
    return nova_viagem

def get_viagem(viagem_id: int, db: Session) -> ViagemResponse:
    return db.query(Viagem).filter(Viagem.id == viagem_id).first()

def get_viagens(db: Session, skip: int = 0, limit: int = 100) -> list[ViagemResponse]:
    return db.query(Viagem).offset(skip).limit(limit).all()

def update_viagem(viagem_db: Viagem, viagem: ViagemRequest, db: Session) -> ViagemResponse:    
    for key, value in viagem.model_dump().items():
        setattr(viagem_db, key, value)

    db.commit()
    db.refresh(viagem_db)

    return viagem_db

def delete_viagem(viagem_db: Viagem, db: Session) -> int:
    db.delete(viagem_db)
    db.commit()

    return viagem_db.id