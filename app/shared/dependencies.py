from app.shared.session import dbConnectionHandler

def get_db():
    db = dbConnectionHandler.__enter__()
    try:
        yield db.session
    finally:
        db.__exit__(None, None, None)