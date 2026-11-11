from datetime import date
from pydantic import BaseModel, Field
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
    valor: float = Field(ge=0)
    tipo: str
    id_banco: int
    meio_pagamento: Optional[str] = None
    dia: date


class BancoSchema(BaseModel):
    nome: str
    saldo: Optional[float] = Field(default=0, ge=0)
    fatura: Optional[float] = Field(default=0, ge=0)

# class MeioPagamento(str,Enum):
#     debito: "débito"
#     credito: "crédito"  
