# Sistema de Vendas - Documentação do Script SQL

Este documento explica detalhadamente cada seção do arquivo `ddl_dml_vendas.sql`, que implementa a estrutura básica de um sistema de vendas.

## Estrutura do Banco de Dados

O sistema é composto por 4 tabelas principais que representam as entidades fundamentais de um sistema de e-commerce:

- **usuario**: Cadastro dos clientes
- **produto**: Catálogo de produtos
- **pedido**: Registro dos pedidos realizados
- **itens_pedido**: Detalhamento dos produtos em cada pedido

---

## Explicação Detalhada do Script

### 1. **Remoção de Tabelas Existentes**

```sql
DROP TABLE IF EXISTS itens_pedido;
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS produto;
DROP TABLE IF EXISTS usuario;
```

**Propósito**: Remove as tabelas se já existirem, permitindo recriar a estrutura do zero.

**Ordem**: A ordem de remoção é **inversa** à ordem de criação devido às dependências (chaves estrangeiras). As tabelas filhas devem ser removidas antes das tabelas pai.

---

### 2. **Tabela USUARIO**

```sql
CREATE TABLE usuario (
    id_usuario INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    telefone VARCHAR(20),
    endereco TEXT,
    data_nascimento DATE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE
);
```

**Campos Principais**:

- `id_usuario`: Chave primária com auto incremento
- `nome`: Nome completo do usuário (obrigatório)
- `email`: Email único para login/identificação
- `telefone`: Contato telefônico (opcional)
- `endereco`: Endereço completo em formato texto
- `data_nascimento`: Data de nascimento para validações de idade
- `data_cadastro`: Timestamp automático do momento do cadastro
- `ativo`: Flag para soft delete (desativar sem excluir)

**Constraints**:

- Email deve ser único (`UNIQUE`)
- Nome e email são obrigatórios (`NOT NULL`)

---

### 3. **Tabela PRODUTO**

```sql
CREATE TABLE produto (
    id_produto INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(150) NOT NULL,
    descricao TEXT,
    categoria VARCHAR(50),
    preco DECIMAL(10,2) NOT NULL CHECK (preco >= 0),
    quantidade_estoque INT DEFAULT 0 CHECK (quantidade_estoque >= 0),
    peso DECIMAL(8,3),
    dimensoes VARCHAR(50),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ativo BOOLEAN DEFAULT TRUE
);
```

**Campos Principais**:

- `id_produto`: Chave primária com auto incremento
- `nome`: Nome do produto (obrigatório)
- `descricao`: Descrição detalhada em formato texto
- `categoria`: Classificação do produto
- `preco`: Valor com 2 casas decimais, deve ser positivo
- `quantidade_estoque`: Controle de estoque, não pode ser negativo
- `peso`: Peso em kg para cálculo de frete
- `dimensoes`: Dimensões para logística
- `data_cadastro`: Timestamp automático
- `ativo`: Controle de produtos ativos/inativos

**Constraints**:

- Preço deve ser maior ou igual a zero (`CHECK (preco >= 0)`)
- Estoque não pode ser negativo (`CHECK (quantidade_estoque >= 0)`)

---

### 4. **Tabela PEDIDO**

```sql
CREATE TABLE pedido (
    id_pedido INT PRIMARY KEY AUTO_INCREMENT,
    id_usuario INT NOT NULL,
    data_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status_pedido ENUM('pendente', 'confirmado', 'processando', 'enviado', 'entregue', 'cancelado') DEFAULT 'pendente',
    valor_total DECIMAL(12,2) DEFAULT 0.00 CHECK (valor_total >= 0),
    endereco_entrega TEXT NOT NULL,
    observacoes TEXT,
    data_entrega_prevista DATE,
    data_entrega_real DATE,
  
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE RESTRICT
);
```

**Campos Principais**:

- `id_pedido`: Chave primária com auto incremento
- `id_usuario`: Referência ao cliente que fez o pedido
- `data_pedido`: Timestamp automático da criação
- `status_pedido`: Estado atual do pedido (ENUM com valores predefinidos)
- `valor_total`: Soma total do pedido (calculado pelos triggers)
- `endereco_entrega`: Endereço específico para entrega
- `observacoes`: Informações adicionais do cliente
- `data_entrega_prevista`: Data estimada de entrega
- `data_entrega_real`: Data efetiva da entrega

**Relacionamentos**:

- Chave estrangeira para `usuario` com `ON DELETE RESTRICT` (impede excluir usuário com pedidos)

