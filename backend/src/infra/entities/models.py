from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from database.database import Base
from sqlalchemy.orm import relationship
#from sqlalchemy_utils.types import ChoiceType

class Banco(Base):
    __tablename__ = "bancos"
    id = Column("id",Integer, primary_key=True, index=True)
    nome = Column("banco",String, nullable=False)
    saldo = Column("saldo",Float, nullable=False)
    fatura = Column("fatura",Float, nullable=False)
    
    def __init__(self, nome:str, saldo=0, fatura=0):
        self.nome = nome
        self.saldo = saldo
        self.fatura = fatura

class Gastos(Base):
    __tablename__ = "gastos"
    
    ##TIPO_GASTOS = (
      #  ("débito", "débito"),
       # ("crédito", "crédito"),
        
   # )
    
    id = Column("id",Integer, primary_key=True, index=True)
    nome = Column("nome",String, nullable=False)
    valor = Column("valor",Float, nullable=False)
    tipo = Column("tipo",String, nullable=False)
    id_banco = Column("id_banco",Integer, ForeignKey("bancos.id"), nullable=False)
    
    def __init__ (self, nome:str, valor:float, tipo:str, id_banco:int):
        self.nome = nome
        self.valor = valor
        self.tipo = tipo
        self.id_banco = id_banco

class Caixinhas(Base):
    __tablename__ = "caixinhas"
    id = Column("id",Integer, primary_key=True, index=True)
    nome = Column("nome",String, nullable=False)    
    valor = Column("valor",Float, nullable=False)
    id_banco = Column("id_banco",Integer, ForeignKey("bancos.id"), nullable=False)
