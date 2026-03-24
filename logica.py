import sqlite3

def insert_gasto(valor, categoria, data,pagamento,cartão):
    if valor <= 0:
        raise ValueError("O valor do gasto deve ser maior que zero.")
    # Aqui tem que adicionar a logica para salvar o gasto no banco de dados, tenho que aprender ainda
    else:
        print(f"Gasto registrado: R${valor:.2f}")
    
def insert_ganho(valor, categoria, data, pagamento):
    if valor <= 0:
        raise ValueError("O valor do ganho deve ser maior que zero.")
    # Aqui tem que adicionar a logica para salvar o ganho no banco de dados, tenho que aprender ainda . Não vai adicionar somente o gasto, vai adicionar todas as outras informações, como categoria, data, forma de pagamento, etc.

def registrar_gasto_usuario():
    print("\n=== Registrar Novo Gasto ===")
    valor = float(input("Digite o valor (R$): "))
    if valor <= 0:
        print("Valor inválido. O valor do gasto deve ser maior que zero.")
        return
    
    categoria = input("Digite a categoria: ")
    data = input("Digite a data (DD/MM/YYYY): ")
    pagamento = input("Forma de pagamento (Dinheiro/Débito/Crédito/Pix): ")
    cartao = input("Nome do cartão (opcional, pressione Enter para pular): ")
    
    insert_gasto(valor, categoria, data, pagamento, cartao)

if __name__ == "__main__":
    registrar_gasto_usuario()
    