**Status do Pedido**:

- `pendente`: Aguardando confirmação
- `confirmado`: Pedido confirmado
- `processando`: Em preparação
- `enviado`: A caminho
- `entregue`: Finalizado
- `cancelado`: Cancelado

---

### 5. **Tabela ITENS_PEDIDO**

```sql
CREATE TABLE itens_pedido (
    id_item INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    preco_unitario DECIMAL(10,2) NOT NULL CHECK (preco_unitario >= 0),
    subtotal DECIMAL(12,2) GENERATED ALWAYS AS (quantidade * preco_unitario) STORED,
  
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto) ON DELETE RESTRICT,
  
    UNIQUE KEY unique_pedido_produto (id_pedido, id_produto)
);
```

**Campos Principais**:

- `id_item`: Chave primária com auto incremento
- `id_pedido`: Referência ao pedido
- `id_produto`: Referência ao produto
- `quantidade`: Quantidade solicitada (deve ser maior que zero)
- `preco_unitario`: Preço do produto no momento do pedido
- `subtotal`: Valor calculado automaticamente (quantidade × preço_unitario)

**Relacionamentos**:

- FK para `pedido` com `ON DELETE CASCADE` (remove itens se pedido for excluído)
- FK para `produto` com `ON DELETE RESTRICT` (impede excluir produto com pedidos)

**Constraints Especiais**:

- `UNIQUE KEY unique_pedido_produto`: Impede adicionar o mesmo produto duas vezes no mesmo pedido
- `GENERATED ALWAYS AS`: Campo calculado automaticamente pelo banco

---

## Dados de Exemplo (DML)

### Usuários de Teste

```sql
INSERT INTO usuario (nome, email, telefone, endereco, data_nascimento) VALUES
('João Silva', 'joao.silva@email.com', '(11) 99999-1111', 'Rua A, 123, São Paulo - SP', '1990-05-15'),
('Maria Santos', 'maria.santos@email.com', '(11) 99999-2222', 'Av. B, 456, São Paulo - SP', '1985-08-20'),
('Pedro Oliveira', 'pedro.oliveira@email.com', '(11) 99999-3333', 'Rua C, 789, São Paulo - SP', '1992-12-10');
```

**Propósito**: Cria usuários de exemplo para testar o sistema.

### Produtos de Teste

```sql
INSERT INTO produto (nome, descricao, categoria, preco, quantidade_estoque, peso) VALUES
('Smartphone Galaxy', 'Smartphone Android com 128GB', 'Eletrônicos', 1200.00, 50, 0.200),
('Notebook Dell', 'Notebook Intel i5, 8GB RAM, 256GB SSD', 'Informática', 2500.00, 20, 2.100),
('Tênis Nike Air', 'Tênis esportivo para corrida', 'Calçados', 350.00, 100, 0.800),
('Livro Python', 'Livro sobre programação em Python', 'Livros', 89.90, 30, 0.500),
('Mouse Gamer', 'Mouse óptico para jogos', 'Informática', 120.00, 75, 0.150);
```

**Propósito**: Cria um catálogo diversificado com diferentes categorias e preços.

### Pedidos e Itens de Teste

```sql
-- Pedidos
INSERT INTO pedido (id_usuario, endereco_entrega, observacoes) VALUES
(1, 'Rua A, 123, São Paulo - SP', 'Entregar no período da manhã'),
(2, 'Av. B, 456, São Paulo - SP', 'Apartamento 302'),
(1, 'Rua A, 123, São Paulo - SP', 'Presente de aniversário');

-- Itens dos pedidos
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(1, 1, 1, 1200.00),  -- João: 1 Smartphone
(1, 5, 2, 120.00),   -- João: 2 Mouses
(2, 2, 1, 2500.00),  -- Maria: 1 Notebook
(2, 3, 1, 350.00),   -- Maria: 1 Tênis
(3, 4, 3, 89.90);    -- João: 3 Livros
```

**Cenários Criados**:

- **Pedido 1**: João compra smartphone + mouses (valor total: R$ 1.440,00)
- **Pedido 2**: Maria compra notebook + tênis (valor total: R$ 2.850,00)
- **Pedido 3**: João compra livros como presente (valor total: R$ 269,70)

---

## Recursos Avançados

### Campos Calculados

- `subtotal` na tabela `itens_pedido`: Calculado automaticamente como `quantidade × preco_unitario`
- `valor_total` no `pedido`: Atualizado automaticamente via triggers

