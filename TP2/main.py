from conexao.Conexao import Conexao
from modelos import Cliente, ItemPedido, Pedido, Endereco, FormaPagamento, Vendedor, Item

conn = Conexao("loja_virtual", "placidoneto", "placidoneto", "localhost", "5432")
conn.conectar()

# Exemplo de uso das funções
if __name__ == "__main__":

    while(True):
        #Menu com funções
        print("1 - Listar todos os pedidos feitos por um cliente específico")
        print("2 - Listar todos os itens de um pedido específico")
        print("3 - Listar todos os clientes que fizeram pedidos em um determinado intervalo de datas")
        print("4 - Listar todos os pedidos e os respectivos clientes")
        print("5 - Listar todos os itens vendidos por um vendedor específico")
        print("6 - Listar todos os pagamentos feitos em um determinado intervalo de datas")
        print("7 - Listar todos os pedidos que foram pagos com uma forma de pagamento específica")
        print("8 - Listar todos os clientes e seus respectivos endereços")
        print("9 - Listar todos os vendedores que venderam itens em um determinado intervalo de datas")
        print("10 - Listar todos os itens que estão fora de estoque")        
        print("0 - Sair")
        opcao = int(input("Digite a opção desejada: "))
        if opcao == 1:
            id_cliente = int(input("Digite o ID do Cliente desejado: "))                        
            if conn:
                pedidos = conn.obter_pedidos_por_cliente(id_cliente)
                for pedido in pedidos:
                    #print(pedido)
                    print(pedido.id, " - ", pedido.status)
        elif opcao == 2:
            id_pedido = int(input("Digite o ID do Pedido desejado: "))                        
            if conn:
                itens, itens_pedido = conn.obter_itens_por_pedido(id_pedido)
                for item in itens:
                    print(item)
        elif opcao == 3:
            print("Digite o intervalo de Datas desejado: ")                        
            data_inicio = input("Digite a data de início: ")
            data_fim = input("Digite a data de fim: ")
            if conn:
                clientes = conn.obter_clientes_por_data(data_inicio, data_fim)
                for cliente in clientes:
                    print(cliente)
        elif opcao == 0:
            break
        else:
            print("Opção inválida")