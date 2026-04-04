import sqlite3
from logica import (
    alterar_saldo_banco,
    alterar_saldo_caixinha,
    criar_caixinha,
    registrar_gasto,
    transferir_saldo
)

conexao = sqlite3.connect('bancos_e_caixinhas_e_gastos.db')
cursor = conexao.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute('''CREATE TABLE IF NOT EXISTS bancos (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    saldo_total FLOAT  NOT NULL,
    fatura_atual FLOAT NOT NULL
    )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS gastos(
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                valor FLOAT NOT NULL,
                data DATE NOT NULL,
                tipo TEXT NOT NULL,
                pagamento TEXT NOT NULL,
                id_banco INTEGER NOT NULL,
                FOREIGN KEY (id_banco) REFERENCES bancos(id)
                    ON DELETE CASCADE   
                )''')    

cursor.execute('''CREATE TABLE IF NOT EXISTS caixinhas (
               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               nome TEXT NOT NULL UNIQUE,     
               valor_reservado REAL DEFAULT 0.0,
               id_banco INTEGER NOT NULL,   
                FOREIGN KEY (id_banco) REFERENCES bancos(id)
                    ON DELETE CASCADE      
                )'''  )    

cursor.execute('''INSERT OR IGNORE INTO bancos 
               (nome, saldo_total, fatura_atual) VALUES 
               ('Nubank', 0000.0, 000.0)''')


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