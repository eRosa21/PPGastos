import sqlite3

# def insert_gasto(valor, categoria, data,pagamento,cartão):
#     if valor <= 0:
#         raise ValueError("O valor do gasto deve ser maior que zero.")
#     # Aqui tem que adicionar a logica para salvar o gasto no banco de dados, tenho que aprender ainda
#     else:
#         print(f"Gasto registrado: R${valor:.2f}")
    
# def insert_ganho(valor, categoria, data, pagamento):
#     if valor <= 0:
#         raise ValueError("O valor do ganho deve ser maior que zero.")
#     # Aqui tem que adicionar a logica para salvar o ganho no banco de dados, tenho que aprender ainda . Não vai adicionar somente o gasto, vai adicionar todas as outras informações, como categoria, data, forma de pagamento, etc.

# def registrar_gasto_usuario():
#     print("\n=== Registrar Novo Gasto ===")
#     valor = float(input("Digite o valor (R$): "))
#     if valor <= 0:
#         print("Valor inválido. O valor do gasto deve ser maior que zero.")
#         return
    
#     categoria = input("Digite a categoria: ")
#     data = input("Digite a data (DD/MM/YYYY): ")
#     pagamento = input("Forma de pagamento (Dinheiro/Débito/Crédito/Pix): ")
#     cartao = input("Nome do cartão (opcional, pressione Enter para pular): ")
    
#     insert_gasto(valor, categoria, data, pagamento, cartao)

# if __name__ == "__main__":
#     registrar_gasto_usuario()
    
    

def alterar_saldo_banco(conexao,cursor):
    print("Insira o id do banco que você quer adicionar o valor:")
    id_busca = int(input("ID: "))
    print("Você quer adicionar ou subtrair do saldo do banco?")
    print("1 - Adicionar")
    print("2 - Subtrair")
    escolha = input("Escolha (1 ou 2): ")
    
    if(escolha == "1"):
        print("Insira o valor que você irá adicionar ao banco:")
        novo_valor = float(input("Valor: R$ "))
    elif(escolha == "2"):
        print("Insira o valor que você irá subtrair do banco:")
        novo_valor = float(input("Valor: R$ "))
        novo_valor = -novo_valor  # Tornar o valor negativo para subtração
    
    cursor.execute('''UPDATE bancos
                   SET saldo_total = saldo_total + ?
                   WHERE id = ?''', (novo_valor, id_busca))
    conexao.commit()
    print(f"Saldo do banco ID {id_busca} atualizado com sucesso!")

    