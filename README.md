# TP2 - 2025.2 Sistema Bancário

Link Assignment: https://classroom.github.com/a/cVxn4hMj

## Descrição do Problema

Imagine que um banco nacional solicitou para que você desenvolvesse um sistema de gerenciamento bancário para modernizar suas operações. O problema é que o banco não possui um sistema que permita o controle adequado de agências, contas, clientes e transações financeiras, o que leva a inconsistências nos dados e dificuldades no atendimento aos clientes.

A diretoria do banco decidiu criar um sistema de gestão bancária, onde será possível cadastrar agências, abrir contas para clientes, registrar depósitos, saques e transferências entre contas. O sistema deve garantir a rastreabilidade de todas as operações financeiras realizadas.


## Contexto do Sistema

O sistema bancário deve gerenciar os seguintes elementos:

### Agências
Cada agência bancária possui:
- Código da agência (único)
- Nome da agência
- Endereço completo
- Telefone de contato
- Gerente responsável
- Status (ativa ou inativa)

### Clientes
Cada cliente do banco possui:
- CPF (único)
- Nome completo
- Data de nascimento
- Endereço
- Telefone
- Email
- Data de cadastro
- Status (ativo ou inativo)

### Contas
Cada conta bancária possui:
- Número da conta (único)
- Código da agência
- CPF do titular
- Tipo de conta (Corrente, Poupança, Salário)
- Saldo atual
- Data de abertura
- Status (ativa, bloqueada ou encerrada)
- Limite de saque diário

### Depósitos
Cada operação de depósito registra:
- Número da conta
- Valor do depósito
- Data e hora da operação
- Tipo de depósito (Dinheiro, Cheque, Transferência, PIX)
- Descrição/observações
- Caixa/operador responsável

### Saques
Cada operação de saque registra:
- Número da conta
- Valor do saque
- Data e hora da operação
- Local do saque (Caixa, Caixa Eletrônico)
- Caixa/operador responsável (se aplicável)
- Status da operação (Aprovado, Negado)

### Transferências
Cada transferência entre contas registra:
- Número da conta de origem
- Número da conta de destino
- Valor da transferência
- Data e hora da operação
- Tipo de transferência (TED, DOC, PIX, Transferência Interna)
- Descrição/finalidade
- Status da operação (Processando, Concluída, Falhou)

O sistema bancário segue diferentes fluxos de operação:

1. **Fluxo de Cadastro**: Registro de agências, clientes e abertura de contas
2. **Fluxo de Depósitos**: Registro de entrada de valores nas contas
3. **Fluxo de Saques**: Registro de retirada de valores das contas
4. **Fluxo de Transferências**: Movimentação de valores entre diferentes contas

## Fluxos do Sistema

O sistema bancário segue diferentes fluxos de operação:

1. **Fluxo de Cadastro**: Registro de agências, clientes e abertura de contas
2. **Fluxo de Depósitos**: Registro de entrada de valores nas contas
3. **Fluxo de Saques**: Registro de retirada de valores das contas
4. **Fluxo de Transferências**: Movimentação de valores entre diferentes contas

## Requisitos do Trabalho Prático

Para a criação da primeira versão da API, considere o que foi trabalhado em sala de aula. O sistema deve permitir o gerenciamento completo de todas as entidades do banco:

### 1. Configuração Inicial
- Criar a configuração inicial para a implementação de um projeto Django com Django Rest Framework
- Configurar acesso a um banco de dados PostgreSQL
- Configurar as variáveis de ambiente necessárias

### 2. Modelos de Dados
Criar os modelos Django para:
- Agência
- Cliente
- Conta
- Depósito
- Saque
- Transferência

### 3. Serializers
- Criar serializers para todos os modelos criados
- Implementar validações básicas nos serializers

### 4. Views
- Criar views (ViewSets ou APIViews) para todos os modelos
- Implementar operações CRUD (Create, Read, Update, Delete)

### 5. Rotas
- Configurar as rotas da API usando o Router do DRF
- Seguir o padrão RESTful para nomenclatura das rotas

### 6. Documentação
- Configurar e disponibilizar documentação da API usando **Swagger**
- Configurar e disponibilizar documentação da API usando **Redoc**

### 7. Testes
- Realizar testes de todas as funcionalidades da API usando Swagger ou um Frontend CLI

### 8. README
- O arquivo README.md do seu repositório deve conter:
  - Descrição do projeto
  - Descrição dos modelos
  - Descrição dos endpoints
- 
## Observações Importantes

**OBS 1**: Neste primeiro momento **não há necessidade de relacionar as tabelas**. Os modelos devem ser independentes, sem interrelação via ForeignKey ou relacionamentos do Django ORM.

**OBS 2**: Os campos que referenciam outras entidades (como "código da agência" em Conta, ou "número da conta" em Depósito) devem ser implementados como campos simples (CharField, IntegerField, etc.), não como chaves estrangeiras.

**OBS 3**: As validações de negócio (como verificar se uma conta existe antes de fazer um depósito) **não são necessárias nesta primeira versão**. O foco é na estrutura básica da API.

## Entrega

O trabalho deve ser entregue através do GitHub Classroom no link fornecido acima. 

Certifique-se de que:

1. O código está completo e funcional
2. O README.md possui todas as instruções necessárias
3. A API está devidamente documentada