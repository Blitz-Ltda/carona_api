from app.models import Avaliacao
from sqlalchemy.orm import Session

class AvaliacaoRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, avaliacao: Avaliacao) -> Avaliacao:
        try:
            self.db.add(avaliacao)
            self.db.commit()
            self.db.refresh(avaliacao)
            return avaliacao
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_viagem(self, viagem_id: int):
        return self.db.query(Avaliacao).filter(Avaliacao.viagem_id == viagem_id).all()
    
    def get_by_motorista(self, motorista_id: int):
        return self.db.query(Avaliacao).filter(Avaliacao.motorista_id == motorista_id).all()