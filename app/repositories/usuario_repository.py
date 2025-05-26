from app.models import Usuario
from sqlalchemy.orm import Session

class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, usuario: Usuario) -> Usuario:
        try:
            self.db.add(usuario)
            self.db.commit()
            self.db.refresh(usuario)
            return usuario
        except Exception as e:
            self.db.rollback()
            raise e

    def get_by_email(self, email: str) -> Usuario:
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def get_by_id(self, usuario_id: int) -> Usuario:
        return self.db.query(Usuario).filter(Usuario.id == usuario_id).first()
    
    def get_all(self) -> list[Usuario]:
        return self.db.query(Usuario).all()
    
    def delete(self, usuario_id: int) -> bool:
        usuario = self.get_by_id(usuario_id)
        if not usuario:
            return False

        try:
            usuario.status = 'inativo'
            self.db.commit()
            self.db.refresh(usuario)
            return True
        except Exception as e:
            self.db.rollback()
            raise e