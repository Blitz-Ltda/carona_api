from sqlalchemy.orm import Session
from app.models.viagem import Viagem, viagem_status_enum
from app.models.reserva import Reserva, reserva_status_enum
from app.schemas.viagem import ViagemRequest, ViagemResponse
from app.schemas.reserva import ReservaRequest, ReservaResponse
from app.repositories import ViagemRepository, ReservaRepository

def create_viagem(db: Session, viagem: ViagemRequest) -> ViagemResponse:
    nova_viagem = Viagem(**viagem.model_dump())
    return ViagemRepository(db).save(nova_viagem)

def get_viagem(viagem_id: int, db: Session) -> ViagemResponse:
    return ViagemRepository(db).get_by_id(viagem_id)

def get_viagens(db: Session) -> list[ViagemResponse]:
    return ViagemRepository(db).get_all()

def update_viagem(viagem_db: Viagem, viagem: dict, db: Session) -> ViagemResponse:    
    for key, value in viagem.items():
        setattr(viagem_db, key, value)

    return ViagemRepository(db).save(viagem_db)

def delete_viagem(viagem_db: Viagem, db: Session) -> bool:
    return ViagemRepository(db).delete(viagem_id=viagem_db.id)

def iniciar_viagem(viagem_db: Viagem, db: Session) -> ViagemResponse:
    viagem_db.status = viagem_status_enum.enums[4]  # Em andamento
    return ViagemRepository(db).save(viagem_db)

def finalizar_viagem(viagem_db: Viagem, db: Session) -> ViagemResponse:
    viagem_db.status = viagem_status_enum.enums[3]
    return ViagemRepository(db).save(viagem_db)

def reduzir_vagas(viagem_db: Viagem, quantidade: int, db: Session) -> ViagemResponse:
    if viagem_db.vagas >= quantidade:
        viagem_db.vagas -= quantidade
        return ViagemRepository(db).save(viagem_db)
    else:
        raise ValueError("Quantidade de vagas insuficiente")

# Reservas
def create_reserva(db: Session, reserva: ReservaRequest) -> ReservaResponse:
    nova_reserva = Reserva(**reserva.model_dump())

    if reserva.quantidade_vagas <= 0:
        raise ValueError("Quantidade de vagas deve ser maior que zero")
    
    return ReservaRepository(db).save(nova_reserva)

def get_reserva(reserva_id: int, db: Session) -> ReservaResponse:
    return ReservaRepository(db).get_by_id(reserva_id)

def get_reservas_finalizadas(viagem_id: int, db: Session) -> list[ReservaResponse]:
    return ReservaRepository(db).get_by_status(viagem_id=viagem_id, status=reserva_status_enum.enums[3])  # Finalizada

def get_reservas_pendentes(viagem_id: int, db: Session) -> list[ReservaResponse]:
    return ReservaRepository(db).get_by_status(viagem_id=viagem_id, status=reserva_status_enum.enums[0])  # Pendente

def get_reservas_confirmadas(viagem_id: int, db: Session) -> list[ReservaResponse]:
    return ReservaRepository(db).get_by_status(viagem_id=viagem_id, status=reserva_status_enum.enums[1])  # Aprovada


def get_reservas(viagem_id: int, db: Session) -> list[ReservaResponse]:
    return ReservaRepository(db).get_by_viagem(viagem_id=viagem_id)

def update_reserva(reserva_db: Reserva, reserva: dict, db: Session) -> ReservaResponse:
    for key, value in reserva.items():
        setattr(reserva_db, key, value)

    return ReservaRepository(db).save(reserva_db)

def delete_reserva(reserva_db: Reserva, db: Session) -> bool:
    return ReservaRepository(db).delete(reserva_id=reserva_db.id)

def aprovar_reserva(reserva_db: Reserva, viagem_db: Viagem, db: Session) -> int:    
    try:
        reserva_db.status = reserva_status_enum.enums[1]  # Aprovada

        reduzir_vagas(viagem_db=viagem_db, quantidade=reserva_db.quantidade_vagas, db=db)
        return ReservaRepository(db).save(reserva_db).id
    except ValueError as e:
        raise ValueError(f"Erro ao aprovar reserva: {str(e)}") from e
    

def recusar_reserva(reserva_db: Reserva, db: Session) -> int:
    reserva_db.status = reserva_status_enum.enums[2]  # Recusada
    return ReservaRepository(db).save(reserva_db).id