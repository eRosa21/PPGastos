import os
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from jose import jwt
from src.infra.database.database import get_db
from src.infra.entities.models import Usuario
from schemas import UsuarioSchema, LoginSchema
from controllers.dependencies import verificar_token


load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES"))

auth_router = APIRouter(prefix="/auth", tags=["auth"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def criar_token(email: str, duracao_token: timedelta | None = None):
    if duracao_token is None:
        duracao_token = timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": email, "exp": data_expiracao}
    encoded_jwt = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def autenticar_usuario(email: str, senha: str, session: Session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()
    if not usuario: 
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False
    return usuario

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
    
@auth_router.post("/login")
async def login (login_schema: LoginSchema, session: Session = Depends(get_db)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Email não encontrado ou credenciais inválidas.")
    else:
        acess_token = criar_token(usuario.email)
        refresh_token = criar_token(usuario.email, duracao_token=timedelta(days=7))
        return {
            "access-token": acess_token,
            "refresh-token": refresh_token,
            "token_type": "bearer"
        }
@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):

    access_token = criar_token(usuario.email)
    return{
            "access-token": access_token,
            "token_type": "Bearer"
        }