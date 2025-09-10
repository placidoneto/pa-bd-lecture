import os
import sys
from typing import Optional
import psycopg2
from psycopg2 import sql

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
        # DEVE SER IMPLEMENTADO
        return None
    
    # ========================================
    # FUNCOES COM CONSULTAS SQL
    # ========================================
    
    def consulta_01_usuarios_ativos(self):
        """1. Listagem de Usuários Ativos"""
        sql = """
        SELECT id, nome, email, telefone
        FROM usuarios
        WHERE ativo = TRUE;
        """
        self.executar_consulta(sql, "1. Listagem de Usuários Ativos")
    
    def consulta_02_produtos_categoria(self):
        
        sql = """
        """
        self.executar_consulta(sql, "DESCRICAO DA CONSULTA")
    
    def consulta_03_pedidos_status(self):
        
        sql = """
        """
        self.executar_consulta(sql, "DESCRICAO DA CONSULTA")
    
    def consulta_04_estoque_baixo(self):
        
        sql = """
        """
        self.executar_consulta(sql, "DESCRICAO DA CONSULTA")
    
    def consulta_05_pedidos_recentes(self):
        
        sql = """
        """
        self.executar_consulta(sql, "DESCRICAO DA CONSULTA")
    
    def consulta_06_produtos_caros_categoria(self):
        
        sql = """
        """
        self.executar_consulta(sql, "DESCRICAO DA CONSULTA")
    
    def consulta_07_contatos_incompletos(self):
        
        sql = """
        """
        self.executar_consulta(sql, "DESCRICAO DA CONSULTA")
    
    def consulta_08_pedidos_enviados(self):
        
        sql = """
        """
        self.executar_consulta(sql, "DESCRICAO DA CONSULTA")
    
    def consulta_09_detalhamento_pedido(self):
        
        sql = """
        """
        self.executar_consulta(sql, "DESCRICAO DA CONSULTA")
    
    def consulta_10_ranking_produtos(self):
    
        sql = """
        """
        self.executar_consulta(sql, "DESCRICAO DA CONSULTA")
    
    def consulta_11_clientes_sem_compras(self):
        
        sql = """
        """
        self.executar_consulta(sql, "DESCRICAO DA CONSULTA")
    
    def consulta_12_estatisticas_cliente(self):
        
        sql = """
        """
        self.executar_consulta(sql, "DESCRICAO DA CONSULTA")
    
    def consulta_13_relatorio_mensal(self):
        
        sql = """
        """
        self.executar_consulta(sql, "DESCRICAO DA CONSULTA")
    
    def consulta_14_produtos_nao_vendidos(self):
        
        sql = """
        """
        self.executar_consulta(sql, "DESCRICAO DA CONSULTA")
    
    def consulta_15_ticket_medio_categoria(self):
        
        sql = """
        """
        self.executar_consulta(sql, "DESCRICAO DA CONSULTA")
    
    # ========================================
    # MENUS 
    # ======================================== 
    def menu_exercicios(self):
        """MENU"""
        while True:            
            print("=" * 40)
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
            print("0. Voltar ao Menu Principal")
            print("=" * 40)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.consulta_01_usuarios_ativos()
            elif opcao == "2":
                self.consulta_02_produtos_categoria()
            elif opcao == "3":
                self.consulta_03_pedidos_status()
            elif opcao == "4":
                self.consulta_04_estoque_baixo()
            elif opcao == "5":
                self.consulta_05_pedidos_recentes()
            elif opcao == "6":
                self.consulta_06_produtos_caros_categoria()
            elif opcao == "7":
                self.consulta_07_contatos_incompletos()
            elif opcao == "8":
                self.consulta_08_pedidos_enviados()
            elif opcao == "9":
                self.consulta_09_detalhamento_pedido()
            elif opcao == "10":
                self.consulta_10_ranking_produtos()
            elif opcao == "11":
                self.consulta_11_clientes_sem_compras()
            elif opcao == "12":
                self.consulta_12_estatisticas_cliente()
            elif opcao == "13":
                self.consulta_13_relatorio_mensal()
            elif opcao == "14":
                self.consulta_14_produtos_nao_vendidos()
            elif opcao == "15":
                self.consulta_15_ticket_medio_categoria()                
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
            
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
