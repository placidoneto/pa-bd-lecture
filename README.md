
# Trabalho Prático 1 - Modelagem e Consultas SQL

## Descrição do Trabalho

O trabalho prático consiste em desenvolver um banco de dados relacional para uma aplicação de gerenciamento de laboratórios. O objetivo é aplicar os conceitos de modelagem de dados, criação de tabelas e consultas SQL aprendidos nas aulas.

**Link assignment Github Classroom**: https://classroom.github.com/a/PIpNkXJW

Imagine que a Direção da DIATINF solicitou para que você resolvesse um problema crônico de gestão de laboratórios da nossa Diretoria. O problema é que os laboratórios não têm um controle adequado de agendamento e uso, o que leva a conflitos de horários e falta de recursos disponíveis para os alunos.

A Direção da DIATINF decidiu criar um sistema de agendamento de laboratórios, onde os professores poderão reservar horários para utilizar os laboratórios disponíveis. Os laboratórios também podem ser reservados para atividades extras, como reuniões, cursos, palestras, etc.

Cada laboratório tem um nome, uma descrição, uma capacidade máxima de alunos e um status (disponível ou indisponível em um determinado horário). Os professores podem reservar laboratórios para aulas, e cada reserva deve incluir o nome do professor, a data e hora de início e fim da reserva, o laboratório reservado e o número de alunos.

Nos casos dos laboratórios já estares alocados para as aulas, o professor deverá registrar a retirada e a entrega da chave do laboratório, com a data e hora de retirada e entrega. O sistema deve permitir que os professores visualizem as reservas feitas para cada laboratório, bem como o histórico de reservas e retiradas de chaves.

Percebam que a gerência dos laboratórios seguem 2 fluxos distintos:
1. O fluxo principal é de horarios de aulas definidos para os professores e suas respectivas disciplinas e cursos;
2. A reserva de laboratórios nos horários disponíveis para atividades extras, como reuniões, cursos, palestras, etc.

## O que deve ser entregue?

1. Listar os elementos conceituais de domínio do problema e a suas respectivas descrições;
    - **Exemplo de Possíveis Elementos Conceituais:**
      1. Laboratório: Nome, Descrição, Capacidade, Status
      2. Professor: Nome, Disciplina, Curso
      3. Reserva: Data e Hora de Início, Data e Hora de Fim, Número de Alunos
      4. Retirada/Entrega de Chave: Data e Hora de Retirada, Data e Hora de Entrega
      5. Atividade Extra: Tipo (Reunião, Curso, Palestra), Data e Hora
      6. *OBS: Você tem autonomia para definir outros e novos elementos conceituais que sejam relevantes para o sistema.*
2. Criar o modelo conceitual a partir dos elementos de domínio;
3. Criar o modelo lógico a partir do modelo conceitual (DER);
4. Criar o modelo físico a partir do modelo lógico (Script SQL para criação do banco e tabelas);
5. Criar o script SQL para popular as tabelas com dados fictícios (de 2 a 5 registros por tabela);
6. Criar o script SQL para consultas (mínimo 5 consultas) que demonstrem o uso de JOINs, GROUP BY, HAVING, ORDER BY e WHERE para manipulação e consulta dos dados;
    - **Exemplo de Possíveis Consultas:**
      1. Listar todos os laboratórios disponíveis para reserva;
      2. Listar todas as reservas feitas por um professor;
      3. Listar o histórico de reservas e retiradas de chaves de um laboratório específico;
      4. Listar o número total de reservas feitas por cada professor em um determinado período;
      5. Listar o número total de reservas feitas para cada laboratório em um determinado período;
      6. *OBS: Você tem autonomia para definir outras e novas consultas que sejam relevantes para o sistema.*

OBS.: O trabalho deve ser entregue com as informações no Readme.md do repositório, com os scripts SQL para criação do banco e tabelas, inserção de dados e consultas. 

Os modelos conceitual, lógico e físico devem ser entregues em formato de imagem (PNG ou JPG). A imagem do banco criado no postgres também deve ser incluido no Readme.md.