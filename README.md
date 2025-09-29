# TP1 - 2025.2 Consultas Avançadas

Link Assignment: https://classroom.github.com/a/Uln1eKr9
Nome Repositório: *TP1_NomeSobrenome*

Considere que você está para modelar o banco de um Sistema de PetShop, e após a modelagem, você identificou algumas das tabelas listadas abaixo.

# Modelo de Dados - Sistema Petshop

## 1. Tabela: CLIENTES
```sql
CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    telefone VARCHAR(15),
    email VARCHAR(100),
    endereco TEXT,
    data_cadastro DATE
);
```

## 2. Tabela: PETS
```sql
CREATE TABLE pets (
    id_pet INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(50) NOT NULL,
    especie VARCHAR(30),
    raca VARCHAR(50),
    idade INT,
    peso DECIMAL(5,2),
    id_cliente INT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);
```

## 3. Tabela: SERVICOS
```sql
CREATE TABLE servicos (
    id_servico INT PRIMARY KEY AUTO_INCREMENT,
    nome_servico VARCHAR(80) NOT NULL,
    preco DECIMAL(8,2) NOT NULL,
    duracao_minutos INT,
    categoria VARCHAR(30)
);
```

## 4. Tabela: FUNCIONARIOS
```sql
CREATE TABLE funcionarios (
    id_funcionario INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    cargo VARCHAR(50),
    salario DECIMAL(8,2),
    data_admissao DATE,
    especialidade VARCHAR(50)
);
```

## 5. Tabela: AGENDAMENTOS
```sql
CREATE TABLE agendamentos (
    id_agendamento INT PRIMARY KEY AUTO_INCREMENT,
    id_pet INT,
    id_servico INT,
    id_funcionario INT,
    data_agendamento DATE,
    hora_agendamento TIME,
    status VARCHAR(20),
    valor_pago DECIMAL(8,2),
    observacoes TEXT,
    FOREIGN KEY (id_pet) REFERENCES pets(id_pet),
    FOREIGN KEY (id_servico) REFERENCES servicos(id_servico),
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario)
);
```

## Relacionamentos:
- **CLIENTES** (1) → (N) **PETS**
- **PETS** (1) → (N) **AGENDAMENTOS**
- **SERVICOS** (1) → (N) **AGENDAMENTOS**
- **FUNCIONARIOS** (1) → (N) **AGENDAMENTOS**

Considerando o que foi definido acima, responda as seguintes questões no README do Repositório.

**Instruções:** Para cada consulta SQL apresentada abaixo, descreva detalhadamente o que está sendo executado, incluindo quais tabelas estão sendo consultadas, como estão sendo relacionadas e qual é o resultado esperado.

---

## Questão 1 
```sql
SELECT c.nome AS cliente, p.nome AS pet, p.especie, p.raca
FROM clientes c
JOIN pets p ON c.id_cliente = p.id_cliente
WHERE p.especie = 'Cão'
ORDER BY c.nome;
```

**Descreva o que esta consulta faz:**
```
Lista todos os clientes que possuem cães, mostrando nome do cliente, nome do pet, espécie e raça. O uso da junção entre clientes e pets, filtra apenas cães e ordena por nome do cliente.
```

---

## Questão 2 
```sql
SELECT s.categoria, COUNT(*) as total_agendamentos, SUM(a.valor_pago) as receita_total
FROM servicos s
JOIN agendamentos a ON s.id_servico = a.id_servico
WHERE a.status = 'Concluído'
GROUP BY s.categoria
ORDER BY receita_total DESC;
```

**Descreva o que esta consulta faz:**
```
Agrupa os serviços por categoria e calcula o total de agendamentos concluídos e a receita total por categoria. Ordena pela receita (maior para menor).
```

---

## Questão 3 
```sql
SELECT f.nome AS funcionario, f.cargo, COUNT(a.id_agendamento) as total_atendimentos
FROM funcionarios f
JOIN agendamentos a ON f.id_funcionario = a.id_funcionario 
    AND a.data_agendamento BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY f.id_funcionario, f.nome, f.cargo
ORDER BY total_atendimentos DESC;
```

**Descreva o que esta consulta faz:**
```
Mostra todos os funcionários com a quantidade de atendimentos realizados em 2024. Ordena por quantidade de atendimentos.
```

---

## Questão 4 
```sql
SELECT c.nome AS cliente, COUNT(DISTINCT p.id_pet) as qtd_pets, 
       COUNT(a.id_agendamento) as total_agendamentos
FROM clientes c
JOIN pets p ON c.id_cliente = p.id_cliente
JOIN agendamentos a ON p.id_pet = a.id_pet
GROUP BY c.id_cliente, c.nome
HAVING COUNT(DISTINCT p.id_pet) > 1
ORDER BY qtd_pets DESC;
```

**Descreva o que esta consulta faz:**
```
Lista clientes que possuem mais de 1 pet, mostrando quantos pets cada um tem e total de agendamentos. O uso de várias junções e having filtra para considerar as restrições.
```

---

## Questão 5 
```sql
SELECT s.nome_servico, s.preco, AVG(s.preco) OVER() as preco_medio_geral,
       CASE 
           WHEN s.preco > AVG(s.preco) OVER() THEN 'Acima da Média'
           ELSE 'Na Média ou Abaixo'
       END as classificacao
FROM servicos s
ORDER BY s.preco DESC;
```

