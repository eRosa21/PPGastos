import sqlite3
from logica import alterar_saldo_banco

conexao = sqlite3.connect('bancos.db')
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

alterar_saldo_banco(conexao, cursor)
    
conexao.close()