import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "API Modular"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

    SECRET_KEY = os.getenv("SECRET_KEY", "minha_chave_super_secreta")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    EXPIRATION_MINUTES = int(os.getenv("EXPIRATION_MINUTES", 30))

settings = Settings()
