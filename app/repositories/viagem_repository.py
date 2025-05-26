from app.models import Viagem
from sqlalchemy.orm import Session

class ViagemRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, viagem: Viagem) -> Viagem:
        try:
            self.db.add(viagem)
            self.db.commit()
            self.db.refresh(viagem)
            return viagem
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_id(self, viagem_id: int) -> Viagem:
        return self.db.query(Viagem).filter(Viagem.id == viagem_id).first()

    def get_by_usuario(self, usuario_id: int) -> list[Viagem]:
        return self.db.query(Viagem).filter(Viagem.usuario_id == usuario_id).all()

    def get_all(self) -> list[Viagem]:
        return self.db.query(Viagem).all()

    def delete(self, viagem_id: int) -> bool:
        viagem = self.get_by_id(viagem_id)
        if viagem:
            try:
                self.db.delete(viagem)
                self.db.commit()
                return True
            except Exception as e:
                self.db.rollback()
                raise e