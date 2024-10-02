# L02 - Instalação e Configuração do PostgreSQL Admin

## Pré-requisitos
- Sistema operacional: Windows, macOS ou Linux
- PostgreSQL instalado

## Passo 1: Baixar o pgAdmin
1. Acesse o site oficial do pgAdmin: pgAdmin Downloads
2. Selecione a versão adequada para o seu sistema operacional.
3. Baixe e execute o instalador.

[pgAdmin Downloads](https://www.pgadmin.org/download/)

## Passo 2: Instalar o pgAdmin
1. Siga as instruções do instalador para completar a instalação.
2. No Windows, você pode precisar reiniciar o computador após a instalação.


## Passo 3: Configurar o pgAdmin
1. Abra o pgAdmin.
2. Na tela inicial, clique em "Add New Server".


3. Preencha as informações do servidor:
   - **Name**: Nome do servidor (ex: `MeuServidorPostgres`)
   - **Host**: Endereço do servidor (ex: `localhost` para um servidor local)
   - **Port**: Porta do PostgreSQL (padrão é `5432`)
   - **Username**: Nome de usuário do PostgreSQL (ex: `postgres`)
   - **Password**: Senha do usuário

## Passo 4: Conectar ao Servidor
1. Após preencher as informações, clique em "Save".
2. O pgAdmin tentará se conectar ao servidor PostgreSQL.
3. Se a conexão for bem-sucedida, você verá o servidor listado na árvore de servidores.


## Passo 5: Gerenciar Bancos de Dados
1. Expanda o servidor na árvore de servidores.
2. Você verá uma lista de bancos de dados disponíveis.
3. Clique com o botão direito em um banco de dados para gerenciar tabelas, executar consultas SQL, etc.



## Passo 6: Executar Consultas SQL
1. Selecione o banco de dados desejado.
2. Clique em "Tools" > "Query Tool".
3. Digite sua consulta SQL na janela de consulta.
4. Clique em "Execute/Refresh" para executar a consulta.


## Conclusão
Você instalou e configurou com sucesso o pgAdmin para gerenciar seu servidor PostgreSQL. Agora você pode criar e gerenciar bancos de dados, executar consultas e muito mais!

