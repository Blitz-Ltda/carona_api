from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.shared.config import settings

class DBConnectionHandler:
    def __init__(self):
        self.__connection_string = settings.DATABASE_URL
        self.__engine = self.__create_engine()
        self.session = None

    def __create_engine(self):
        engine = create_engine(
            self.__connection_string,
            pool_pre_ping = True,
        )
        return engine
    
    def get_engine(self):
        return self.__engine
    
    def __enter__(self):
        self.session = sessionmaker(bind=self.__engine)()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

dbConnectionHandler = DBConnectionHandler()
