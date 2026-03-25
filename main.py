import sqlite3

conexao = sqlite3.connect('bancos.db')
cursor = conexao.cursor()

cursor.execute("PRAGMA foreign_keys = ON;")

cursor.execute('''CREATE TABLE IF NOT EXISTS bancos (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    saldo_total FLOAT  NOT NULL,
    fatura_atual FLOAT NOT NULL
    )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS caixinhas (
               id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
               nome TEXT NOT NULL,     
               valor_reservado REAL DEFAULT 0.0,
               id_banco INTEGER NOT NULL,   
                FOREIGN KEY (id_banco) REFERENCES bancos(id)
                    ON DELETE CASCADE      
                )'''  )    
            
conexao.commit()    
    
conexao.close()