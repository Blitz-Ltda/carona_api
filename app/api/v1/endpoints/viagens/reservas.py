from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def criar_reserva():
    return {"msg": "Reserva criada com sucesso"}
