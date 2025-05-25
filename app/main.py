from fastapi import FastAPI
from app.api.v1.endpoints.usuarios import auth, usuarios
from app.api.v1.endpoints.veiculos import veiculos
from app.api.v1.endpoints.viagens import ofertas, reservas
from app.api.v1.endpoints.avaliacoes import avaliacoes
from app.shared.exception import NotFoundError, not_found_exception_handler

app = FastAPI(title="Aplicação de Transporte Modular")

# Rotas de Usuário
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(usuarios.router, prefix="/api/v1/usuarios", tags=["Usuarios"])

# Rotas de veiculos
app.include_router(veiculos.router, prefix="/api/v1/veiculos", tags=["Veiculos"])

# Rotas de Viagens
app.include_router(ofertas.router, prefix="/api/v1/viagens/ofertas", tags=["Ofertas"])
app.include_router(reservas.router, prefix="/api/v1/viagens/reservas", tags=["Reservas"])

# Rotas de Avaliações
app.include_router(avaliacoes.router, prefix="/api/v1/avaliacoes", tags=["Avaliações"])

app.add_exception_handler(
    NotFoundError,
    not_found_exception_handler
)