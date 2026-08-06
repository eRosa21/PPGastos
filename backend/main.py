import os
import sys
from pathlib import Path
import uvicorn
import requests
# Adiciona a pasta infra ao path, para que 'from database.database import ...' funcione
INFRA_PATH = Path(__file__).resolve().parent / "src" / "infra"
sys.path.append(str(INFRA_PATH))

from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from src.infra.database.database import get_db,engine,Base
from src.infra.entities.models import Banco,Gastos,Caixinhas
from controllers.dependencies import catch_session
#from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

Base.metadata.create_all(bind=engine)

app = FastAPI()

#bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from controllers.auth_ctrl import auth_router

app.include_router(auth_router)

@app.get("/")
def root():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("API_PORT", 8001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)