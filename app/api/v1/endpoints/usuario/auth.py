from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.schemas.auth import LoginData
from app.services.auth_service import login

router = APIRouter()

@router.post("/login")
def realizar_login(data: LoginData, db: Session = Depends(get_db)):
    token = login(db, data.email, data.senha)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    return {"access_token": token, "token_type": "bearer"}
