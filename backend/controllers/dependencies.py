import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from src.infra.entities.models import Usuario
from src.infra.database.database import get_db

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
bearer_scheme = HTTPBearer(auto_error=False)

def catch_session(session: Session = Depends(get_db)):
    yield session

def verificar_token(token, session: Session = Depends(get_db)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY,ALGORITHM)
        email_usuario = dic_info.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado, verifique a data de expiração.")
    
    usuario = session.query(Usuario).filter(Usuario.email == email_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail = "Acesso inválido. Email não encontrado.")
    
    return usuario





# def verificar_token(
#     credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
#     session: Session = Depends(get_db),
# ):
#     if credentials is None:
#         raise HTTPException(status_code=401, detail="Token não informado.")

#     try:
#         dic_info = jwt.decode(
#             credentials.credentials,
#             SECRET_KEY,
#             algorithms=[ALGORITHM],
#         )
#     except JWTError:
#         raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

#     email = dic_info.get("sub")
#     if not email:
#         raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

#     usuario = session.query(Usuario).filter(Usuario.email == email).first()
#     if usuario is None:
#         raise HTTPException(status_code=401, detail="Usuário do token não encontrado.")

#     return usuario
