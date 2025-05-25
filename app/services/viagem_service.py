from sqlalchemy.orm import Session
from app.models.viagem import Viagem, viagem_status_enum
from app.models.reserva import Reserva, reserva_status_enum
from app.schemas.viagem import ViagemRequest, ViagemResponse
from app.schemas.reserva import ReservaRequest, ReservaResponse

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

def iniciar_viagem(viagem_db: Viagem, db: Session) -> ViagemResponse:
    viagem_db.status = viagem_status_enum.enums[4]  # Em andamento
    db.commit()
    db.refresh(viagem_db)

    return viagem_db

def finalizar_viagem(viagem_db: Viagem, db: Session) -> ViagemResponse:
    viagem_db.status = viagem_status_enum.enums[3]
    db.commit()
    db.refresh(viagem_db)

    return viagem_db

def reduzir_vagas(viagem_db: Viagem, quantidade: int, db: Session) -> ViagemResponse:
    if viagem_db.vagas >= quantidade:
        viagem_db.vagas -= quantidade
        db.commit()
        db.refresh(viagem_db)
    else:
        raise ValueError("Quantidade de vagas insuficiente")

    return viagem_db

# Reservas
def create_reserva(db: Session, reserva: ReservaRequest) -> ReservaResponse:
    nova_reserva = Reserva(**reserva.model_dump())

    if reserva.quantidade_vagas <= 0:
        raise ValueError("Quantidade de vagas deve ser maior que zero")
    
    db.add(nova_reserva)
    db.commit()
    db.refresh(nova_reserva)

    return nova_reserva


def get_reserva(reserva_id: int, db: Session) -> ReservaResponse:
    return db.query(Reserva).filter(Reserva.id == reserva_id).first()

def get_reservas_finalizadas(viagem_id: int, db: Session, skip: int = 0, limit: int = 100) -> list[ReservaResponse]:
    return db.query(Reserva).where(
        Reserva.viagem_id == viagem_id,
        Reserva.status == reserva_status_enum.enums[3]  # Finalizada
    ).offset(skip).limit(limit).all()

def get_reservas_pendentes(viagem_id: int, db: Session, skip: int = 0, limit: int = 100) -> list[ReservaResponse]:
    return db.query(Reserva).where(
        Reserva.viagem_id == viagem_id,
        Reserva.status == reserva_status_enum.enums[0]  # Pendente
    ).offset(skip).limit(limit).all()

def get_reservas_confirmadas(viagem_id: int, db: Session, skip: int = 0, limit: int = 100) -> list[ReservaResponse]:
    return db.query(Reserva).where(
        Reserva.viagem_id == viagem_id,
        Reserva.status == reserva_status_enum.enums[1]  # Aprovada
    ).offset(skip).limit(limit).all()

def get_reservas(viagem_id: int, db: Session, skip: int = 0, limit: int = 100) -> list[ReservaResponse]:
    return db.query(Reserva).where(
        Reserva.viagem_id == viagem_id
    ).offset(skip).limit(limit).all()

def update_reserva(reserva_db: Reserva, reserva: Reserva, db: Session) -> ReservaResponse:
    for key, value in reserva.model_dump().items():
        setattr(reserva_db, key, value)

    db.commit()
    db.refresh(reserva_db)

    return reserva_db

def delete_reserva(reserva_db: Reserva, db: Session) -> int:
    db.delete(reserva_db)
    db.commit()

    return reserva_db.id

def aprovar_reserva(reserva_db: Reserva, viagem_db: Viagem, db: Session) -> int:    
    try:
        reserva_db.status = reserva_status_enum.enums[1]  # Aprovada

        reduzir_vagas(viagem_db=viagem_db, quantidade=reserva_db.quantidade_vagas, db=db)
        db.commit()
        db.refresh(reserva_db)

        return reserva_db.id
    except ValueError as e:
        raise ValueError(f"Erro ao aprovar reserva: {str(e)}") from e
    

def recusar_reserva(reserva_db: Reserva, db: Session) -> int:
    reserva_db.status = reserva_status_enum.enums[2]  # Recusada
    db.commit()
    db.refresh(reserva_db)

    return reserva_db.id