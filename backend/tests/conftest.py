import os
import sys
from pathlib import Path

os.environ["DATABASE_URL"] = "sqlite:///./teste.db"
os.environ["SECRET_KEY"] = "chave-so-para-testes-0123456789-0123456789"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACESS_TOKEN_EXPIRE_MINUTES"] = "30"

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient

from main import app
from src.infra.database.database import Base, engine

# Trava de segurança: nunca rodar drop_all fora do banco de teste.
assert engine.url.get_backend_name() == "sqlite", "Os testes só podem rodar em SQLite!"


@pytest.fixture(autouse=True)
def banco_limpo():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth(client):
    client.post("/auth/registro", json={"nome": "t", "email": "t@t.com", "senha": "abc12345"})
    r = client.post("/auth/login-form", data={"username": "t@t.com", "password": "abc12345"})
    return {"Authorization": f"Bearer {r.json()['access_token']}"}