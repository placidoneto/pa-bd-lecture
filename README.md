# L01 - Fundamentos SQL em PostgreSQL

### O que é o SQL?

**SQL (Structured Query Language)** é a linguagem padrão para gerenciar e manipular bancos de dados relacionais. O SQL é uma ferramenta indispensável para qualquer profissional que trabalha com dados. Sua versatilidade, poder e facilidade de uso fazem dele a linguagem padrão para interagir com bancos de dados relacionais. Aqui estão alguns conceitos básicos:

### Conceitos Básicos

- **Banco de Dados**: Conjunto organizado de dados armazenados e acessados eletronicamente.
- **Tabela**: Estrutura dentro de um banco de dados que armazena dados em linhas e colunas.
- **Linha (Registro)**: Uma única entrada em uma tabela.
- **Coluna (Campo)**: Um atributo de dados em uma tabela.- **Chave Primária**: Um identificador único para cada registro em uma tabela.
- **Chave Estrangeira**: Um campo que cria um relacionamento entre duas tabelas.


### Por que usar SQL? Uma Linguagem Essencial para Manipulação de Dados

- **Linguagem universal**: É amplamente utilizada em diversos sistemas gerenciadores de bancos de dados (SGBDs), como PostgreSQL, MySQL, Oracle, SQL Server, etc.

- **Facilidade de aprendizado**: Possui uma sintaxe relativamente simples e intuitiva, facilitando o aprendizado para pessoas com diferentes níveis de experiência.

- **Consultas eficientes**: Permite realizar consultas complexas e obter resultados precisos em grandes conjuntos de dados de forma rápida.
- **Agrupamento e agregação**: Funções como SUM, AVG, COUNT, GROUP BY e HAVING permitem realizar cálculos e análises estatísticas sobre os dados.

#### Criação de Banco de Dados e Tabelas

```sql
-- Criação de um banco de dados
CREATE DATABASE nome_do_banco;

-- Seleção de um banco de dados
\c nome_do_banco;

-- Criação de uma tabela
CREATE TABLE nome_da_tabela (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    idade INT
);
```

#### Inserção de Dados

```sql
-- Inserção de dados em uma tabela
INSERT INTO nome_da_tabela (nome, idade) VALUES ('João', 30);
```

#### Consulta de Dados

```sql
-- Seleção de todos os dados de uma tabela
SELECT * FROM nome_da_tabela;

-- Seleção de dados com condição
SELECT * FROM nome_da_tabela WHERE idade > 25;
```

#### Atualização de Dados

```sql
-- Atualização de dados em uma tabela
UPDATE nome_da_tabela SET idade = 31 WHERE nome = 'João';
```

#### Exclusão de Dados

```sql
-- Exclusão de dados em uma tabela
DELETE FROM nome_da_tabela WHERE nome = 'João';
```

#### Alteração de Estrutura de Tabelas

```sql
-- Adição de uma nova coluna
ALTER TABLE nome_da_tabela ADD COLUMN email VARCHAR(100);

-- Exclusão de uma coluna
ALTER TABLE nome_da_tabela DROP COLUMN email;
```

### Funções de Agregação

```sql
-- Contagem de registros
SELECT COUNT(*) FROM nome_da_tabela;

-- Soma de valores
SELECT SUM(idade) FROM nome_da_tabela;

-- Média de valores
SELECT AVG(idade) FROM nome_da_tabela;
```

### Junções (Joins)

```sql
-- Junção interna
SELECT a.nome, b.idade
FROM tabela1 a
INNER JOIN tabela2 b ON a.id = b.id;

-- Junção externa
SELECT a.nome, b.idade
FROM tabela1 a
LEFT JOIN tabela2 b ON a.id = b.id;
```

### Subconsultas

```sql
-- Subconsulta em cláusula WHERE
SELECT nome FROM nome_da_tabela
WHERE idade > (SELECT AVG(idade) FROM nome_da_tabela);
```

## Aplicação de Venda de Veículos com PostgreSQL: Uma Visão Geral e Exemplos de Consultas SQL

Imagine uma aplicação web que permite a compra e venda de veículos. Essa aplicação seria construída com uma interface intuitiva, onde os usuários podem:

- **Cadastrar veículos**: Informando marca, modelo, ano, preço e outras características relevantes.
- **Pesquisar veículos**: Filtrando por diversos critérios, como marca, modelo, faixa de preço e ano.
- **Gerencia a venda dos veículos**: Realizar o registro de venda de um veículo para um cliente.

Ver código abaixo:

```sql
-- Criação das tabelas
CREATE TABLE Clientes (
    ClienteID SERIAL PRIMARY KEY,
    Nome VARCHAR(100),
    Email VARCHAR(100),
    Telefone VARCHAR(20)
);

CREATE TABLE Veiculos (
    VeiculoID SERIAL PRIMARY KEY,
    Marca VARCHAR(50),
    Modelo VARCHAR(50),
    Ano INT,
    Preco DECIMAL(10, 2)
);

CREATE TABLE Vendas (
    VendaID SERIAL PRIMARY KEY,
    ClienteID INT REFERENCES Clientes(ClienteID),
    VeiculoID INT REFERENCES Veiculos(VeiculoID),
    DataVenda DATE,
    ValorVenda DECIMAL(10, 2)
);
```

Agora vamos inserir alguns dados no banco de dados:
```sql
-- Inserção de dados nas tabelas
INSERT INTO Clientes (Nome, Email, Telefone) VALUES
('João Silva', 'joao.silva@example.com', '123456789'),
('Maria Oliveira', 'maria.oliveira@example.com', '987654321');

INSERT INTO Veiculos (Marca, Modelo, Ano, Preco) VALUES
('Toyota', 'Corolla', 2020, 75000.00),
('Honda', 'Civic', 2019, 70000.00);

INSERT INTO Vendas (ClienteID, VeiculoID, DataVenda, ValorVenda) VALUES
(1, 1, '2024-09-01', 75000.00),
(2, 2, '2024-09-05', 70000.00);

-- Consultas SQL
-- 1. Selecionar todos os clientes
SELECT * FROM Clientes;

-- 2. Selecionar todos os veículos disponíveis
SELECT * FROM Veiculos;

-- 3. Selecionar todas as vendas realizadas
SELECT * FROM Vendas;

-- 4. Selecionar vendas com detalhes do cliente e veículo
SELECT Vendas.VendaID, Clientes.Nome, Veiculos.Marca, Veiculos.Modelo, Vendas.DataVenda, Vendas.ValorVenda
FROM Vendas
JOIN Clientes ON Vendas.ClienteID = Clientes.ClienteID
JOIN Veiculos ON Vendas.VeiculoID = Veiculos.VeiculoID;
```

### Estrutura da Aplicação Web com Flask e Python para a aplicação de Venda de Veículos

Vamos implementar uma simples aplicação usando Flask para manipular os dados de venda.

Estrutura de Diretórios
```
/app
    /static
    /templates
    __init__.py
    routes.py
    models.py
    config.py
run.py
```

Código da Aplicação

run.py
```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)    
```

app/__init__.py
```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()

    return app   
```