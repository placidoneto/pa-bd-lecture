# Avalliação Final 1o Bimestre

## Instruções

- Não seguir alguma das regras na descrição desta atividade implicará em não correção da atividade.
- O trabalho pode ser feito em grupos de até 2 pessoas.
- O trabalho deve ser enviado via github-classroom.
- O trabalho deve ser feito em Python.
- Os membros do grupo devem enviar (commit e push), cada um, pelo menos a metade das questões abaixo.
- O link para o Assignment é: [Assignment Avaliação - 1o Bimestre] (https://classroom.github.com/a/LgclJO6E).
- O prazo de entrega é até o dia 10/12/2024 até às 12:00.
- O nome das equipes deem ser: avalicacao-nomeSobrenome-nomeSobrenome.

## Descritivo

Imagine que você foi contratado para implementar o novo sistema de uma clínica médica de atendimento multiprofissional. Os donos da clínica querem um sistema que seja capaz de armazenar informações sobre os pacientes, os profissionais que atendem na clínica e os atendimentos realizados. Cada paciente possui um prontuario eletrônico que contém informações pessoais, como nome, data de nascimento, endereço, telefone, e-mail, profissão, histórico de doenças, alergias, medicamentos em uso, e informações sobre o convênio médico. Cada profissional possui um cadastro com nome, data de nascimento, endereço, telefone, e-mail, formação, especialidade, e informações sobre o convênio médico. Cada atendimento possui um número de identificação, a data e hora do atendimento, o profissional que realizou o atendimento, o paciente atendido, o diagnóstico, e as prescrições médicas. Os atendimentos podem ser através de convênio médico ou particular. Os tipos de atendimento são: consulta ou exames. Todos os atendimentos são agendados previamente e não há atendimento de urgência na clinica.

A clinica tem todo cuidado com os dados e agendamentos de pacientes e profissionais, e por isso, deseja que o sistema seja capaz de armazenar as informações de forma segura e eficiente. 

A clínica deseja que o sistema seja capaz de realizar operações diversas que permitam o cadastro, a busca, a edição e a remoção de informações sobre os agendamentos, os pacientes, os profissionais e os atendimentos. Além disso, a clínica deseja que o sistema seja capaz de gerar relatórios diversos, como: a quantidade de atendimentos realizados por um profissional, a quantidade de atendimentos realizados por um paciente, a quantidade de atendimentos realizados em um determinado período, a quantidade de atendimentos realizados por convênio médico, a quantidade de atendimentos realizados por tipo de atendimento, a quantidade de atendimentos realizados por diagnóstico, a quantidade de atendimentos realizados por prescrição médica, entre outros.

## Requisitos de Implementação

- O sistema deve ser implementado em Python.
- A API (Backend) deve ser implementada utilizando Django Rest.
- O Front end deve ser implementado utilizando o terminal de comando a primeira versão do sistema.
- Além dos endpoints de CRUD para os modelos da aplicação, o sistema deve possuir endpoints para os relatórios solicitados (mínimo de 6 novos endpoints).
- O frontend deve ser capaz de consumir os endpoints da API e exibir as informações de forma clara e organizada.
- O frontend deve ser mostrar apenas as funções dos endpoints NÃO CRUD dos modelos da aplicação.
- As funções de CRUD podem ser utulizadas através do swagger.

## Entrega

- O trabalho deve ser entregue via GitHub Classroom, em um repositório da dupla. O repositório deve conter o código fonte do projeto (backend e frontend), o arquivo README.md na raiz do projeto com a descrição do modelo de dados, e a descrição de de seus atributos e suas relações.
