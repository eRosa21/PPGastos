import sqlite3
from logica import menu
from logica import criar_caixinha

conexao = sqlite3.connect('bancos_e_caixinhas.db')
cursor = conexao.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute('''CREATE TABLE IF NOT EXISTS bancos (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE,
    saldo_total FLOAT  NOT NULL,
    fatura_atual FLOAT NOT NULL
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


conexao.commit()    

menu(conexao, cursor)
    
conexao.close()