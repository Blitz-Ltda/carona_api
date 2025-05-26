from app.models import Reserva
from sqlalchemy.orm import Session

class ReservaRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, reserva: Reserva) -> Reserva :
        try:
            self.db.add(reserva)
            self.db.commit()
            self.db.refresh(reserva)
            return reserva
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_id(self, reserva_id: int) -> Reserva:
        return self.db.query(Reserva).filter(Reserva.id == reserva_id).first()

    def get_by_usuario(self, usuario_id: int) -> list[Reserva]:
        return self.db.query(Reserva).filter(Reserva.usuario_id == usuario_id).all()
    
    def get_by_status(self, viagem_id: int, status: str) -> list[Reserva]:
        return self.db.query(Reserva).filter(
            Reserva.viagem_id == viagem_id,
            Reserva.status == status
        ).all()
    
    def get_by_viagem(self, viagem_id: int) -> list[Reserva]:
        return self.db.query(Reserva).filter(Reserva.viagem_id == viagem_id).all()
    
    def delete(self, reserva_id: int) -> bool:
        reserva = self.get_by_id(reserva_id)
        if reserva:
            try:
                self.db.delete(reserva)
                self.db.commit()
                return True
            except Exception as e:
                self.db.rollback()
                raise e