-- ==========================================
-- Sistema de Vendas - DDL e DML
-- Criação das tabelas básicas
-- ==========================================

-- Remover tabelas se já existirem (ordem inversa das dependências)
DROP TABLE IF EXISTS itens_pedido;
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS produto;
DROP TABLE IF EXISTS usuario;

-- ==========================================
-- TABELA: USUARIO
-- ==========================================
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

-- ==========================================
-- TABELA: PRODUTO
-- ==========================================
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

-- ==========================================
-- TABELA: PEDIDO
-- ==========================================
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
    
    -- Chave estrangeira
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE RESTRICT
);

-- ==========================================
-- TABELA: ITENS_PEDIDO
-- ==========================================
CREATE TABLE itens_pedido (
    id_item INT PRIMARY KEY AUTO_INCREMENT,
    id_pedido INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL CHECK (quantidade > 0),
    preco_unitario DECIMAL(10,2) NOT NULL CHECK (preco_unitario >= 0),
    subtotal DECIMAL(12,2) GENERATED ALWAYS AS (quantidade * preco_unitario) STORED,
    
    -- Chaves estrangeiras
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto) ON DELETE RESTRICT,
    
    -- Índice único para evitar duplicação de produto no mesmo pedido
    UNIQUE KEY unique_pedido_produto (id_pedido, id_produto)
);



-- ==========================================
-- DADOS DE EXEMPLO (DML)
-- ==========================================

-- Inserir usuários
INSERT INTO usuario (nome, email, telefone, endereco, data_nascimento) VALUES
('João Silva', 'joao.silva@email.com', '(11) 99999-1111', 'Rua A, 123, São Paulo - SP', '1990-05-15'),
('Maria Santos', 'maria.santos@email.com', '(11) 99999-2222', 'Av. B, 456, São Paulo - SP', '1985-08-20'),
('Pedro Oliveira', 'pedro.oliveira@email.com', '(11) 99999-3333', 'Rua C, 789, São Paulo - SP', '1992-12-10');

-- Inserir produtos
INSERT INTO produto (nome, descricao, categoria, preco, quantidade_estoque, peso) VALUES
('Smartphone Galaxy', 'Smartphone Android com 128GB', 'Eletrônicos', 1200.00, 50, 0.200),
('Notebook Dell', 'Notebook Intel i5, 8GB RAM, 256GB SSD', 'Informática', 2500.00, 20, 2.100),
('Tênis Nike Air', 'Tênis esportivo para corrida', 'Calçados', 350.00, 100, 0.800),
('Livro Python', 'Livro sobre programação em Python', 'Livros', 89.90, 30, 0.500),
('Mouse Gamer', 'Mouse óptico para jogos', 'Informática', 120.00, 75, 0.150);

-- Inserir pedidos
INSERT INTO pedido (id_usuario, endereco_entrega, observacoes) VALUES
(1, 'Rua A, 123, São Paulo - SP', 'Entregar no período da manhã'),
(2, 'Av. B, 456, São Paulo - SP', 'Apartamento 302'),
(1, 'Rua A, 123, São Paulo - SP', 'Presente de aniversário');

-- Inserir itens dos pedidos
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(1, 1, 1, 1200.00),  -- João comprou 1 Smartphone
(1, 5, 2, 120.00),   -- João comprou 2 Mouses
(2, 2, 1, 2500.00),  -- Maria comprou 1 Notebook
(2, 3, 1, 350.00),   -- Maria comprou 1 Tênis
(3, 4, 3, 89.90);    -- João comprou 3 Livros
