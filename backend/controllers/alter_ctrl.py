from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from controllers.dependencies import verificar_token
from schemas import UsuarioSchema, GastoSchema
from src.infra.entities.models import Gastos, Banco, Usuario
from dotenv import load_dotenv
from controllers.banco_ctrl import banco_router
from src.infra.database.database import get_db

load_dotenv()

alter_router = APIRouter(prefix="/alter", tags=["alter"], dependencies=[Depends(verificar_token)])

def aplicar_efeito(session, gasto):
    if gasto.meio_pagamento == "débito":
        linhas = session.query(Banco).filter(Banco.id == gasto.id_banco, Banco.saldo >= gasto.valor).update(
            {"saldo": Banco.saldo - gasto.valor}
        )
        if linhas == 0:
            raise HTTPException(status_code=400, detail="Saldo insuficiente para realizar a operação.")
    elif gasto.meio_pagamento == "crédito":
        linhas = session.query(Banco).filter(Banco.id == gasto.id_banco).update(
            {"fatura": Banco.fatura + gasto.valor}
        )
    
def desfazer_efeito(session,gasto):
    if gasto.meio_pagamento == "débito":
        linhas = session.query(Banco).filter(Banco.id == gasto.id_banco).update(
            {"saldo": Banco.saldo + gasto.valor}
        )
    elif gasto.meio_pagamento == "crédito":
        linhas = session.query(Banco).filter(Banco.id == gasto.id_banco, Banco.fatura >= gasto.valor).update(
            {"fatura": Banco.fatura - gasto.valor}    
        )
        if linhas == 0:
            raise HTTPException(status_code= 409, detail= "Fatura menor que o gasto removido, não é possível desfazer")
        
        
@alter_router.post("/adicionar-gasto")
def adicionar_gasto(gasto: GastoSchema, session: Session = Depends(get_db), usuario : Usuario = Depends(verificar_token)):
    if gasto.valor <= 0:
        raise HTTPException(status_code=400, detail="O valor deve ser maior que zero.")

    banco = session.get(Banco, gasto.id_banco)
    if not banco:
        raise HTTPException(status_code=404, detail="Banco não registrado.")
    if banco.usuario_id != usuario.id and not usuario.admin:
        raise HTTPException(status_code=403, detail="Você não tem acesso para usar este banco.")

    novo_gasto = Gastos(
        nome=gasto.nome,
        valor=gasto.valor,
        tipo=gasto.tipo,
        id_banco=gasto.id_banco,
        usuario_id=usuario.id,
        meio_pagamento=gasto.meio_pagamento,
        dia=gasto.dia,
    )
    
    aplicar_efeito(session,novo_gasto)
    session.add(novo_gasto)
    session.commit()
  
    return  {"Gasto adicionado com sucesso."}

@alter_router.delete("/remover-gasto/{gasto_id}")
def remover_gasto(gasto_id: int, session: Session = Depends(get_db), usuario : Usuario = Depends(verificar_token)):
    gasto = session.query(Gastos).filter(Gastos.id == gasto_id).first()
    if not gasto:
        raise HTTPException(status_code=404, detail="Transação não encontrada.")
    if usuario.id != gasto.usuario_id and not usuario.admin:
        raise HTTPException(status_code=403, detail="Você não tem acesso para realizar esta remoção.")
    
    desfazer_efeito(session, gasto)
    session.delete(gasto)
    session.commit()
    
    return {
        f"Gasto removido com sucesso."
        }
