from fastapi import FastAPI
from app.api.v1.endpoints.usuario import auth, passageiros, motoristas
from app.api.v1.endpoints.veiculos import veiculos
from app.api.v1.endpoints.viagens import ofertas, reservas

from app.db.init_db import db_init
db_init.create_db()

app = FastAPI(title="Aplicação de Transporte Modular")

# Rotas de Usuário
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(passageiros.router, prefix="/api/v1/passageiros", tags=["Passageiros"])
app.include_router(motoristas.router, prefix="/api/v1/motoristas", tags=["Motoristas"])

# Rotas de veiculos
app.include_router(veiculos.router, prefix="/api/v1/veiculos", tags=["Veiculos"])

# Rotas de Viagens
app.include_router(ofertas.router, prefix="/api/v1/viagens/ofertas", tags=["Ofertas"])
app.include_router(reservas.router, prefix="/api/v1/viagens/reservas", tags=["Reservas"])
