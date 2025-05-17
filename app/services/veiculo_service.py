from sqlalchemy.orm import Session
from app.models.veiculo import Veiculo
from app.schemas.veiculo import VeiculoRequest, VeiculoResponse

def create_veiculo(db: Session, veiculo: VeiculoRequest) -> Veiculo:
    novo_veiculo = Veiculo(**veiculo.model_dump())
    db.add(novo_veiculo)
    db.commit()
    db.refresh(novo_veiculo)
    return novo_veiculo

def get_veiculo(veiculo_id: int, db: Session) -> Veiculo:
    return db.query(Veiculo).filter(Veiculo.id == veiculo_id).first()

def get_veiculos(db: Session, skip: int = 0, limit: int = 100) -> list[Veiculo]:
    return db.query(Veiculo).offset(skip).limit(limit).all()

def update_veiculo(veiculo_db: Veiculo, veiculo: VeiculoRequest, db: Session) -> Veiculo:   
    for key, value in veiculo.model_dump().items():
        setattr(veiculo_db, key, value)

    db.commit()
    db.refresh(veiculo_db)
    return veiculo_db

def delete_veiculo(veiculo_db: Veiculo, db: Session) -> int:    
    db.delete(veiculo_db)
    db.commit()

    return veiculo_db.id