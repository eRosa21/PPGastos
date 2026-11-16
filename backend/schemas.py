from datetime import date
from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

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


class MeioPagamento(str,Enum):
     debito = "débito"
     credito = "crédito"  
     
     
class GastoSchema(BaseModel):
    nome: str
    valor: Decimal
    tipo: str
    id_banco: int
    meio_pagamento: MeioPagamento
    dia: date
    numero_parcelas: int = Field(default=1, ge=1)


class BancoSchema(BaseModel):
    nome: str
    saldo: Optional[Decimal] = Field(default=0, ge=0)
    fatura: Optional[Decimal] = Field(default=0, ge=0)


