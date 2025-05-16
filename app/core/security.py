from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha_plain, senha_hash):
    return pwd_context.verify(senha_plain, senha_hash)

def criar_hash_da_senha(senha):
    return pwd_context.hash(senha)

def criar_token_jwt(dados: dict):
    to_encode = dados.copy()
    exp = datetime.now() + timedelta(minutes=settings.EXPIRATION_MINUTES)
    to_encode.update({"exp": exp})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
