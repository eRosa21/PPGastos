import sqlite3



def registrar_gasto(conexao,cursor):
    print("\n--- Registrar Gasto ---")
    print("Digite o nome do gasto:")
    nome = input("Nome: ")
    print("Digite o valor do gasto:")
    valor = float(input("Valor: R$ "))
    print("Digite a data do gasto:")
    data = input("Data: ")
    print("Digite o tipo do gasto:")
    tipo = input("Tipo: ")
    print("Digite a forma de pagamento:")
    pagamento =input('Forma de pagamento: ')
    print("Digite o ID do banco ao qual este gasto pertence (ex: 1 para o Nubank):")
    id_banco = int(input("ID do Banco: "))

    
    try:
        cursor.execute('''INSERT INTO gastos (nome, valor, data, tipo, pagamento, id_banco, is_gasto) VALUES (?, ?, ?, ?, ?, ?, 1)''', (nome, valor, data, tipo, pagamento, id_banco))
        conexao.commit()
        print(f"Gasto '{nome}' registrado com sucesso!")
    except sqlite3.IntegrityError as e:
        msg_erro = str(e).lower()
        if "foreign key" in msg_erro:
            print(f"\nErro: O banco com ID {id_banco} não existe! Verifique o ID do banco e tente de novo.")
        else:
            print(f"\nErro de integridade no banco de dados: {e}")

def criar_caixinha(conexao,cursor):
    while True:
        print("\n--- Nova Caixinha ---")
        print("Digite o nome da caixinha:")
        nome = input("Nome: ")
        print("Digite o ID do banco ao qual esta caixinha pertence (ex: 1 para o Nubank):")
        id_banco = int(input("ID do Banco: "))
        print("Digite o valor inicial da caixinha:")
        valor = float(input("Valor: R$ "))
        
        try:
            cursor.execute('''INSERT INTO caixinhas (nome, valor_reservado, id_banco) VALUES (?, ?, ?)''', (nome, valor, id_banco))
            conexao.commit()
            print(f"Caixinha '{nome}' criada com sucesso!")
            break 
            
        except sqlite3.IntegrityError as e:
            msg_erro = str(e).lower()
            if "unique" in msg_erro:
                print(f"\nErro: Já existe uma caixinha com o nome '{nome}'! Tente de novo com outro nome.")
            elif "foreign key" in msg_erro:
                print(f"\nErro: O banco com ID {id_banco} não existe! Verifique o ID do banco e tente de novo.")
            else:
                print(f"\nErro de integridade no banco de dados: {e}")
                break # Sai do loop caso seja um erro desconhecido

def alterar_saldo_banco(conexao,cursor):
    print("Insira o id do banco que você quer adicionar o valor:")
    id_busca = int(input("ID: "))
    print("Você quer adicionar ou subtrair do saldo do banco?")
    print("1 - Adicionar")
    print("2 - Subtrair")
    escolha2 = input("Escolha (1 ou 2): ")
    
    if(escolha2 == "1"):
        print("Insira o valor que você irá adicionar ao banco:")
        novo_valor = float(input("Valor: R$ "))
        print(f"R$ {novo_valor} foi adicionado ao banco")
    
    elif(escolha2 == "2"):
        print("Insira o valor que você irá subtrair do banco:")
        novo_valor = float(input("Valor: R$ "))
        novo_valor = -novo_valor 
        print(f"R$ {novo_valor} foi retirado do banco")

        
    cursor.execute('''UPDATE bancos
                   SET saldo_total = saldo_total + ?
                   WHERE id = ?''', (novo_valor, id_busca))
                   
    conexao.commit()
    dados_bancos = cursor.execute('''SELECT nome, saldo_total FROM bancos WHERE id = ?''', (id_busca,)).fetchone()
    nome_banco = dados_bancos[0]
    saldo_banco = dados_bancos[1]
    print(f"Saldo do banco {nome_banco} atualizado com sucesso!")
    print(f"saldo atual do banco {nome_banco}: R$ {saldo_banco}")

def alterar_saldo_caixinha(conexao,cursor):
    print("Escolha a caixinha em que você quer alterar o saldo")
    id_buscaC = int(input("ID:"))
    print("Você prefere adicionar ou subtrair do saldo desta caixinha?")
    print("1- Adicionar")
    print("2- Retirar")
    escolha3   = input("Escolha (1 ou 2): ")

    if(escolha3 == "1"):
        print("Insira o valor que você irá adicionar à caixinha:")
        novo_valorC = float(input("Valor: R$ "))
        print(f"R$ {novo_valorC} foi adicionado à caixinha")
    elif(escolha3 == "2"):
        print("Insira o valor que você irá subtrair da caixinha:")
        novo_valorC = float(input("Valor: R$ "))
        novo_valorC = -novo_valorC  
        print(f"R$ {novo_valorC} foi retirado da caixinha")
    
    cursor.execute('''UPDATE caixinhas
                   SET valor_reservado = valor_reservado + ?
                   WHERE id = ?''', (novo_valorC, id_buscaC))
    conexao.commit()

    dados_caixinha = cursor.execute('''SELECT nome, valor_reservado FROM caixinhas WHERE id = ?''', (id_buscaC,)).fetchone()
    nome_caixinha = dados_caixinha[0]
    saldo_caixinha = dados_caixinha[1]
    print(f"Saldo da caixinha {nome_caixinha} atualizado com sucesso!")
    print(f"saldo atual da caixinha {nome_caixinha}: R$ {saldo_caixinha}")
    conexao.commit()

def transferir_saldo(conexao, cursor):
    print("\n--- Transferir Saldo ---")
    id_origem = int(input("ID da conta de origem: "))
    id_destino = int(input("ID da conta de destino: "))
    valor = float(input("Valor: R$ "))
    
    try:
       
        with conexao:
            # 1. Verificar se a conta de origem tem saldo suficiente 
            cursor.execute("SELECT saldo_total FROM bancos WHERE id = ?", (id_origem,))
            resultado = cursor.fetchone()
            
            if resultado is None:
                print("❌ Erro: Conta de origem não encontrada.")
                return
                
            saldo_atual = resultado[0]
            
            if saldo_atual < valor:
                print("❌ Erro: Saldo insuficiente para transferência.")
                return

            cursor.execute("SELECT id FROM bancos WHERE id = ?", (id_destino,))
            resultado_destino = cursor.fetchone()
            
            if resultado_destino is None:
                print("❌ Erro: Conta de destino não encontrada.")
                return

            cursor.execute("UPDATE bancos SET saldo_total = saldo_total - ? WHERE id = ?", (valor, id_origem))
            cursor.execute("UPDATE bancos SET saldo_total = saldo_total + ? WHERE id = ?", (valor, id_destino))
            
            # Registra a movimentação no histórico de gastos como "transferência interna" (is_gasto = 0)
            from datetime import date
            data_atual = date.today().strftime("%d/%m/%Y")
            descricao = f"Transferência para conta {id_destino}"
            cursor.execute('''INSERT INTO gastos (nome, valor, data, tipo, pagamento, id_banco, is_gasto) 
                              VALUES (?, ?, ?, ?, ?, ?, 0)''', 
                           (descricao, valor, data_atual, "Transferência Interna", "Transferência", id_origem))
            
            print(f"✅ Transferência de R$ {valor} realizada com sucesso!")

    except Exception as e:
        print(f"⚠️ Erro crítico na transferência: {e}")

