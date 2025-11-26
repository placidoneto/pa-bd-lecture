#!/usr/bin/env python3
"""
CLI para testar endpoints da API de autenticação JWT
"""

import json
import requests
import os
from typing import Dict, Optional

# Cores para terminal
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class APITester:
    def __init__(self):
        self.base_url = "http://localhost:8000/api"
        self.access_token = None
        self.refresh_token = None
        self.test_data = self.load_test_data()

    def load_test_data(self) -> Dict:
        """Carrega dados de teste do arquivo JSON"""
        try:
            with open('test_data.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"{Colors.FAIL}Erro: Arquivo test_data.json não encontrado!{Colors.ENDC}")
            return {"usuarios_para_registro": [], "endpoints": {}}

    def print_header(self, text: str):
        """Imprime cabeçalho formatado"""
        print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")

    def print_response(self, response: requests.Response):
        """Imprime resposta formatada"""
        print(f"\n{Colors.OKBLUE}Status Code: {response.status_code}{Colors.ENDC}")
        try:
            data = response.json()
            print(f"{Colors.OKCYAN}Response:{Colors.ENDC}")
            print(json.dumps(data, indent=2, ensure_ascii=False))
        except json.JSONDecodeError:
            print(f"{Colors.WARNING}Response (text): {response.text}{Colors.ENDC}")

    def registrar_usuario(self, index: Optional[int] = None):
        """Registra um usuário"""
        usuarios = self.test_data.get("usuarios_para_registro", [])

        if not usuarios:
            print(f"{Colors.FAIL}Nenhum usuário disponível para registro!{Colors.ENDC}")
            return

        if index is None:
            print(f"\n{Colors.OKGREEN}Usuários disponíveis:{Colors.ENDC}")
            for i, user in enumerate(usuarios, 1):
                print(f"{i}. {user['username']} ({user['first_name']} {user['last_name']}) - {user['tipo_perfil']}")

            try:
                choice = int(input(f"\n{Colors.OKCYAN}Escolha um usuário (1-{len(usuarios)}): {Colors.ENDC}"))
                if 1 <= choice <= len(usuarios):
                    index = choice - 1
                else:
                    print(f"{Colors.FAIL}Opção inválida!{Colors.ENDC}")
                    return
            except ValueError:
                print(f"{Colors.FAIL}Entrada inválida!{Colors.ENDC}")
                return

        user_data = usuarios[index]

        print(f"\n{Colors.OKGREEN}Registrando usuário: {user_data['username']}{Colors.ENDC}")

        try:
            response = requests.post(
                f"{self.base_url}/registro/",
                json=user_data,
                headers={"Content-Type": "application/json"}
            )

            self.print_response(response)

            if response.status_code == 201:
                data = response.json()
                if 'tokens' in data:
                    self.access_token = data['tokens']['access']
                    self.refresh_token = data['tokens']['refresh']
                    print(f"\n{Colors.OKGREEN}✓ Tokens salvos automaticamente!{Colors.ENDC}")

        except requests.exceptions.RequestException as e:
            print(f"{Colors.FAIL}Erro na requisição: {e}{Colors.ENDC}")

    def registrar_todos_usuarios(self):
        """Registra todos os usuários do arquivo de teste"""
        usuarios = self.test_data.get("usuarios_para_registro", [])

        print(f"\n{Colors.OKGREEN}Registrando {len(usuarios)} usuários...{Colors.ENDC}\n")

        for i, user_data in enumerate(usuarios):
            print(f"{Colors.OKCYAN}[{i+1}/{len(usuarios)}] Registrando: {user_data['username']}{Colors.ENDC}")

            try:
                response = requests.post(
                    f"{self.base_url}/registro/",
                    json=user_data,
                    headers={"Content-Type": "application/json"}
                )

                if response.status_code == 201:
                    print(f"{Colors.OKGREEN}✓ Sucesso!{Colors.ENDC}")
                    # Salva tokens do primeiro usuário
                    if i == 0:
                        data = response.json()
                        if 'tokens' in data:
                            self.access_token = data['tokens']['access']
                            self.refresh_token = data['tokens']['refresh']
                else:
                    print(f"{Colors.FAIL}✗ Falhou (Status: {response.status_code}){Colors.ENDC}")
                    print(f"  {response.text[:100]}")

            except requests.exceptions.RequestException as e:
                print(f"{Colors.FAIL}✗ Erro: {e}{Colors.ENDC}")

        print(f"\n{Colors.OKGREEN}Processo concluído!{Colors.ENDC}")

    def fazer_login(self):
        """Faz login com um usuário"""
        print(f"\n{Colors.OKGREEN}Login{Colors.ENDC}")
        username = input(f"{Colors.OKCYAN}Username: {Colors.ENDC}").strip()
        password = input(f"{Colors.OKCYAN}Password: {Colors.ENDC}").strip()

        if not username or not password:
            print(f"{Colors.FAIL}Username e password são obrigatórios!{Colors.ENDC}")
            return

        login_data = {
            "username": username,
            "password": password
        }

        try:
            response = requests.post(
                f"{self.base_url}/login/",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )

            self.print_response(response)

            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access')
                self.refresh_token = data.get('refresh')
                print(f"\n{Colors.OKGREEN}✓ Tokens salvos automaticamente!{Colors.ENDC}")

        except requests.exceptions.RequestException as e:
            print(f"{Colors.FAIL}Erro na requisição: {e}{Colors.ENDC}")

    def obter_usuario_atual(self):
        """Obtém dados do usuário autenticado"""
        if not self.access_token:
            print(f"{Colors.FAIL}Você precisa fazer login primeiro!{Colors.ENDC}")
            return

        print(f"\n{Colors.OKGREEN}Obtendo dados do usuário autenticado...{Colors.ENDC}")

        try:
            response = requests.get(
                f"{self.base_url}/usuario/",
                headers={"Authorization": f"Bearer {self.access_token}"}
            )

            self.print_response(response)

        except requests.exceptions.RequestException as e:
            print(f"{Colors.FAIL}Erro na requisição: {e}{Colors.ENDC}")

    def renovar_token(self):
        """Renova o access token usando o refresh token"""
        if not self.refresh_token:
            print(f"{Colors.FAIL}Você precisa ter um refresh token! Faça login primeiro.{Colors.ENDC}")
            return

        print(f"\n{Colors.OKGREEN}Renovando access token...{Colors.ENDC}")

        try:
            response = requests.post(
                f"{self.base_url}/token/refresh/",
                json={"refresh": self.refresh_token},
                headers={"Content-Type": "application/json"}
            )

            self.print_response(response)

            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access')
                print(f"\n{Colors.OKGREEN}✓ Novo access token salvo automaticamente!{Colors.ENDC}")

        except requests.exceptions.RequestException as e:
            print(f"{Colors.FAIL}Erro na requisição: {e}{Colors.ENDC}")

    def visualizar_tokens(self):
        """Visualiza os tokens atuais"""
        print(f"\n{Colors.OKGREEN}Tokens Atuais:{Colors.ENDC}")

        if self.access_token:
            print(f"\n{Colors.OKCYAN}Access Token:{Colors.ENDC}")
            print(f"{self.access_token[:50]}...{self.access_token[-20:]}")
        else:
            print(f"\n{Colors.WARNING}Access Token: Não disponível{Colors.ENDC}")

        if self.refresh_token:
            print(f"\n{Colors.OKCYAN}Refresh Token:{Colors.ENDC}")
            print(f"{self.refresh_token[:50]}...{self.refresh_token[-20:]}")
        else:
            print(f"\n{Colors.WARNING}Refresh Token: Não disponível{Colors.ENDC}")

    def limpar_tokens(self):
        """Limpa os tokens salvos"""
        self.access_token = None
        self.refresh_token = None
        print(f"\n{Colors.OKGREEN}✓ Tokens limpos!{Colors.ENDC}")

    def mostrar_menu(self):
        """Mostra o menu principal"""
        self.print_header("API TESTER - Autenticação JWT")

        print(f"{Colors.OKGREEN}1.{Colors.ENDC} Registrar um usuário")
        print(f"{Colors.OKGREEN}2.{Colors.ENDC} Registrar todos os usuários (5)")
        print(f"{Colors.OKGREEN}3.{Colors.ENDC} Fazer login")
        print(f"{Colors.OKGREEN}4.{Colors.ENDC} Obter dados do usuário atual")
        print(f"{Colors.OKGREEN}5.{Colors.ENDC} Renovar access token")
        print(f"{Colors.OKGREEN}6.{Colors.ENDC} Visualizar tokens")
        print(f"{Colors.OKGREEN}7.{Colors.ENDC} Limpar tokens")
        print(f"{Colors.OKGREEN}8.{Colors.ENDC} Executar teste completo")
        print(f"{Colors.FAIL}0.{Colors.ENDC} Sair")

        if self.access_token:
            print(f"\n{Colors.OKGREEN}✓ Autenticado{Colors.ENDC}")
        else:
            print(f"\n{Colors.WARNING}⚠ Não autenticado{Colors.ENDC}")

    def executar_teste_completo(self):
        """Executa um fluxo completo de testes"""
        self.print_header("EXECUTANDO TESTE COMPLETO")

        print(f"{Colors.OKCYAN}Passo 1/5: Registrando todos os usuários...{Colors.ENDC}")
        self.registrar_todos_usuarios()

        input(f"\n{Colors.WARNING}Pressione ENTER para continuar...{Colors.ENDC}")

        print(f"\n{Colors.OKCYAN}Passo 2/5: Fazendo login com o primeiro usuário (maria)...{Colors.ENDC}")
        try:
            response = requests.post(
                f"{self.base_url}/login/",
                json={"username": "maria", "password": "senha123"},
                headers={"Content-Type": "application/json"}
            )
            self.print_response(response)
            if response.status_code == 200:
                data = response.json()
                self.access_token = data.get('access')
                self.refresh_token = data.get('refresh')
        except requests.exceptions.RequestException as e:
            print(f"{Colors.FAIL}Erro: {e}{Colors.ENDC}")

        input(f"\n{Colors.WARNING}Pressione ENTER para continuar...{Colors.ENDC}")

        print(f"\n{Colors.OKCYAN}Passo 3/5: Obtendo dados do usuário autenticado...{Colors.ENDC}")
        self.obter_usuario_atual()

        input(f"\n{Colors.WARNING}Pressione ENTER para continuar...{Colors.ENDC}")

        print(f"\n{Colors.OKCYAN}Passo 4/5: Renovando access token...{Colors.ENDC}")
        self.renovar_token()

        input(f"\n{Colors.WARNING}Pressione ENTER para continuar...{Colors.ENDC}")

        print(f"\n{Colors.OKCYAN}Passo 5/5: Obtendo dados novamente com novo token...{Colors.ENDC}")
        self.obter_usuario_atual()

        print(f"\n{Colors.OKGREEN}{'='*60}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}TESTE COMPLETO FINALIZADO!{Colors.ENDC}")
        print(f"{Colors.OKGREEN}{'='*60}{Colors.ENDC}")

    def run(self):
        """Executa o CLI"""
        while True:
            self.mostrar_menu()

            try:
                opcao = input(f"\n{Colors.OKCYAN}Escolha uma opção: {Colors.ENDC}").strip()

                if opcao == '0':
                    print(f"\n{Colors.OKGREEN}Até logo!{Colors.ENDC}\n")
                    break
                elif opcao == '1':
                    self.registrar_usuario()
                elif opcao == '2':
                    self.registrar_todos_usuarios()
                elif opcao == '3':
                    self.fazer_login()
                elif opcao == '4':
                    self.obter_usuario_atual()
                elif opcao == '5':
                    self.renovar_token()
                elif opcao == '6':
                    self.visualizar_tokens()
                elif opcao == '7':
                    self.limpar_tokens()
                elif opcao == '8':
                    self.executar_teste_completo()
                else:
                    print(f"{Colors.FAIL}Opção inválida!{Colors.ENDC}")

                input(f"\n{Colors.WARNING}Pressione ENTER para continuar...{Colors.ENDC}")

                # Limpa a tela (funciona em Unix/Linux/Mac)
                os.system('clear' if os.name == 'posix' else 'cls')

            except KeyboardInterrupt:
                print(f"\n\n{Colors.OKGREEN}Até logo!{Colors.ENDC}\n")
                break
            except Exception as e:
                print(f"{Colors.FAIL}Erro inesperado: {e}{Colors.ENDC}")
                input(f"\n{Colors.WARNING}Pressione ENTER para continuar...{Colors.ENDC}")


def main():
    """Função principal"""
    print(f"{Colors.HEADER}{Colors.BOLD}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                                                            ║")
    print("║           API TESTER - Autenticação JWT                   ║")
    print("║                                                            ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.ENDC}")

    # Verifica se o servidor está rodando
    tester = APITester()
    try:
        response = requests.get(f"{tester.base_url}/", timeout=2)
    except requests.exceptions.RequestException:
        print(f"{Colors.FAIL}⚠ ATENÇÃO: Servidor não está respondendo em {tester.base_url}{Colors.ENDC}")
        print(f"{Colors.WARNING}Certifique-se de que o servidor Django está rodando:{Colors.ENDC}")
        print(f"{Colors.OKCYAN}  python manage.py runserver{Colors.ENDC}\n")
        continuar = input(f"{Colors.WARNING}Deseja continuar mesmo assim? (s/n): {Colors.ENDC}").lower()
        if continuar != 's':
            return

    tester.run()


if __name__ == "__main__":
    main()
