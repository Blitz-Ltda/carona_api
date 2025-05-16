from fastapi import APIRouter
from app.schemas.veiculo import VeiculoCreate, VeiculoResponse
from typing import List

router = APIRouter()

veiculos = []

@router.get("/", response_model=List[VeiculoResponse])
def listar_veiculos():
    return veiculos

@router.post("/", status_code=201)
def criar_veiculo(veiculo: VeiculoCreate):
    veiculos.append(veiculo)
    return veiculo