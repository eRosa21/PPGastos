import pytest
from sqlalchemy.orm import Session

from src.infra.database.database import SessionLocal
from src.infra.entities.models import Banco, Gastos

GASTO = dict(nome="mercado", tipo="alimentacao", id_banco=1, dia="2026-11-01")


def criar_banco(client, auth, saldo=1000, fatura=0):
    client.post("/banco/adicionar-banco",
                json={"nome": "B", "saldo": saldo, "fatura": fatura}, headers=auth)


def ler_banco():
    with SessionLocal() as s:
        b = s.query(Banco).first()
        return b.saldo, b.fatura

def adicionar(client, auth, valor, meio):
    return client.post("/alter/adicionar-gasto",
                       json={**GASTO, "valor": valor, "meio_pagamento": meio}, headers=auth)


def test_debito_adicionar_e_remover_volta_ao_inicial(client, auth):
    criar_banco(client, auth)
    adicionar(client, auth, 100, "débito")
    assert ler_banco() == (900, 0)

    r = client.delete("/alter/remover-gasto/1", headers=auth)

    assert r.status_code == 200
    assert ler_banco() == (1000, 0)


def test_credito_adicionar_e_remover_volta_ao_inicial(client, auth):
    criar_banco(client, auth)
    adicionar(client, auth, 40, "crédito")
    assert ler_banco() == (1000, 40)

    r = client.delete("/alter/remover-gasto/1", headers=auth)

    assert r.status_code == 200
    assert ler_banco() == (1000, 0)


def test_remover_gasto_inexistente_da_404(client, auth):
    assert client.delete("/alter/remover-gasto/999", headers=auth).status_code == 404


def test_falha_no_meio_da_remocao_nao_altera_o_saldo(client, auth, monkeypatch):
    criar_banco(client, auth)
    adicionar(client, auth, 100, "débito")          # saldo 900

    def quebra(self, obj):
        raise RuntimeError("falha simulada")
    monkeypatch.setattr(Session, "delete", quebra)  # o UPDATE já rodou, o delete falha

    with pytest.raises(RuntimeError):
        client.delete("/alter/remover-gasto/1", headers=auth)

    monkeypatch.undo()
    assert ler_banco() == (900, 0)                  
    with SessionLocal() as s:
        assert s.query(Gastos).count() == 1         

def test_remover_credito_com_fatura_menor_que_o_gasto_da_409_e_mantem_o_gasto(client, auth):
    criar_banco(client, auth)
    adicionar(client, auth, 40, "crédito")           # fatura 40
    with SessionLocal() as s:                         # simula "fatura paga": fica 10
        s.query(Banco).update({"fatura": 10}); s.commit()

    r = client.delete("/alter/remover-gasto/1", headers=auth)

    assert r.status_code == 409
    with SessionLocal() as s:
        assert s.query(Gastos).count() == 1           # o gasto NÃO pode ter sido apagado