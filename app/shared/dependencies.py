from app.shared.session import dbConnectionHandler
from app.services.email_service import EmailService

def get_email_service():
    return EmailService()

def get_db():
    db = dbConnectionHandler.__enter__()
    try:
        yield db.session
    finally:
        db.__exit__(None, None, None)