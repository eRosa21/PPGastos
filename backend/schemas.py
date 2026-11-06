from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    
class Config:
    from_attributes = True
    
class LoginSchema(BaseModel):
    email: str
    senha: str
    
    class Config:
        from_attributes = True

class GastoSchema(BaseModel):
    nome: str
    valor: float
    tipo: str
    id_banco: int
    meio_pagamento: Optional[str] = None


class BancoSchema(BaseModel):
    nome: str
    saldo: Optional[float] = 0 
    fatura: Optional[float] = 0
    
     
    