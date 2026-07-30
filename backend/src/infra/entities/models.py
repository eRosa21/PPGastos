from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from database.database import Base

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
    id = Column("id",Integer, primary_key=True, index=True)

class Caixinhas(Base):
    __tablename__ = "caixinhas"
    id = Column("id",Integer, primary_key=True, index=True)
    
