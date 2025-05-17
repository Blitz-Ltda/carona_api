from app.schemas.veiculo import VeiculoRequest, VeiculoResponse
from app.shared.dependencies import get_db
from app.services.veiculo_service import *
from app.shared.exception import NotFoundError
from fastapi import APIRouter, Depends
from typing import List

router = APIRouter()

@router.get("/", response_model=List[VeiculoResponse])
def listar_veiculos(db: Session = Depends(get_db)):
    return get_veiculos(db=db)

@router.post("/", status_code=201)
def criar_veiculo(veiculo: VeiculoRequest, db: Session = Depends(get_db)):
    return create_veiculo(db=db, veiculo=veiculo)

@router.put("/{veiculo_id}", status_code=200)
def atualizar_veiculo(veiculo_id: int, veiculo: VeiculoRequest, db: Session = Depends(get_db)):
    veiculo_db = _get_veiculo_by_id(veiculo_id=veiculo_id, db=db)

    return update_veiculo(veiculo_db=veiculo_db, db=db)

@router.delete("/{veiculo_id}", status_code=204)
def deletar_veiculo(veiculo_id: int, db: Session = Depends(get_db)):
    veiculo_db = _get_veiculo_by_id(veiculo_id=veiculo_id, db=db)

    return delete_veiculo(veiculo_db=veiculo_db, db=db)

def _get_veiculo_by_id(veiculo_id: int, db: Session = Depends(get_db)):
    veiculo = get_veiculo(veiculo_id=veiculo_id, db=db)
    if not veiculo:
        raise NotFoundError("Veiculo")
    
    return veiculo