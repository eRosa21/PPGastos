import sqlite3

conexao = sqlite3.connect('registros.db')
cursor = conexao.cursor()

cursor.execute('DELETE FROM registros')

conexao.commit()
conexao.close()

print("✅ Todos os dados foram deletados!")
print("📊 Tabela 'registros' está vazia agora")
