import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.shared.base import Base
from app.shared.dependencies import get_db

base_url = "/api/v1/viagens" 

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

def test_create_viagem_offer(client):
    offer_data = {
        "motorista_id": 1,
        "origem": "Maceió",
        "destino": "Arapiraca",
        "data_hora": "2025-06-01T08:00:00",
        "vagas": 3,
        "descricao": "Carona para trabalho"
    }
    response = client.post(f"{base_url}/ofertas/", json=offer_data)
    assert response.status_code == 201
    data = response.json()
    assert data["origem"] == offer_data["origem"]

def test_get_viagem_offers(client):
    response = client.get(f"{base_url}/ofertas/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_update_viagem_offer(client):
    response = client.get(f"{base_url}/ofertas/")
    if not response.json():
        pytest.skip("Sem ofertas para testar update")
    viagem_id = response.json()[0]["id"]
    update_data = {"vagas": 2}
    resp = client.put(f"f{base_url}/ofertas/{viagem_id}", json=update_data)
    assert resp.status_code == 200
    assert resp.json()["vagas"] == 2

def test_start_and_finish_viagem(client):
    response = client.get(f"{base_url}/ofertas/")
    if not response.json():
        pytest.skip("Sem ofertas para testar start/finish")
    viagem_id = response.json()[0]["id"]
    resp_start = client.put(f"{base_url}/ofertas/iniciar_viagem/{viagem_id}")
    assert resp_start.status_code == 200
    resp_finish = client.put(f"{base_url}/ofertas/finalizar_viagem/{viagem_id}")
    assert resp_finish.status_code == 200

def test_delete_viagem_offer(client):
    response = client.get(f"{base_url}/ofertas/")
    if not response.json():
        pytest.skip("Sem ofertas para deletar")
    viagem_id = response.json()[0]["id"]
    resp = client.delete(f"{base_url}/ofertas/{viagem_id}")
    assert resp.status_code == 204

def test_create_reserva(client):
    reserva_data = {
        "viagem_id": 1,
        "passageiro_id": 2,
        "status": "pendente"
    }
    response = client.post(f"{base_url}/reservas/", json=reserva_data)
    assert response.status_code == 201

def test_get_reservas_pendentes(client):
    response = client.get(f"{base_url}/reservas/1/reservas_pendentes")
    assert response.status_code in (200, 404)

def test_confirm_and_recusar_reserva(client):
    response = client.get(f"{base_url}/reservas/1/reservas_pendentes")
    reservas = response.json() if response.status_code == 200 else []
    if not reservas:
        pytest.skip("Sem reservas pendentes para confirmar/recusar")
    reserva_id = reservas[0]["id"]
    resp_confirm = client.put(f"{base_url}/reservas/{reserva_id}/confirmar")
    assert resp_confirm.status_code == 200
    resp_recusar = client.put(f"{base_url}/reservas/{reserva_id}/recusar")
    assert resp_recusar.status_code == 200
