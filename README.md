# Trabalho Prático 3 - Relacionamentos em Django Rest

## Objetivo
O objetivo desta atividade é desenvolver um modelo de dados usando relacionamento entre as entidades. Toda aplicação deve ser desenvolvida após que o modelo conceitual e seus relacionamentos estão bem definidos.

## Descrição

Imagine que você identificou que o transporte publico de sua cidade é muito ruim e decidiu criar um aplicativo para ajudar as pessoas a se locomoverem. Você quer criar um aplicativo que permita que os usuários se cadastrem, comprarem seus tickets em um aplicativo de celular, ou computador.

Existem vários tipos de tickets, como por exemplo: avulso, diario, semanal,  mensal e anual. Cada ticket tem seu valor específico. Cada parada, onibus ou trem tem um validador de trajeto, que significa que o usuário pode validar seu ticket em qualquer um deles. A validação significa que o usuario está pagando o intinerário, o que é debitado algomaticamente da sua conta. Essa validação pode ser feita pelo proprio celular, ou um cartão de usuario. O mesmo ticket pode ser utilizado por 1 hora de trajeto. Assim, se o usuario qualquer intinerário durante 1 hora, nao importanto quantos transportes ele pegar. 

As empresas de transporte e o municipio consedente podem acompanhar quantos onibus, trens e paradas estão sendo utilizados, quantos tickets foram validados e quantos tickets foram comprados. Da mesma forma que o usuario pode acompanhar quantos tickets ele comprou, quantos tickets ele validou e quantos tickets ele ainda tem.

## Requisitos

- O sistema deve permitir o cadastro de usuários, com informações como nome, email, telefone e endereço.
- O sistema deve permitir o cadastro de tickets, com informações como tipo (avulso, diario, semanal, mensal e anual) e valor.
- O sistema deve permitir o cadastro de paradas, onibus e trens, com informações como nome, localização e tipo (parada, onibus ou trem).
- O sistema deve permitir o cadastro de validadores, com informações como nome, localização e tipo (celular ou cartão).
- O sistema deve permitir o cadastro de trajetos, com informações como origem, destino e tempo de validade do ticket.
- O sistema deve permitir o cadastro de validações, com informações como data e hora da validação, local, tipo de validador e tipo de ticket.
- O sistema deve permitir o cadastro de empresas de transporte, com informações como nome, CNPJ e endereço.
- O sistema deve permitir o cadastro de municípios, com informações como nome e endereço.
- O sistema deve permitir o cadastro de relatórios, com informações como quantidade de tickets comprados, validados e ainda disponíveis.


## Oque deve ser entregue 

1. Descrever o modelo de dados que atenda a descrição acima.
2. Cada elemento do modelo deve ser descrito com seus respectivos atributos;
    1. Cada elemento do modelo deve ser descrito com suas respectivas relações com outros elementos do modelo;
    2. O modelo de dados deve ser descrito em um arquivo README.md na raiz do projeto.
    3. Implementar o modelo de dados utilizando o Django ORM.
3. O modelo de dados deve ser implementado utilizando o Django ORM;
    1. O modelo de dados deve ser implementado em um arquivo models.py na raiz do projeto.
    2. Implementar uma API REST que permita a criação, leitura, atualização e exclusão de registros no banco de dados.
4. A API deve ser implementada utilizando o Django Rest Framework;
    1. Todas as operações devem ser realizadas via API usando o Swagger;
    2. A API deve ser implementada em um arquivo views.py na raiz do projeto.
    3. A API deve ser implementada em um arquivo urls.py na raiz do projeto.
    4. A API deve ser implementada em um arquivo serializers.py na raiz do projeto.
    5. Os endpoints para cada um dos requisitos devem ser definidos em um arquivo urls.py na raiz do projeto.
 5. **Link GithubClassroom: https://classroom.github.com/a/mCw8_de9**
 6. O projeto é em duplo, e ambos devem fazer commit e push no mesmo repositório, como critério de avaliação