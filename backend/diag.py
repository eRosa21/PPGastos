import os
from pathlib import Path
from urllib.parse import urlparse
from dotenv import dotenv_values

def resumo(url):
    u = urlparse(url)
    return f"{u.scheme} | {u.hostname}:{u.port}{u.path}"   # sem senha

amb = os.environ.get("DATABASE_URL")
print("Ambiente do Windows:", resumo(amb) if amb else "não definida")

raiz = Path(__file__).resolve().parents[1]
for rel in [".env", "backend/.env", "backend/src/infra/.env", "alembic/.env"]:
    p = raiz / rel
    url = dotenv_values(p).get("DATABASE_URL") if p.exists() else None
    print(rel, "->", resumo(url) if url else ("não existe" if not p.exists() else "sem DATABASE_URL"))