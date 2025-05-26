import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.shared.base import Base
from app.shared.dependencies import get_db

base_user_url = "/api/v1/usuarios" 
# client = TestClient(app)

# Configurar banco SQLite em memória para testes
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_create_user(client):
    user_data = {
        "nome": "João Silva",
        "email": "joao@example.com",
        "senha": "senha123",
        "genero": "masculino",
        "telefone": "11999999999",
        "matricula": "123456789",
        "nome_emergencia": "Maria Silva",
        "telefone_emergencia": "11988888888",
        "descricao": "Usuário de teste",
    }

    response = client.post(base_user_url, json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == user_data["nome"]
    assert "id" in data


def test_get_users(client):
    response = client.get(base_user_url)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(user["nome"] == "João Silva" for user in data)


def test_update_user(client):
    # client.post(base_user_url, json={"nome": "João Silva","email": "joao@example.com","senha": "senha123","genero": "masculino","telefone": "11999999999","matricula": "1234553","nome_emergencia": "Maria Silva","telefone_emergencia": "11988888888","descricao": "Usuário de teste"})
    response_users = client.get(base_user_url)

    user_id = response_users.json()[0]["id"]
    update_data = {
        "nome": "João Atualizado"
    }

    response = client.put(f"{base_user_url}/{user_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["nome"] == update_data["nome"]

def test_delete_user(client):
    # Criar usuário para deletar
    user_data = {"nome": "Usuário Para Deletar","email": "delete@example.com","senha": "senha123","telefone": "11977777777","genero": "masculino","telefone": "11999999999","matricula": "12222789","nome_emergencia": "Maria Silva","telefone_emergencia": "11988888888","descricao": "Usuário de teste"}

    response = client.post(base_user_url, json=user_data)
    user_id = response.json()["id"]

    response_delete = client.delete(f"{base_user_url}/{user_id}")
   
    assert response_delete.status_code == 204

    # Verificar se usuário foi deletado
    # response_check = client.get(f"/usuarios/{user_id}/perfil_completo")
    # assert response_check.status_code == 404

