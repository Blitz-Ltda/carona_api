from app.shared.session import DBConnectionHandler as db
from app.shared.base import Base
from app.models import usuario, veiculo, viagem

class DBInit:
    def __init__(self):
        self.db = db()
    
    def create_db(self):
        with self.db as session:
            Base.metadata.drop_all(bind=session.get_engine())
            Base.metadata.create_all(bind=session.get_engine())
            print("Database tables created successfully.")

db_init = DBInit()