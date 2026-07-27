import sqlite3

def get_connection():
    conexao = sqlite3.connect('bancos_e_caixinhas_e_gastos.db')
    cursor = conexao.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute('''CREATE TABLE IF NOT EXISTS bancos (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE,
        saldo_total FLOAT NOT NULL,
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
                    is_gasto INTEGER DEFAULT 1,
                    FOREIGN KEY (id_banco) REFERENCES bancos(id)
                        ON DELETE CASCADE
                    )''')

    try:
        cursor.execute("ALTER TABLE gastos ADD COLUMN is_gasto INTEGER DEFAULT 1")
    except sqlite3.OperationalError:
        pass

    cursor.execute('''CREATE TABLE IF NOT EXISTS caixinhas (
                   id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL UNIQUE,
                   valor_reservado REAL DEFAULT 0.0,
                   id_banco INTEGER NOT NULL,
                    FOREIGN KEY (id_banco) REFERENCES bancos(id)
                        ON DELETE CASCADE
                    )''')

    cursor.execute('''INSERT OR IGNORE INTO bancos
                   (nome, saldo_total, fatura_atual) VALUES
                   ('Nubank', 0000.0, 000.0)''')

    return conexao, cursor