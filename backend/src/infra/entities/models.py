from datetime import date
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean, UniqueConstraint
from src.infra.database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Numeric, Integer


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
    saldo = Column("saldo", Numeric(10,2), nullable=False)
    fatura = Column("fatura", Numeric(10,2), nullable=False)
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False)
    
    def __init__(self, nome: str, usuario_id: int, saldo=0, fatura=0):
        self.nome = nome
        self.usuario_id = usuario_id
        self.saldo = saldo
        self.fatura = fatura

class Gastos(Base):
    __tablename__ = "gastos"
    
    id = Column("id", Integer, primary_key=True, index=True)
    usuario_id = Column("usuario_id", Integer, ForeignKey("usuarios.id"), nullable=False)
    nome = Column("nome", String(255), nullable=False)
    valor = Column("valor", Numeric(10,2), nullable=False)
    tipo = Column("tipo", String(255), nullable=False)
    id_banco = Column("id_banco", Integer, ForeignKey("bancos.id"), nullable=False)
    meio_pagamento = Column("meio_pagamento", String(255), nullable=True)
    dia = Column("dia", Date, nullable=False)
    numero_parcelas = Column("Numero_parcelas", Integer, nullable=False, default=1, server_default="1")

    def __init__(
        self,
        nome: str,
        valor: float,
        tipo: str,
        id_banco: int,
        usuario_id: int,
        dia: date,
        meio_pagamento: str = None,
        numero_parcelas: int = 1,
    ):
        self.usuario_id = usuario_id
        self.nome = nome
        self.valor = valor
        self.tipo = tipo
        self.id_banco = id_banco
        self.meio_pagamento = meio_pagamento
        self.dia = dia
        self.numero_parcelas = numero_parcelas

class Caixinhas(Base):
    __tablename__ = "caixinhas"
    
    id = Column("id", Integer, primary_key=True, index=True)
    nome = Column("nome", String(255), nullable=False)    
    valor = Column("valor", Numeric(10,2), nullable=False)
    id_banco = Column("id_banco", Integer, ForeignKey("bancos.id"), nullable=False)
    
    ##def __init__

class Faturas(Base):
    
    __tablename__ = "faturas"
    id = Column("id", Integer, primary_key = True, index = True)
    data_vencimento =Column("dia_vencimento", Date, nullable=False)
    data_fechamando = Column("dia_fechamento", Date, nullable=False)
    valor_total = Column("valor_total", Numeric(10,2))
    id_banco = Column("id_banco",Integer, ForeignKey("bancos.id"), nullable=False)
    mes_referencia = Column("mes", Date, nullable = False)
    pago_em = Column ("data_pagamento", Date, nullable = False)
    
    
class Parcelas(Base):
    
    __tablename__ = "parcelas"
    
    id = Column("id", Integer, primary_key =True, index = True)
    nome = Column("nome", String(255), nullable=False)
    numero_parcelas= Column("numero",Integer, nullable = False)
    valor = Column("Valor", Numeric(10,2), nullable = False)
    gasto_id = Column("gasto_id",Integer, ForeignKey("gastos.id"), nullable=False)
    fatura_id = Column("fatura_id", Integer, ForeignKey("faturas.id"), nullable= False)
    

                   