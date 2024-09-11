# L01 - Fundamentos SQL em PostgreSQL

### O que é o SQL?

**SQL (Structured Query Language)** é a linguagem padrão para gerenciar e manipular bancos de dados relacionais. Aqui estão alguns conceitos básicos:

### Conceitos Básicos

- **Banco de Dados**: Conjunto organizado de dados armazenados e acessados eletronicamente.
- **Tabela**: Estrutura dentro de um banco de dados que armazena dados em linhas e colunas.
- **Linha (Registro)**: Uma única entrada em uma tabela.
- **Coluna (Campo)**: Um atributo de dados em uma tabela.- **Chave Primária**: Um identificador único para cada registro em uma tabela.
- **Chave Estrangeira**: Um campo que cria um relacionamento entre duas tabelas.


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
