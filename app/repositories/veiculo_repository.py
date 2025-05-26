from app.models import Veiculo
from sqlalchemy.orm import Session

class VeiculoRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, veiculo: Veiculo) -> Veiculo:
        try:
            self.db.add(veiculo)
            self.db.commit()
            self.db.refresh(veiculo)
            return veiculo
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_id(self, veiculo_id: int) -> Veiculo:
        return self.db.query(Veiculo).filter(Veiculo.id == veiculo_id).first()
    
    def get_by_motorista_id(self, motorista_id: int) -> list[Veiculo]:
        return self.db.query(Veiculo).filter(Veiculo.motorista_id == motorista_id).all()

    def get_all(self) -> list[Veiculo]:
        return self.db.query(Veiculo).all()

    def delete(self, veiculo_id: int) -> bool:
        veiculo = self.get_by_id(veiculo_id)
        if veiculo:
            try:
                self.db.delete(veiculo)
                self.db.commit()
                return True
            except Exception as e:
                self.db.rollback()
                raise e