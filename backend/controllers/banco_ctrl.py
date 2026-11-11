from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from controllers.dependencies import verificar_token, catch_session
from schemas import BancoSchema
from src.infra.entities.models import Banco, Usuario

banco_router = APIRouter(prefix="/banco", tags=["banco"], dependencies= [Depends(verificar_token)])


@banco_router.post("/adicionar-banco")
async def add_banco(banco: BancoSchema, session: Session = Depends(catch_session), usuario: Usuario = Depends(verificar_token)):
    novo_banco = Banco(
        nome=banco.nome,
        usuario_id=usuario.id,
        saldo=banco.saldo,
        fatura=banco.fatura
    )
    session.add(novo_banco)
    session.commit()

    return {f"Banco {novo_banco.nome} adicionado com sucesso."}


@banco_router.delete("/remover-banco/{banco_id}")
async def remover_banco(banco_id: int, session: Session = Depends(catch_session), usuario: Usuario = Depends(verificar_token)):

    banco = session.query(Banco).filter(Banco.id == banco_id).first()

    if not banco: 
        raise HTTPException(status_code=404, detail="Banco não encontrado.")
    if usuario.id != banco.usuario_id and not usuario.admin:
        raise HTTPException(status_code=403, detail="Você não tem acesso para realizar esta remoção.")

    session.delete(banco)
    session.commit()
    return {f"Banco removido com sucesso."}