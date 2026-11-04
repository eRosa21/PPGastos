import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from src.infra.database.database import get_db,engine,Base
from src.infra.entities.models import Banco, Gastos, Caixinhas, Usuario
load_dotenv()

#print("API conectada em:", engine.url.render_as_string(hide_password=True))

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

from controllers.auth_ctrl import auth_router
from controllers.alter_ctrl import alter_router
app.include_router(auth_router)
app.include_router(alter_router)

@app.get("/")
def root():
    return {"status": "ok"}

if __name__ == "__main__":
    port = int(os.environ.get("API_PORT", 8001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)