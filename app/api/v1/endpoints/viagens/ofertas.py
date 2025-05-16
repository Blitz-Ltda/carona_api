from fastapi import APIRouter
from app.schemas.viagem import ViagemCreate, ViagemResponse
from typing import List

router = APIRouter()

ofertas = []

@router.get("/", response_model=List[ViagemResponse])
def listar_ofertas():
    return ofertas

@router.post("/", status_code=201)
def criar_oferta(oferta: ViagemCreate):
    ofertas.append(oferta)
    return oferta