### Integridade Referencial

- **RESTRICT**: Impede exclusão de registros referenciados
- **CASCADE**: Remove registros dependentes automaticamente

### Validações (CHECK Constraints)

- Preços não podem ser negativos
- Quantidades devem ser positivas
- Estoque não pode ser negativo

### Controle de Estado

- Campo `ativo` para soft delete
- ENUM para status de pedidos com fluxo definido

---

## Casos de Uso

### Fluxo Típico de Pedido:

1. **Cliente se cadastra** → Inserção na tabela `usuario`
2. **Produtos são cadastrados** → Inserção na tabela `produto`
3. **Cliente faz pedido** → Inserção na tabela `pedido`
4. **Adiciona produtos ao pedido** → Inserção na tabela `itens_pedido`
5. **Sistema calcula totais** → Triggers atualizam automaticamente
6. **Pedido avança nos status** → Atualização do campo `status_pedido`

---

## Atividade Prática - 15 Exercícios de Consultas SQL

### **Instruções Gerais:**
- Desenvolva as consultas SQL para resolver cada problema proposto
- Use os dados de exemplo do arquivo `ddl_dml_vendas.sql` para testar
- Organize suas consultas em um arquivo `.sql` com comentários
- Teste cada consulta antes de finalizar

---

#### **1. Listagem de Usuários Ativos**
Escreva uma consulta que exiba o ID, nome, email e telefone de todos os usuários que estão ativos no sistema.

#### **2. Catálogo de Produtos por Categoria**
Crie uma consulta que mostre todos os produtos da categoria 'Informática', exibindo nome, preço e quantidade em estoque. Ordene por preço crescente.

#### **3. Contagem de Pedidos por Status**
Desenvolva uma consulta que conte quantos pedidos existem para cada status diferente.

#### **4. Alerta de Estoque Baixo**
Faça uma consulta que identifique produtos com quantidade em estoque menor que 30 unidades. Mostre nome do produto, quantidade atual e categoria.

#### **5. Histórico de Pedidos Recentes**
Escreva uma consulta que liste todos os pedidos realizados nos últimos 60 dias, mostrando ID do pedido, data, valor total e status.

#### **6. Produtos Mais Caros por Categoria**
Crie uma consulta que mostre o produto mais caro de cada categoria, exibindo categoria, nome do produto e preço.

#### **7. Clientes com Dados de Contato Incompletos**
Desenvolva uma consulta para identificar usuários ativos que não possuem telefone cadastrado.

#### **8. Pedidos Pendentes de Entrega**
Faça uma consulta que liste todos os pedidos com status 'enviado', mostrando dados do cliente e endereço de entrega.

#### **9. Detalhamento Completo de Pedidos**
Crie uma consulta que mostre, para um pedido específico (ID = 1), todas as informações: dados do cliente, produtos comprados, quantidades, preços unitários e subtotais.

#### **10. Ranking dos Produtos Mais Vendidos**
Desenvolva uma consulta que liste os produtos ordenados pela quantidade total vendida (soma de todas as vendas). Mostre nome, categoria e total vendido.

#### **11. Análise de Clientes Sem Compras**
Escreva uma consulta que identifique todos os usuários ativos que nunca fizeram um pedido no sistema.

#### **12. Estatísticas de Compras por Cliente**
Crie uma consulta que calcule, para cada cliente que já fez pedidos: número total de pedidos, valor médio por pedido e valor total gasto.

#### **13. Relatório Mensal de Vendas**
Desenvolva uma consulta que agrupe as vendas por mês/ano, mostrando: período, quantidade de pedidos, número de produtos diferentes vendidos e faturamento total.

#### **14. Produtos que Nunca Foram Vendidos**
Faça uma consulta que identifique produtos ativos que nunca foram incluídos em nenhum pedido.

#### **15. Análise de Ticket Médio por Categoria**
Crie uma consulta que calcule o ticket médio (valor médio de venda) para cada categoria de produto, considerando apenas pedidos não cancelados.

---

## CLI em Python para Execução das Consultas

Foi desenvolvido um **CLI (Command Line Interface)** completo em Python para facilitar a execução e teste das 15 consultas SQL propostas. O sistema oferece uma interface organizada e intuitiva para que os alunos possam implementar e testar suas soluções.

### **Arquivos do CLI:**

#### **1. `sistema_vendas_cli.py`** - Programa Principal
Interface completa com menus organizados e todas as funções preparadas para implementação das consultas.

É necessário implementar as funções vazias. 