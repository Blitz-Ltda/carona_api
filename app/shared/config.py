import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "API Modular"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

    SECRET_KEY = os.getenv("SECRET_KEY", "minha_chave_super_secreta")
    ALGORITHM = os.getenv("ALGORITHM", "HS256")
    EXPIRATION_MINUTES = int(os.getenv("EXPIRATION_MINUTES", 30))

    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.example.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")

settings = Settings()
