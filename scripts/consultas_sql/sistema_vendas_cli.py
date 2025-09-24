import os
import sys
from typing import Optional
import psycopg2
from psycopg2 import sql
#import tabulate

DB_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'postgres',
    'database': 'sistema_vendas'
}

class SistemaVendasCLI:
    def __init__(self):
        self.conexao = None
        print("Sistema de Vendas - CLI Inicializado")
        print("=" * 50)
    
    def conectar_banco(self):
        try:
            self.conexao = psycopg2.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password'],
                database=DB_CONFIG['database']
            )
            
            print("Conectando ao banco PostgreSQL...")
            #self.conexao = psycopg2.connect(**pg_config)
            self.conexao.autocommit = True
            print("Conexão estabelecida com sucesso!")
            return True
        except psycopg2.Error as e:
            print(f"Erro ao conectar ao PostgreSQL: {e}")
            return False
        except Exception as e:
            print(f"Erro inesperado: {e}")
            return False
        return True
    
    def desconectar_banco(self):
        if self.conexao:
            self.conexao.close()
            print("Conexão com o banco de dados encerrada.")
                        
    def executar_consulta(self, sql: str, descricao: str) -> None:
        """Executa uma consulta SQL e exibe os resultados formatados"""
        print(f"\nExecutando: {descricao}")
        print("=" * 60)
        print(f"SQL: {sql.strip()}")
        print("=" * 60)
        
        try:
            cursor = self.conexao.cursor()
            cursor.execute(sql)
            resultados = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description]
            
            #table = tabulate.tabulate(resultados, headers=colunas, tablefmt="grid")
            #print(table)
            
            if resultados:
                # Exibir cabeçalhos
                print("\n Resultados:")
                
                # Cria o cabeçalho da tabela formatando cada nome de coluna
                #  Aplica formatação de 20 caracteres alinhados à esquerda (:<20)
                # com 20 caracteres alinhados à esquerda e separados por " | "
                header = " | ".join(f"{col:<20}" for col in colunas)
                print(header)
                print("-" * len(header))
                
                # Exibir dados
                for linha in resultados:
                    # Formata cada linha de resultado criando uma string onde:
                    #  Converte cada valor da linha para string com str(valor)
                    #  Aplica formatação de 20 caracteres alinhados à esquerda (:<20)
                    #  Une todos os valores formatados com " | " como separador
                    #  Resultado: colunas alinhadas visualmente em formato tabular
                    row = " | ".join(f"{str(valor):<20}" for valor in linha)
                    
                    print(row)
                    
                print(f"\nTotal de registros encontrados: {len(resultados)}")
                
            else:
                print("\nNenhum registro encontrado.")
                
        except psycopg2.Error as e:
            print(f"\nErro na consulta SQL: {e}")
        except Exception as e:
            print(f"\nErro inesperado: {e}")
        finally:
            if 'cursor' in locals():
                cursor.close()
        
        print("\nConsulta finalizada!")
    
    # ========================================
    # FUNCOES COM CONSULTAS SQL
    # ========================================
    
    def consulta_01_usuarios_ativos(self):
        """1. Listagem de Usuários Ativos"""
        sql = """
        SELECT id_usuario, nome, email, telefone
        FROM usuario
        WHERE ativo = TRUE
        ORDER BY nome;
        """
        self.executar_consulta(sql, "1. Listagem de Usuários Ativos")
    
    def consulta_02_produtos_categoria(self):
        """2. Catálogo de Produtos por Categoria"""
        sql = """
        SELECT nome, preco, quantidade_estoque, categoria
        FROM produto
        WHERE categoria = 'Informática' AND ativo = TRUE
        ORDER BY preco ASC;
        """
        self.executar_consulta(sql, "2. Catálogo de Produtos por Categoria")
    
    def consulta_03_pedidos_status(self):
        """3. Contagem de Pedidos por Status"""
        sql = """
        SELECT status_pedido, COUNT(*) as total_pedidos
        FROM pedido
        GROUP BY status_pedido
        ORDER BY total_pedidos DESC;
        """
        self.executar_consulta(sql, "3. Contagem de Pedidos por Status")
    
    def consulta_04_estoque_baixo(self):
        """4. Alerta de Estoque Baixo"""
        sql = """
        SELECT nome, quantidade_estoque, categoria
        FROM produto
        WHERE quantidade_estoque < 30 AND ativo = TRUE
        ORDER BY quantidade_estoque ASC;
        """
        self.executar_consulta(sql, "4. Alerta de Estoque Baixo")
    
    def consulta_05_pedidos_recentes(self):
        """5. Histórico de Pedidos Recentes"""
        sql = """
        SELECT id_pedido, data_pedido, valor_total, status_pedido
        FROM pedido
        WHERE data_pedido >= CURRENT_DATE - INTERVAL '60 days'
        ORDER BY data_pedido DESC;
        """
        self.executar_consulta(sql, "5. Histórico de Pedidos Recentes")
    
    def consulta_06_produtos_caros_categoria(self):
        """6. Produtos Mais Caros por Categoria"""
        sql = """
        SELECT DISTINCT ON (categoria) categoria, nome, preco
        FROM produto
        WHERE ativo = TRUE
        ORDER BY categoria, preco ASC;
        """
        self.executar_consulta(sql, "6. Produtos Mais Caros por Categoria")
    
    def consulta_07_contatos_incompletos(self):
        """7. Clientes com Dados de Contato Incompletos"""
        sql = """
        SELECT id_usuario, nome, email
        FROM usuario
        WHERE ativo = TRUE AND (telefone IS NULL OR telefone = '')
        ORDER BY nome;
        """
        self.executar_consulta(sql, "7. Clientes com Dados de Contato Incompletos")
    
    def consulta_08_pedidos_enviados(self):
        """8. Pedidos Pendentes de Entrega"""
        sql = """
        SELECT p.id_pedido, u.nome as cliente, u.email, p.endereco_entrega, p.data_pedido
        FROM pedido p
        INNER JOIN usuario u ON p.id_usuario = u.id_usuario
        WHERE p.status_pedido = 'enviado'
        ORDER BY p.data_pedido;
        """
        self.executar_consulta(sql, "8. Pedidos Pendentes de Entrega")
    
    def consulta_09_detalhamento_pedido(self):
        """9. Detalhamento Completo de Pedidos"""
        sql = """
        SELECT 
            p.id_pedido,
            u.nome as cliente,
            u.email,
            p.data_pedido,
            p.status_pedido,
            pr.nome as produto,
            ip.quantidade,
            ip.preco_unitario,
            ip.subtotal
        FROM pedido p
        INNER JOIN usuario u ON p.id_usuario = u.id_usuario
        INNER JOIN itens_pedido ip ON p.id_pedido = ip.id_pedido
        INNER JOIN produto pr ON ip.id_produto = pr.id_produto
        WHERE p.id_pedido = 1
        ORDER BY pr.nome;
        """
        self.executar_consulta(sql, "9. Detalhamento Completo de Pedidos")
    
    def consulta_10_ranking_produtos(self):
        """10. Ranking dos Produtos Mais Vendidos"""
        sql = """
        SELECT 
            pr.nome,
            pr.categoria,
            SUM(ip.quantidade) as total_vendido
        FROM produto pr
        INNER JOIN itens_pedido ip ON pr.id_produto = ip.id_produto
        INNER JOIN pedido p ON ip.id_pedido = p.id_pedido
        WHERE p.status_pedido != 'cancelado'
        GROUP BY pr.id_produto, pr.nome, pr.categoria
        ORDER BY total_vendido DESC;
        """
        self.executar_consulta(sql, "10. Ranking dos Produtos Mais Vendidos")
    
    def consulta_11_clientes_sem_compras(self):
        """11. Análise de Clientes Sem Compras"""
        sql = """
        SELECT u.id_usuario, u.nome, u.email, u.data_cadastro
        FROM usuario u
        LEFT JOIN pedido p ON u.id_usuario = p.id_usuario
        WHERE p.id_usuario IS NULL AND u.ativo = TRUE
        ORDER BY u.data_cadastro DESC;
        """
        self.executar_consulta(sql, "11. Análise de Clientes Sem Compras")
    
    def consulta_12_estatisticas_cliente(self):
        """12. Estatísticas de Compras por Cliente"""
        sql = """
        SELECT 
            u.nome,
            COUNT(p.id_pedido) as total_pedidos,
            ROUND(AVG(p.valor_total), 2) as valor_medio,
            ROUND(SUM(p.valor_total), 2) as valor_total_gasto
        FROM usuario u
        INNER JOIN pedido p ON u.id_usuario = p.id_usuario
        WHERE p.status_pedido != 'cancelado'
        GROUP BY u.id_usuario, u.nome
        HAVING COUNT(p.id_pedido) > 0
        ORDER BY valor_total_gasto DESC;
        """
        self.executar_consulta(sql, "12. Estatísticas de Compras por Cliente")
    
    def consulta_13_relatorio_mensal(self):
        """13. Relatório Mensal de Vendas"""
        sql = """
        SELECT 
            EXTRACT(YEAR FROM p.data_pedido) as ano,
            EXTRACT(MONTH FROM p.data_pedido) as mes,
            COUNT(DISTINCT p.id_pedido) as quantidade_pedidos,
            COUNT(DISTINCT ip.id_produto) as produtos_diferentes,
            ROUND(SUM(p.valor_total), 2) as faturamento_total
        FROM pedido p
        INNER JOIN itens_pedido ip ON p.id_pedido = ip.id_pedido
        WHERE p.status_pedido != 'cancelado'
        GROUP BY EXTRACT(YEAR FROM p.data_pedido), EXTRACT(MONTH FROM p.data_pedido)
        ORDER BY ano DESC, mes DESC;
        """
        self.executar_consulta(sql, "13. Relatório Mensal de Vendas")
    
    def consulta_14_produtos_nao_vendidos(self):
        """14. Produtos que Nunca Foram Vendidos"""
        sql = """
        SELECT pr.id_produto, pr.nome, pr.categoria, pr.preco, pr.quantidade_estoque
        FROM produto pr
        LEFT JOIN itens_pedido ip ON pr.id_produto = ip.id_produto
        WHERE ip.id_produto IS NULL AND pr.ativo = TRUE
        ORDER BY pr.categoria, pr.nome;
        """
        self.executar_consulta(sql, "14. Produtos que Nunca Foram Vendidos")
    
    def consulta_15_ticket_medio_categoria(self):
        """15. Análise de Ticket Médio por Categoria"""
        sql = """
        SELECT 
            pr.categoria,
            COUNT(DISTINCT ip.id_pedido) as pedidos_categoria,
            ROUND(AVG(ip.subtotal), 2) as ticket_medio
        FROM produto pr
        INNER JOIN itens_pedido ip ON pr.id_produto = ip.id_produto
        INNER JOIN pedido p ON ip.id_pedido = p.id_pedido
        WHERE p.status_pedido != 'cancelado'
        GROUP BY pr.categoria
        ORDER BY ticket_medio DESC;
        """
        self.executar_consulta(sql, "15. Análise de Ticket Médio por Categoria")
    
    def limpar_tela(self):
        """Limpa a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    # ========================================
    # MENUS 
    # ======================================== 
    def menu_exercicios(self):
        """Menu principal com todas as consultas"""
        while True:
            self.limpar_tela()
            print("SISTEMA DE VENDAS - CONSULTAS SQL")
            print("=" * 50)            
            print("1. Listagem de Usuários Ativos")
            print("2. Catálogo de Produtos por Categoria")
            print("3. Contagem de Pedidos por Status")
            print("4. Alerta de Estoque Baixo")
            print("5. Histórico de Pedidos Recentes")
            print("6. Produtos Mais Caros por Categoria")
            print("7. Clientes com Dados Incompletos")
            print("8. Pedidos Pendentes de Entrega")
            print("9. Detalhamento Completo de Pedidos")
            print("10. Ranking dos Produtos Mais Vendidos")
            print("11. Análise de Clientes Sem Compras")
            print("12. Estatísticas de Compras por Cliente")
            print("13. Relatório Mensal de Vendas")
            print("14. Produtos que Nunca Foram Vendidos")
            print("15. Análise de Ticket Médio por Categoria")            
            print("")
            print("0. Sair do Sistema")
            print("=" * 50)
            
            opcao = input("Escolha uma opção (0-15): ").strip()
            
            funcoes = {
                "1": self.consulta_01_usuarios_ativos,
                "2": self.consulta_02_produtos_categoria,
                "3": self.consulta_03_pedidos_status,
                "4": self.consulta_04_estoque_baixo,
                "5": self.consulta_05_pedidos_recentes,
                "6": self.consulta_06_produtos_caros_categoria,
                "7": self.consulta_07_contatos_incompletos,
                "8": self.consulta_08_pedidos_enviados,
                "9": self.consulta_09_detalhamento_pedido,
                "10": self.consulta_10_ranking_produtos,
                "11": self.consulta_11_clientes_sem_compras,
                "12": self.consulta_12_estatisticas_cliente,
                "13": self.consulta_13_relatorio_mensal,
                "14": self.consulta_14_produtos_nao_vendidos,
                "15": self.consulta_15_ticket_medio_categoria
            }
            
            if opcao == "0":
                print("\n Encerrando o sistema...")
                break
            elif opcao in funcoes:
                funcoes[opcao]()
            else:
                print("\nOpção inválida! Escolha um número de 0 a 15.")
            
            input("\nPressione ENTER para continuar...")

def main():
    cli = SistemaVendasCLI()
    if cli.conectar_banco():
        try:
            cli.menu_exercicios()
        finally:
            cli.desconectar_banco()
    else:
        print("Falha ao conectar ao banco de dados.")
        sys.exit(1)

if __name__ == "__main__":
    main()
