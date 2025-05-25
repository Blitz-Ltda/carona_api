from app.schemas.reserva import ReservaRequest, ReservaResponse
from app.services.viagem_service import *
from app.services.usuario_service import get_usuario
from app.shared.exception import NotFoundError
from app.shared.dependencies import get_db, get_email_service
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

@router.post("/")
def create_reserva_view(reserva: ReservaRequest, db: Session = Depends(get_db)):
    viagem_db = get_viagem(viagem_id=reserva.viagem_id, db=db)

    if not viagem_db:
        raise NotFoundError("Viagem para reserva")
    
    motorista_db = get_usuario(usuario_id=viagem_db.motorista_id, db=db)
    passageiro_db = get_usuario(usuario_id=reserva.passageiro_id, db=db)
    
    reserva_db = create_reserva(db=db, reserva=reserva)
    if not reserva_db:
        raise NotFoundError("Reserva")
    
    _send_motorista_reserva_email(to_address=motorista_db.email, reserva=reserva_db)
    _send_passageiro_reserva_pendente_email(to_address=passageiro_db.email, reserva=reserva_db, motorista_id=motorista_db.id)

    return reserva_db

@router.get("/{viagem_id}/reservas_pendentes", response_model=List[ReservaResponse])
def get_reservas_pendentes_view(viagem_id, db: Session = Depends(get_db)) -> List[ReservaResponse]:
    reservas = get_reservas_pendentes(viagem_id=viagem_id, db=db)
    if not reservas:
        raise NotFoundError("Reservas pendentes para a viagem")
    
    return reservas

@router.get("/{viagem_id}", response_model=List[ReservaResponse])
def get_reservas_view(viagem_id, db: Session = Depends(get_db)) -> List[ReservaResponse]:
    reservas = get_reservas(viagem_id=viagem_id, db=db)
    if not reservas:
        raise NotFoundError("Reservas confirmadas para a viagem")
    
    return reservas

@router.put("/{reserva_id}/confirmar")
def aprovar_reserva_view(reserva_id: int, db: Session = Depends(get_db)):
    reserva_db = get_reserva(reserva_id=reserva_id, db=db)
    if not reserva_db:
        raise NotFoundError("Reserva")
    
    viagem_db = get_viagem(viagem_id=reserva_db.viagem_id, db=db)
    if not viagem_db:
        raise NotFoundError("Viagem para reserva")
    
    motorista_db = get_usuario(usuario_id=viagem_db.motorista_id, db=db)
    passageiro_db = get_usuario(usuario_id=reserva_db.passageiro_id, db=db)

    if not motorista_db or not passageiro_db:
        raise NotFoundError("Motorista ou Passageiro")

    try:
        aprovar_reserva(reserva_db=reserva_db, viagem_db=viagem_db, db=db)

        _send_passageiro_reserva_confirmada_email(to_address=passageiro_db.email, reserva=reserva_db, motorista_id=motorista_db.id)
        return reserva_db
    except ValueError as e:
        raise NotFoundError(str(e))

@router.put("/{reserva_id}/recusar")
def recusar_reserva_view(reserva_id: int, db: Session = Depends(get_db)):
    reserva_db = get_reserva(reserva_id=reserva_id, db=db)
    if not reserva_db:
        raise NotFoundError("Reserva")
    
    viagem_db = get_viagem(viagem_id=reserva_db.viagem_id, db=db)
    if not viagem_db:
        raise NotFoundError("Viagem para reserva")
    
    motorista_db = get_usuario(usuario_id=viagem_db.motorista_id, db=db)
    passageiro_db = get_usuario(usuario_id=reserva_db.passageiro_id, db=db)

    if not motorista_db or not passageiro_db:
        raise NotFoundError("Motorista ou Passageiro")

    try:
        recusar_reserva(reserva_db=reserva_db, db=db)

        _send_passageiro_reserva_cancelada_email(to_address=passageiro_db.email, reserva=reserva_db, motorista_id=motorista_db.id)
        return reserva_db
    except ValueError as e:
        raise NotFoundError(str(e))

def _send_motorista_reserva_email(to_address: str, reserva: ReservaResponse) -> bool:
    subject = "Nova Reserva Recebida"
    body = f"""
    <html>
        <body>
            <h1>Nova Reserva</h1>
            <p>Você recebeu uma nova reserva para a viagem com ID {reserva.viagem_id}.</p>
            <p>Passageiro: {reserva.passageiro_id}</p>
            <p>Quantidade de vagas reservadas: {reserva.quantidade_vagas}</p>
        </body>
    </html>
    """
    
    return get_email_service().send_email(to_address, subject, body)

def _send_passageiro_reserva_pendente_email(to_address: str, reserva: ReservaResponse, motorista_id) -> bool:
    subject = "Reserva Pendente"
    body = f"""
    <html>
        <body>
            <h1>Reserva Pendente</h1>
            <p>Sua reserva para a viagem com ID {reserva.viagem_id} está pendente de confirmação.</p>
            <p>Motorista: {motorista_id}</p>
            <p>Quantidade de vagas reservadas: {reserva.quantidade_vagas}</p>
        </body>
    </html>
    """
    
    return get_email_service().send_email(to_address, subject, body)

def _send_passageiro_reserva_confirmada_email(to_address: str, reserva: ReservaResponse, motorista_id) -> bool:
    subject = "Reserva Confirmada"
    body = f"""
    <html>
        <body>
            <h1>Reserva Confirmada</h1>
            <p>Sua reserva para a viagem com ID {reserva.viagem_id} foi confirmada.</p>
            <p>Motorista: {motorista_id}</p>
            <p>Quantidade de vagas reservadas: {reserva.quantidade_vagas}</p>
        </body>
    </html>
    """
    
    return get_email_service().send_email(to_address, subject, body)

def _send_passageiro_reserva_cancelada_email(to_address: str, reserva: ReservaResponse, motorista_id) -> bool:
    subject = "Reserva Cancelada"
    body = f"""
    <html>
        <body>
            <h1>Reserva Cancelada</h1>
            <p>Sua reserva para a viagem com ID {reserva.viagem_id} foi cancelada.</p>
            <p>Motorista: {motorista_id}</p>
            <p>Quantidade de vagas reservadas: {reserva.quantidade_vagas}</p>
        </body>
    </html>
    """
    
    return get_email_service().send_email(to_address, subject, body)