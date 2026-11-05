import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from controllers.dependencies import verificar_token, catch_session
from schemas import UsuarioSchema
from src.infra.entities.models import Gastos
from dotenv import load_dotenv
from controllers.banco_ctrl import banco_router
from schemas import GastoSchema, BancoSchema

load_dotenv()

alter_router = APIRouter(prefix="/alter", tags=["alter"], dependencies=[Depends(verificar_token)])



@alter_router.post("/adicionar-gasto")
async def adicionar_gasto(gasto: GastoSchema, session: Session = Depends(catch_session)):
    novo_gasto = Gastos(
        nome=gasto.nome,
        valor=gasto.valor,
        tipo=gasto.tipo,
        id_banco=gasto.id_banco
    )
    session.add(novo_gasto)
    session.commit()    
    return  {"Gasto adicionado com sucesso."}

@alter_router.delete("/remover-gasto/{gasto_id}")
async def remover_gasto(gasto_id: int, session: Session = Depends(catch_session)):
    gasto = session.query(Gastos).filter(Gastos.id == gasto_id).first()
    if not gasto:
        raise HTTPException(status_code=404, detail="Transação não encontrada.")
    
    session.delete(gasto)
    session.commit()
    return {
        f"Gasto removido com sucesso."
        }
