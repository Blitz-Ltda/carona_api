from sqlalchemy.orm import Session
from app.models.veiculo import Veiculo
from app.schemas.veiculo import VeiculoRequest, VeiculoResponse
from app.repositories import VeiculoRepository

def create_veiculo(db: Session, veiculo: VeiculoRequest) -> Veiculo:
    novo_veiculo = Veiculo(**veiculo.model_dump())

    return VeiculoRepository(db).save(novo_veiculo)

def get_veiculo(veiculo_id: int, db: Session) -> Veiculo:
    return VeiculoRepository(db).get_by_id(veiculo_id)

def get_veiculos(db: Session) -> list[Veiculo]:
    return VeiculoRepository(db).get_all()

def get_veiculos_por_motorista(motorista_id: int, db: Session) -> list[Veiculo]:
    return VeiculoRepository(db).get_by_motorista_id(motorista_id=motorista_id)

def update_veiculo(veiculo_db: Veiculo, veiculo: dict, db: Session) -> Veiculo:   
    for key, value in veiculo.items():
        setattr(veiculo_db, key, value)

    return VeiculoRepository(db).save(veiculo_db)

def delete_veiculo(veiculo_db: Veiculo, db: Session) -> bool:
    return VeiculoRepository(db).delete(veiculo_id=veiculo_db.id)