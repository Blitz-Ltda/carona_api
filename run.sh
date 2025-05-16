#!/bin/bash

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

export PYTHONPATH=.
uvicorn app.main:app --reload