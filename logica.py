import sqlite3

    
def menu(conexao, cursor):
    print("O que você deseja fazer?")
    print("1 - Alterar saldo de um Banco")
    print("2 - Alterar saldo de uma Caixinha")
    print("3 - Criar uma nova Caixinha")
    escolha1 = input("Escolha (1, 2 ou 3): ")

    if(escolha1 == "1"):
        alterar_saldo_banco(conexao,cursor)
    elif(escolha1 == "2"):
        alterar_saldo_caixinha(conexao,cursor)
    elif(escolha1 == "3"):
        criar_caixinha(conexao,cursor)

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
    
    