**Descreva o que esta consulta faz:**
```
Lista todos os serviços comparando o preço de cada um com a média geral, classificando se está acima ou na média/abaixo. 
```

---

## Questão 6 
```sql
SELECT MONTH(a.data_agendamento) as mes, 
       COUNT(*) as total_agendamentos,
       SUM(a.valor_pago) as receita_mensal
FROM agendamentos a
WHERE YEAR(a.data_agendamento) = 2024 
  AND a.status IN ('Concluído', 'Pago')
GROUP BY MONTH(a.data_agendamento)
ORDER BY mes;
```

**Descreva o que esta consulta faz:**
```
Relatório mensal de 2024 mostrando quantidade de agendamentos e receita por mês, apenas para agendamentos concluídos ou pagos.
```

---



**Instruções:** Com base no modelo de dados do sistema petshop apresentado anteriormente, crie consultas SQL para resolver os problemas propostos abaixo. Suas consultas devem ser funcionais e otimizadas.

---

## Questão 7
**Problema:** O gerente do petshop precisa de uma lista com todos os pets cadastrados no sistema, mostrando o nome do pet, a espécie, a raça e o nome do dono. A lista deve estar ordenada alfabeticamente pelo nome do pet.

**Sua consulta SQL:**
```sql
SELECT p.nome AS pet, p.especie, p.raca, c.nome AS dono
FROM pets p
INNER JOIN clientes c ON p.id_cliente = c.id_cliente
ORDER BY p.nome;
```

---

## Questão 8
**Problema:** A recepcionista precisa saber quais são os 3 serviços mais caros oferecidos pelo petshop e quantas vezes cada um já foi agendado (independente do status). Se um serviço nunca foi agendado, ainda deve aparecer na lista com quantidade 0.

**Sua consulta SQL:**
```sql
SELECT s.nome_servico, s.preco, COUNT(a.id_agendamento) as vezes_agendado
FROM servicos s
LEFT JOIN agendamentos a ON s.id_servico = a.id_servico
GROUP BY s.id_servico, s.nome_servico, s.preco
ORDER BY s.preco DESC
LIMIT 3;
```

---

## Questão 9
**Problema:** O dono do petshop quer identificar os clientes mais fiéis. Ele precisa de um relatório mostrando os clientes que têm pelo menos 2 pets cadastrados E que já fizeram pelo menos 5 agendamentos no total (considerando todos os seus pets). O relatório deve mostrar: nome do cliente, quantidade de pets, total de agendamentos e o valor total já pago por esse cliente.

**Sua consulta SQL:**
```sql
SELECT c.nome AS cliente, 
       COUNT(DISTINCT p.id_pet) as qtd_pets,
       COUNT(a.id_agendamento) as total_agendamentos,
       COALESCE(SUM(a.valor_pago), 0) as valor_total_pago
FROM clientes c
INNER JOIN pets p ON c.id_cliente = p.id_cliente
LEFT JOIN agendamentos a ON p.id_pet = a.id_pet
GROUP BY c.id_cliente, c.nome
HAVING COUNT(DISTINCT p.id_pet) >= 2 
   AND COUNT(a.id_agendamento) >= 5
ORDER BY valor_total_pago DESC;
```

---

## Questão 10
**Problema:** Para fins de análise de desempenho, o petshop precisa de um relatório mensal dos últimos 6 meses mostrando: o mês/ano, quantos agendamentos foram realizados, quantos foram cancelados, qual a receita total do mês (apenas agendamentos concluídos), e qual foi o serviço mais popular (mais agendado) em cada mês.

**Dica:** Considere que estamos em dezembro de 2024. Foque apenas na parte principal do relatório (mês, total de agendamentos, cancelados e receita). O serviço mais popular pode ser uma consulta separada se necessário.

**Sua consulta SQL:**
```sql
-- ANULADA -- ANULADA -- ANULADA -- ANULADA -- ANULADA -- 
SELECT 
    CONCAT(YEAR(a.data_agendamento), '-', LPAD(MONTH(a.data_agendamento), 2, '0')) as mes_ano,
    COUNT(*) as total_agendamentos,
    COUNT(CASE WHEN a.status = 'Cancelado' THEN 1 END) as cancelados,
    SUM(CASE WHEN a.status = 'Concluído' THEN a.valor_pago ELSE 0 END) as receita_total
FROM agendamentos a
-- Filtra apenas agendamentos dos últimos 6 meses
-- DATE_SUB subtrai 6 meses da data atual (CURDATE)
-- Exemplo: se hoje é 29/09/2024, pega agendamentos >= 29/03/2024
WHERE a.data_agendamento >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY YEAR(a.data_agendamento), MONTH(a.data_agendamento)
ORDER BY a.data_agendamento DESC;
-- ANULADA -- ANULADA -- ANULADA -- ANULADA -- ANULADA --
```

---


### Critérios de Avaliação:
- Identificação correta das tabelas envolvidas
- Explicação do tipo de JOIN utilizado
- Compreensão das funções agregadas (COUNT, SUM, AVG)
- Explicação do GROUP BY e ORDER BY
- Interpretação do resultado esperado
