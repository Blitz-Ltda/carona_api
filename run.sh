#!/bin/bash

#python3 -m venv venv
#source venv/bin/activate

#pip install -r requirements.txt

# alembic init alembic
# alembic revision --autogenerate -m "cria tabelas principais"
# alembic upgrade head

export PYTHONPATH=.
uvicorn app.main:app --reload