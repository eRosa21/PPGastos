from fastapi import APIRouter, Depends, HTTPException
from src.infra.entities.models import Usuario
from sqlalchemy.orm import Session
from src.infra.database.database import get_db


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def autenticar():
    return {"Mensagem": "Autenticação bem-sucedida."}


@auth_router.post("/registro")
async def registrar(nome:str,email: str, senha: str,db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.email == email).first()
    if usuario:
        return {"Mensagem": "Usuário já registrado."}
    else:
        novo_usuario = Usuario(nome, email, senha)
        db.add(novo_usuario)
        db.commit()
        
        return {"Mensagem": "Usuário registrado com sucesso."}