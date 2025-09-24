SELECT c.nome AS cliente, p.nome AS pet, p.especie, p.raca
FROM clientes c
JOIN pets p ON c.id_cliente = p.id_cliente
WHERE p.especie = 'Cão'
ORDER BY c.nome;

Questão 01: Exibindo raça de cães de cada cliente, sendo ordenado por nome do cliente dono do pet.


SELECT s.categoria, COUNT(*) as total_agendamentos, SUM(a.valor_pago) as receita_total
FROM servicos s
JOIN agendamentos a ON s.id_servico = a.id_servico
WHERE a.status = 'Concluído'
GROUP BY s.categoria
ORDER BY receita_total DESC;

Questão 02: Mostrando de forma agrupada por categoria os serviços já concluídos e os valores gastos para a realização de cada um.


SELECT f.nome AS funcionario, f.cargo, COUNT(a.id_agendamento) as total_atendimentos
FROM funcionarios f
JOIN agendamentos a ON f.id_funcionario = a.id_funcionario 
    AND a.data_agendamento BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY f.id_funcionario, f.nome, f.cargo
ORDER BY total_atendimentos DESC;

Questão 03: Consultando o total de atendimentos realizados por cada funcionario entre um período de dias em específico 
e exibindo isso de forma organizada por tipo de cargo. 


SELECT c.nome AS cliente, COUNT(DISTINCT p.id_pet) as qtd_pets, 
       COUNT(a.id_agendamento) as total_agendamentos
FROM clientes c
JOIN pets p ON c.id_cliente = p.id_cliente
JOIN agendamentos a ON p.id_pet = a.id_pet
GROUP BY c.id_cliente, c.nome
HAVING COUNT(DISTINCT p.id_pet) > 1
ORDER BY qtd_pets DESC;

Questão 04: Consultando os clientes com mais de 1 pet e quantidade de agendamentos que foram feitos para cada um desses pets, 
demostrando isso em ordem de quantidade de pets.


SELECT s.nome_servico, s.preco, AVG(s.preco) OVER() as preco_medio_geral,
       CASE 
           WHEN s.preco > AVG(s.preco) OVER() THEN 'Acima da Média'
           ELSE 'Na Média ou Abaixo'
       END as classificacao
FROM servicos s
ORDER BY s.preco DESC;

Questão 05: Consultando e mostrando os preços dos serviços classificando quais estão acima da média de valor e quais estão abaixo dessa 
média.


SELECT MONTH(a.data_agendamento) as mes, 
       COUNT(*) as total_agendamentos,
       SUM(a.valor_pago) as receita_mensal
FROM agendamentos a
WHERE YEAR(a.data_agendamento) = 2024 
  AND a.status IN ('Concluído', 'Pago')
GROUP BY MONTH(a.data_agendamento)
ORDER BY mes;

Questão 06: Exibindo de acordo com dias e mês os atendimentos de 2024 que já foram realizados e pagos.

Questão 07: Todos os pets, nome, especie, raça, dono

SELECT p.nome AS pet, p.especie, p.raca, c.nome AS cliente
FROM pets p
JOIN pets p ON c.id_cliente = p.id_cliente
ORDER BY p.name;
