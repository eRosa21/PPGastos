from datetime import date
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean, UniqueConstraint
from src.infra.database.database import Base
from sqlalchemy.orm import relationship

class Usuario(Base):
    __tablename__ = "usuarios"
    __table_args__ = (UniqueConstraint("email", name="uq_usuarios_email"),)
    
    id = Column("id", Integer, primary_key=True, index=True)
    nome = Column("nome", String(100), nullable=False)  
    email = Column("email", String(150), nullable=False) 
    senha = Column("senha", String(255), nullable=False) 
    ativo = Column('ativo', Boolean)
    admin = Column('admin', Boolean, default=False) 

    def __init__(self, nome: str, email: str, senha: str, ativo = True, admin = False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin  
    
class Banco(Base):
    __tablename__ = "bancos"
    
    id = Column("id", Integer, primary_key=True, index=True)
    nome = Column("banco", String(100), nullable=False) 
    saldo = Column("saldo", Float, nullable=False)
    fatura = Column("fatura", Float, nullable=False)
    usuario = Column("usuario", Integer, ForeignKey("usuarios.id"), nullable=False)
    
    def __init__(self, nome: str, usuario: int, saldo=0, fatura=0):
        self.nome = nome
        self.usuario = usuario
        self.saldo = saldo
        self.fatura = fatura

class Gastos(Base):
    __tablename__ = "gastos"
    
    id = Column("id", Integer, primary_key=True, index=True)
    usuario = Column("usuario", Integer, ForeignKey("usuarios.id"), nullable=False)
    nome = Column("nome", String(255), nullable=False)
    valor = Column("valor", Float, nullable=False)
    tipo = Column("tipo", String(255), nullable=False)
    id_banco = Column("id_banco", Integer, ForeignKey("bancos.id"), nullable=False)
    meio_pagamento = Column("meio_pagamento", String(255), nullable=True)
    dia = Column("dia", Date, nullable=False)

    def __init__(
        self,
        nome: str,
        valor: float,
        tipo: str,
        id_banco: int,
        usuario: int,
        dia: date,
        meio_pagamento: str = None,
    ):
        self.usuario = usuario
        self.nome = nome
        self.valor = valor
        self.tipo = tipo
        self.id_banco = id_banco
        self.meio_pagamento = meio_pagamento
        self.dia = dia

class Caixinhas(Base):
    __tablename__ = "caixinhas"
    
    id = Column("id", Integer, primary_key=True, index=True)
    nome = Column("nome", String(255), nullable=False)    
    valor = Column("valor", Float, nullable=False)
    id_banco = Column("id_banco", Integer, ForeignKey("bancos.id"), nullable=False)

#class MeioPagamento(Base):
