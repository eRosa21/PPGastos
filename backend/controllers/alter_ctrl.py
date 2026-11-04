import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from controllers.dependencies import verificar_token, catch_session
from schemas import UsuarioSchema
from src.infra.entities.models import Gastos
from dotenv import load_dotenv

load_dotenv()

alter_router = APIRouter(prefix="/alter", tags=["alter"], dependencies=[Depends(verificar_token)])

@alter_router.post("/adicionar-gasto")
async def adicionar_gasto(gasto: dict, session: Session = Depends(catch_session)):
    
    return{"Gasto adicionado com sucesso."}

@alter_router.delete("/remover-gasto")
async def remover_gasto(gasto_id: int, session: Session = Depends(catch_session)):
    gasto = session.get(Gastos, gasto_id)
    if not gasto:
        raise HTTPException(status_code=404, detail="Transação não encontrada.")
    
    session.delete(gasto)
    session.commit()
    return {"Gasto removido com sucesso."}
    