import sqlite3

import sqlite3

def limpar_db(nome_arquivo, nome_tabela):
    try:
        conn = sqlite3.connect(nome_arquivo)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {nome_tabela}")
        conn.commit()
        conn.close()
        print(f"✅ Tabela '{nome_tabela}' limpa no arquivo '{nome_arquivo}'")
    except sqlite3.OperationalError:
        print(f"⚠️ Aviso: Tabela '{nome_tabela}' não encontrada em '{nome_arquivo}'")

# Chamando para cada um
limpar_db('registros.db', 'registros')
limpar_db('bancos.db', 'bancos')
limpar_db('caixinhas.db', 'caixinhas')

print("\n🚀 Todos os processos de limpeza finalizados!")