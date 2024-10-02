# L03 - Consultas Avançadas #1

## Estrutura da Tabela


Primeiro, vamos definir a estrutura das tabelas:

```sql
CREATE TABLE grupos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

CREATE TABLE contatos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefone VARCHAR(20),
    grupo_id INT,
    data_nascimento DATE,
    FOREIGN KEY (grupo_id) REFERENCES grupos(id)
);
```


## Inserindo Dados

Vamos inserir alguns dados para trabalhar:

```sql
INSERT INTO grupos (nome) VALUES ('Família'), ('Amigos'), ('Trabalho');

INSERT INTO contatos (nome, email, telefone, grupo_id, data_nascimento) VALUES
('João Silva', 'joao@example.com', '123456789', 1, '1985-05-15'),
('Maria Oliveira', 'maria@example.com', '987654321', 2, '1990-08-22'),
('Carlos Souza', NULL, '555555555', 3, '1982-12-30'),
('Ana Costa', 'ana@example.com', NULL, 1, '1995-03-10');
```

## Filtragem

A cláusula WHERE especifica o critério de pesquisa para as linhas retornadas pela consulta.

Para filtrar contatos de um grupo específico:

```sql
SELECT * FROM contatos WHERE grupo_id = 1;
```

Para filtrar contatos que têm email:
  
  ```sql
SELECT * FROM contatos WHERE email IS NOT NULL;
```


## Ordenação

A cláusula ORDER BY é usada para classificar o resultado em ordem crescente ou decrescente.

Para ordenar contatos por nome:

```sql
SELECT * FROM contatos ORDER BY nome;
```

Para ordenar contatos por nome em ordem alfabética:

```sql  
SELECT * FROM contatos ORDER BY nome ASC;
```

Para ordenar contatos por data de nascimento, mais recentes primeiro:


```sql  
SELECT * FROM contatos ORDER BY data_nascimento DESC;
```

## Valores Distintos

A cláusula DISTINCT é usada para retornar apenas valores distintos. 
Para obter uma lista de grupos distintos aos quais os contatos pertencem:

```sql 
SELECT DISTINCT grupo_id FROM contatos;
```

## Valores Nulos

Para filtrar contatos que não têm email ou telefone:

```sql
SELECT * FROM contatos WHERE email IS NULL;
SELECT * FROM contatos WHERE telefone IS NULL;
```

## Intervalos de Busca

Para filtrar contatos que nasceram entre 1990 e 1995:

```sql
SELECT * FROM contatos WHERE data_nascimento BETWEEN '1990-01-01' AND '1995-12-31';
```

Para encontrar contatos com nomes que começam com ‘A’:

```sql
SELECT * FROM contatos WHERE nome LIKE 'A%';
```

## Junção de Tabelas

Para obter uma lista de contatos com os nomes de seus grupos:

```sql
SELECT contatos.nome, grupos.nome AS grupo
FROM contatos
JOIN grupos ON contatos.grupo_id = grupos.id;
```

## Conclusão

Nesta aula, vimos como filtrar, ordenar e agrupar dados em consultas SQL. 

Essas consultas cobrem uma ampla gama de operações avançadas em PostgreSQL. Com essas técnicas, você pode gerenciar e consultar sua agenda de contatos de maneira eficiente e eficaz. Se precisar de mais detalhes ou tiver outras perguntas, estou aqui para ajudar!
