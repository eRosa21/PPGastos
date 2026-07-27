import sqlite3
from models import get_connection
from logica import (
    alterar_saldo_banco,
    alterar_saldo_caixinha,
    criar_caixinha,
    registrar_gasto,
    transferir_saldo
)

conexao, cursor = get_connection()

def menu(conexao, cursor):
    print("O que você deseja fazer?")
    print("1 - Alterar saldo de um Banco")
    print("2 - Alterar saldo de uma Caixinha")
    print("3 - Criar uma nova Caixinha")
    print("4 - Registrar um Gasto")
    print("5 - Transferir saldo entre bancos")
    escolha1 = input("Escolha (1, 2, 3, 4 ou 5): ")

    if(escolha1 == "1"):
        alterar_saldo_banco(conexao, cursor)
    elif(escolha1 == "2"):
        alterar_saldo_caixinha(conexao, cursor)
    elif(escolha1 == "3"):
        criar_caixinha(conexao, cursor)
    elif(escolha1 == "4"):
        registrar_gasto(conexao, cursor)
    elif(escolha1 == "5"):
        transferir_saldo(conexao, cursor)
    else:
        print("Opção inválida!")

menu(conexao, cursor)
conexao.close()