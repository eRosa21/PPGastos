import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.infra.entities.models import Usuario
from src.infra.database.database import get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="/auth/login-form")

def catch_session(session: Session = Depends(get_db)):
    yield session

def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(get_db)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado, verifique a data de expiração.")

    email_usuario = dic_info.get("sub")
    if not isinstance(email_usuario, str) or not email_usuario:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")
    
    usuario = session.query(Usuario).filter(Usuario.email == email_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail = "Acesso inválido. Email não encontrado.")
    
    return usuario
