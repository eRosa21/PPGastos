import sqlite3

conexao = sqlite3.connect('registros.db')
cursor = conexao.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    valor FLOAT NOT NULL,
    categoria TEXT NOT NULL,
    data TEXT NOT NULL,
    pagamento TEXT NOT NULL,
    cartao TEXT NOT NULL
    )''')


conexao.commit()