
# Trabalho Prático 2 - Modelagem em Django Rest

## Descrição do Trabalho

O trabalho prático consiste em evoluir o TP 1, onde foi modelago um sistema de gerenciamento de laboratórios. O sistema deve permitir que os professores reservem horários para utilizar os laboratórios disponíveis, além de permitir a reserva de laboratórios para atividades extras, como reuniões, cursos, palestras, etc.

**Link assignment Github Classroom**: https://classroom.github.com/a/2UIF0oTU

Imagine que a Direção da DIATINF solicitou para que você resolvesse um problema crônico de gestão de laboratórios da nossa Diretoria. O problema é que os laboratórios não têm um controle adequado de agendamento e uso, o que leva a conflitos de horários e falta de recursos disponíveis para os alunos.

A Direção da DIATINF decidiu criar um sistema de agendamento de laboratórios, onde os professores poderão reservar horários para utilizar os laboratórios disponíveis. Os laboratórios também podem ser reservados para atividades extras, como reuniões, cursos, palestras, etc.

Cada laboratório tem um nome, uma descrição, uma capacidade máxima de alunos e um status (disponível ou indisponível em um determinado horário). Os professores podem reservar laboratórios para aulas, e cada reserva deve incluir o nome do professor, a data e hora de início e fim da reserva, o laboratório reservado e o número de alunos.

Nos casos dos laboratórios já estares alocados para as aulas, o professor deverá registrar a retirada e a entrega da chave do laboratório, com a data e hora de retirada e entrega. O sistema deve permitir que os professores visualizem as reservas feitas para cada laboratório, bem como o histórico de reservas e retiradas de chaves.

Percebam que a gerência dos laboratórios seguem 2 fluxos distintos:
1. O fluxo principal é de horarios de aulas definidos para os professores e suas respectivas disciplinas e cursos;
2. A reserva de laboratórios nos horários disponíveis para atividades extras, como reuniões, cursos, palestras, etc.

Para a criação da primeira versão da API deve-se considerar o que já foi trabalhado em sala de aula, ou seja, o sistema deve permitir que os professores reservem horários para utilizar os laboratórios disponíveis, além de permitir a reserva de laboratórios para atividades extras, como reuniões, cursos, palestras, etc.:

## O que deve ser entregue?

1. Criar a configuração inicial para a implementação de um projeto Django Django Rest que ofereça acesso a uma API em um banco de dados Postgres.
2. Criar os modelos de dados;
3. Criar os serializeres para os modelos;
4. Criar as views para os modelos;
5. Criar as rotas para os modelos;
6. Criar acesso a documentação da API usando Swagger;
7. Criar acesso a documentação da API usando Redoc;
8. Fazer os teste de API com o Postman ou algum outro software de sua preferência que possa testar as funções da API

Criar um arquivo README.md com as instruções de instalação e uso de acesso a API e suas respectivas funcionalidades.

**OBS: Neste primeiro momento não há necessidade de relacionar as tabelas. Os modelos devem ser independentes, sem interrelação.**