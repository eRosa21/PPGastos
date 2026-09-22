from fastapi import APIRouter, Depends, HTTPException
from src.infra.entities.models import Usuario
from sqlalchemy.orm import Session
from src.infra.database.database import get_db
from controllers.dependencies import catch_session
from passlib.context import CryptContext
from schemas import UsuarioSchema


auth_router = APIRouter(prefix="/auth", tags=["auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auth_router.get("/")
async def autenticar():
    return {"Mensagem": "Autenticação bem-sucedida."}


@auth_router.post("/registro")
async def registrar(usuario_schema: UsuarioSchema, session = Depends(get_db)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Email já cadastrado.")
    else:
        crypted_senha = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(nome=usuario_schema.nome, email=usuario_schema.email, senha=crypted_senha, ativo=usuario_schema.ativo)
        session.add(novo_usuario)
        session.commit()
        
        raise HTTPException(status_code=200, detail="Usuário registrado com sucesso.")
        