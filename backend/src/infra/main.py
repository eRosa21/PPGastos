import os
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from database.database import get_db,engine,Base
from entities.models import Banco,Gastos,Caixinhas

load_dotenv()

Base.metadata.create_all(bind=engine)


app = FastAPI()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001,reload = True)