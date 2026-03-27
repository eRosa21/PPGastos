import unittest
import sqlite3

class TestIntegridadeBanco(unittest.TestCase):

    def setUp(self):
        """Executa antes de CADA teste: cria um banco zerado na memória"""
        self.conexao = sqlite3.connect(':memory:')
        self.cursor = self.conexao.cursor()
        self.cursor.execute("PRAGMA foreign_keys = ON;")
        
        # Criando as tabelas necessárias para o teste
        self.cursor.execute('''CREATE TABLE bancos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL)''')
            
        self.cursor.execute('''CREATE TABLE caixinhas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            id_banco INTEGER NOT NULL,
            FOREIGN KEY (id_banco) REFERENCES bancos(id) ON DELETE CASCADE)''')

    def tearDown(self):
        """Executa após cada teste: fecha a conexão"""
        self.conexao.close()

    def test_chave_estrangeira_invalida(self):
        """Teste: Tentar inserir caixinha sem banco existente deve dar erro"""
        with self.assertRaises(sqlite3.IntegrityError):
            #Inserindo o ID de um banco que não existe
            self.cursor.execute("INSERT INTO caixinhas (nome, id_banco) VALUES ('Teste', 999)")

    def test_delete_cascade(self):
        """Teste: Deletar banco deve apagar as caixinhas vinculadas"""
        # 1. Inserimos um banco e uma caixinha
        self.cursor.execute("INSERT INTO bancos (nome) VALUES ('Nubank')")
        id_banco = self.cursor.lastrowid
        self.cursor.execute("INSERT INTO caixinhas (nome, id_banco) VALUES ('Reserva', ?)", (id_banco,))
        
        # 2. Deletamos o banco
        self.cursor.execute("DELETE FROM bancos WHERE id = ?", (id_banco,))
        
        # 3. Verificamos se a caixinha sumiu (Assert)
        self.cursor.execute("SELECT * FROM caixinhas")
        resultado = self.cursor.fetchall()
        self.assertEqual(len(resultado), 0, "A caixinha deveria ter sido deletada em cascata!")

if __name__ == '__main__':
    unittest.main()