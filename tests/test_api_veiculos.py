import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.shared.base import Base
from app.shared.dependencies import get_db

base_url = "/api/v1/veiculos" 

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


def test_create_veiculo(client):
    veiculo_data = {
        "marca": "Ford",
        "modelo": "Ka",
        "ano": 2020,
        "cor": "Preto",
        "placa": "XYZ-1234",
        "revanam": "Revanam Teste",
        "capacidade": 5,
        "tipo": "Carro",
        "motorista_id": 1
    }

    response = client.post(base_url, json=veiculo_data)
    assert response.status_code == 201
    data = response.json()
    assert data["marca"] == veiculo_data["marca"]

def test_get_veiculos(client):
    response = client.get(base_url)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_update_veiculo(client):
    response = client.get(base_url)
    if not response.json():
        pytest.skip("Sem veículos para testar update")

    veiculo_id = response.json()[0]["id"]
    update_data = {"modelo": "Ka Plus"}
    resp = client.put(f"{base_url}/{veiculo_id}", json=update_data)
    assert resp.status_code == 200
    assert resp.json()["modelo"] == "Ka Plus"

def test_delete_veiculo(client):
    response = client.get(base_url)
    if not response.json():
        pytest.skip("Sem veículos para deletar")

    veiculo_id = response.json()[0]["id"]
    resp = client.delete(f"{base_url}/{veiculo_id}")
    assert resp.status_code == 204
