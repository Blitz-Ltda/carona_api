import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.shared.base import Base
from app.shared.dependencies import get_db

base_avaliacoes_url = "/api/v1/avaliacoes" 

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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

def test_create_avaliacao(client):
    avaliacao_data = {
        "viagem_id": 1,
        "passageiro_id": 1,
        "motorista_id": 1,
        "nota": 4,
        "comentario": "Boa viagem"
    }
    response = client.post(base_avaliacoes_url, json=avaliacao_data)
    assert response.status_code == 201
    data = response.json()
    assert data["nota"] == avaliacao_data["nota"]

def test_get_avaliacoes_by_viagem(client):
    response = client.get(f"{base_avaliacoes_url}/1")
    assert response.status_code in (200, 404)
