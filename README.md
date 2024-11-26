# Trabalho Prático de Desenvolvimento de Software para Persistência usando ORM e Djamgp Rest Framework

## Objetivo

O objetivo deste trabalho é desenvolver uma um modelo de dados, e uma primeira versão de uma API REST para acesso aos dados. A aplicação deve permitir a criação, leitura, atualização e exclusão de registros em um banco de dados.


## Descrição

Imagine um prestador de serviço que deseja manter um registro de seus clientes e dos serviços que presta a eles. Esse prestador pode ser qualquer um de sua escolha, e você deve considerar esse contexto escolhido para implementação dos prõximos passos. Exemplo de possíveis prestadores de serviço: `Eletricista, Encanador, Filme Maker, Doceiro(a), Boleiro(a), Fotógrafo(a), etc`. A escolha do tipo de prestador deve ser justificada no momento da descrição do modelo de dados (_ver descrição dos requisitos de entrega abaixo_) O prestador tem vários possíveis clientes. Cada cliente pode ter um ou mais serviços contratados. Cada serviço prestado deve ter um valor associado, com sua respectiva data, valor total do serviço, além de uma descrição do serviço prestado. Cada cliente deve ter um nome, um endereço, um telefone de contato, como também eventual informação de rede social (instagram, facebook, etc.). Cada serviço prestado deve ter uma descrição e uma data de realização. O prestador de serviço precisa ter todo o controle dos clientes, serviços prestados e valores recebidos. O prestador também precisa ter um controle de quanto ele já recebeu de cada cliente, e quanto ele já recebeu no total. O prestador também precisa ter um controle de quanto ele já prestou de serviço para cada cliente, e quanto ele já prestou no total, seja por mês ou por ano. O prestador do serviço precisa também saber qual tipo de situação ocorreu em cada serviço prestado, se foi pago, se está em aberto, se foi cancelado, etc. Eventualmente o prestador também precisa saber qual a relação entre os cliente. Se cliente A é uma indicação do cliente B, por exemplo. Ou ainda se o cliente A é um parente do cliente B, e se for parente, qual o tipo de parentesco.

## Requisitos de Entrega do Trabalho Prático

1. Implementar um modelo de dados que atenda a descrição acima.
   1. Cada elemento do modelo deve ser descrito com seus respectivos atributos;
   2. Cada elemento do modelo deve ser descrito com suas respectivas relações com outros elementos do modelo;
   3. O modelo de dados deve ser descrito em um arquivo `README.md` na raiz do projeto.
2. Implementar uma API REST que permita a criação, leitura, atualização e exclusão de registros no banco de dados.
   1. A API deve ser implementada utilizando o Django Rest Framework;
   2. Todas as operações devem ser realizadas via API usando o Swagger;

## Entrega

O trabalho deve ser entregue via GitHub Classroom, em um repositório privado. O repositório deve conter o código fonte do projeto, e um arquivo `README.md` na raiz do projeto com a descrição do modelo de dados.
