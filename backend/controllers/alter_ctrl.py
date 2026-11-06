import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from controllers.dependencies import verificar_token, catch_session
from schemas import UsuarioSchema
from src.infra.entities.models import Gastos, Banco
from dotenv import load_dotenv
from controllers.banco_ctrl import banco_router
from schemas import GastoSchema, BancoSchema, MeioPagamentoSchema
from src.infra.database.database import get_db

load_dotenv()

alter_router = APIRouter(prefix="/alter", tags=["alter"], dependencies=[Depends(verificar_token)])



@alter_router.post("/adicionar-gasto")
async def adicionar_gasto(gasto: GastoSchema, session: Session = Depends(get_db)):
    novo_gasto = Gastos(
        nome=gasto.nome,
        valor=gasto.valor,
        tipo=gasto.tipo,
        id_banco=gasto.id_banco,
        meio_pagamento=gasto.meio_pagamento,
        dia=gasto.dia,
    )
    meio_pagamento = gasto.meio_pagamento
    banco = session.get(Banco, gasto.id_banco)
    if not banco:
        raise HTTPException(status_code=404, detail="Banco não registrado.")
    
    if meio_pagamento == "débito":
        linhas = session.query(Banco).filter(Banco.id == gasto.id_banco, Banco.saldo >= gasto.valor).update(
            {"saldo": Banco.saldo - gasto.valor}
        )
        if linhas == 0:
            raise HTTPException(status_code=400, detail="Saldo insuficiente, verifique o seu saldo no programa.")
    elif meio_pagamento == "crédito":
        linhas = session.query(Banco).filter(Banco.id == gasto.id_banco).update(
            {"fatura": Banco.fatura + gasto.valor}
        )
    
    session.add(novo_gasto)
    session.commit()
  
    return  {"Gasto adicionado com sucesso."}

@alter_router.delete("/remover-gasto/{gasto_id}")
async def remover_gasto(gasto_id: int, session: Session = Depends(get_db)):
    gasto = session.query(Gastos).filter(Gastos.id == gasto_id).first()
    if not gasto:
        raise HTTPException(status_code=404, detail="Transação não encontrada.")
    
    session.delete(gasto)
    session.commit()
    
    return {
        f"Gasto removido com sucesso."
        }
