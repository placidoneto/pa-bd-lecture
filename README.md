# L01 - Fundamentos SQL em PostgreSQL

### O que é o SQL?

**SQL (Structured Query Language)** é a linguagem padrão para gerenciar e manipular bancos de dados relacionais. O SQL é uma ferramenta indispensável para qualquer profissional que trabalha com dados. Sua versatilidade, poder e facilidade de uso fazem dele a linguagem padrão para interagir com bancos de dados relacionais. Aqui estão alguns conceitos básicos:

### Conceitos Básicos

- **Banco de Dados**: Conjunto organizado de dados armazenados e acessados eletronicamente.
- **Tabela**: Estrutura dentro de um banco de dados que armazena dados em linhas e colunas.
- **Linha (Registro)**: Uma única entrada em uma tabela.
- **Coluna (Campo)**: Um atributo de dados em uma tabela.- **Chave Primária**: Um identificador único para cada registro em uma tabela.
- **Chave Estrangeira**: Um campo que cria um relacionamento entre duas tabelas.


### Por que usar SQL? Uma Linguagem Essencial para Manipulação de Dados

- **Linguagem universal**: É amplamente utilizada em diversos sistemas gerenciadores de bancos de dados (SGBDs), como PostgreSQL, MySQL, Oracle, SQL Server, etc.

- **Facilidade de aprendizado**: Possui uma sintaxe relativamente simples e intuitiva, facilitando o aprendizado para pessoas com diferentes níveis de experiência.

- **Consultas eficientes**: Permite realizar consultas complexas e obter resultados precisos em grandes conjuntos de dados de forma rápida.
- **Agrupamento e agregação**: Funções como SUM, AVG, COUNT, GROUP BY e HAVING permitem realizar cálculos e análises estatísticas sobre os dados.

#### Criação de Banco de Dados e Tabelas

```sql
-- Criação de um banco de dados
CREATE DATABASE nome_do_banco;

-- Seleção de um banco de dados
\c nome_do_banco;

-- Criação de uma tabela
CREATE TABLE nome_da_tabela (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100),
    idade INT
);
```

#### Inserção de Dados

```sql
-- Inserção de dados em uma tabela
INSERT INTO nome_da_tabela (nome, idade) VALUES ('João', 30);
```

#### Consulta de Dados

```sql
-- Seleção de todos os dados de uma tabela
SELECT * FROM nome_da_tabela;

-- Seleção de dados com condição
SELECT * FROM nome_da_tabela WHERE idade > 25;
```

#### Atualização de Dados

```sql
-- Atualização de dados em uma tabela
UPDATE nome_da_tabela SET idade = 31 WHERE nome = 'João';
```

#### Exclusão de Dados

```sql
-- Exclusão de dados em uma tabela
DELETE FROM nome_da_tabela WHERE nome = 'João';
```

#### Alteração de Estrutura de Tabelas

```sql
-- Adição de uma nova coluna
ALTER TABLE nome_da_tabela ADD COLUMN email VARCHAR(100);

-- Exclusão de uma coluna
ALTER TABLE nome_da_tabela DROP COLUMN email;
```

### Funções de Agregação

```sql
-- Contagem de registros
SELECT COUNT(*) FROM nome_da_tabela;

-- Soma de valores
SELECT SUM(idade) FROM nome_da_tabela;

-- Média de valores
SELECT AVG(idade) FROM nome_da_tabela;
```

### Junções (Joins)

```sql
-- Junção interna
SELECT a.nome, b.idade
FROM tabela1 a
INNER JOIN tabela2 b ON a.id = b.id;

-- Junção externa
SELECT a.nome, b.idade
FROM tabela1 a
LEFT JOIN tabela2 b ON a.id = b.id;
```

### Subconsultas

```sql
-- Subconsulta em cláusula WHERE
SELECT nome FROM nome_da_tabela
WHERE idade > (SELECT AVG(idade) FROM nome_da_tabela);
```

## Aplicação de Venda de Veículos com PostgreSQL: Uma Visão Geral e Exemplos de Consultas SQL

Imagine uma aplicação web que permite a compra e venda de veículos. Essa aplicação seria construída com uma interface intuitiva, onde os usuários podem:

- **Cadastrar veículos**: Informando marca, modelo, ano, preço e outras características relevantes.
- **Pesquisar veículos**: Filtrando por diversos critérios, como marca, modelo, faixa de preço e ano.
- **Gerencia a venda dos veículos**: Realizar o registro de venda de um veículo para um cliente.

Ver código abaixo:

```sql
-- Criação das tabelas
CREATE TABLE Clientes (
    ClienteID SERIAL PRIMARY KEY,
    Nome VARCHAR(100),
    Email VARCHAR(100),
    Telefone VARCHAR(20)
);

CREATE TABLE Veiculos (
    VeiculoID SERIAL PRIMARY KEY,
    Marca VARCHAR(50),
    Modelo VARCHAR(50),
    Ano INT,
    Preco DECIMAL(10, 2)
);

CREATE TABLE Vendas (
    VendaID SERIAL PRIMARY KEY,
    ClienteID INT REFERENCES Clientes(ClienteID),
    VeiculoID INT REFERENCES Veiculos(VeiculoID),
    DataVenda DATE,
    ValorVenda DECIMAL(10, 2)
);
```

Agora vamos inserir alguns dados no banco de dados:
```sql
-- Inserção de dados nas tabelas
INSERT INTO Clientes (Nome, Email, Telefone) VALUES
('João Silva', 'joao.silva@example.com', '123456789'),
('Maria Oliveira', 'maria.oliveira@example.com', '987654321');

INSERT INTO Veiculos (Marca, Modelo, Ano, Preco) VALUES
('Toyota', 'Corolla', 2020, 75000.00),
('Honda', 'Civic', 2019, 70000.00);

INSERT INTO Vendas (ClienteID, VeiculoID, DataVenda, ValorVenda) VALUES
(1, 1, '2024-09-01', 75000.00),
(2, 2, '2024-09-05', 70000.00);

-- Consultas SQL
-- 1. Selecionar todos os clientes
SELECT * FROM Clientes;

-- 2. Selecionar todos os veículos disponíveis
SELECT * FROM Veiculos;

-- 3. Selecionar todas as vendas realizadas
SELECT * FROM Vendas;

-- 4. Selecionar vendas com detalhes do cliente e veículo
SELECT Vendas.VendaID, Clientes.Nome, Veiculos.Marca, Veiculos.Modelo, Vendas.DataVenda, Vendas.ValorVenda
FROM Vendas
JOIN Clientes ON Vendas.ClienteID = Clientes.ClienteID
JOIN Veiculos ON Vendas.VeiculoID = Veiculos.VeiculoID;
```

### Estrutura da Aplicação Web com Django Rest para a aplicação de Venda de Veículos

Vamos implementar uma simples aplicação usando Django Rest para manipular os dados de venda.

Estrutura de Diretórios
```
/venda_veiculos
    /static
    /templates
    __init__.py
    asgi.py
    settings.py
    urls.py
    wsgi.py
manage.py
```

### Passo a Passo
1. **Configuração Inicial**

   - Crie um novo projeto Django:

```
django-admin startproject venda_veiculos
cd venda_veiculos
```

   - Crie um novo aplicativo dentro do projeto:
```
python manage.py startapp core
```
2. **Configuração do PostgreSQL**
      - Instale o driver do PostgreSQL:
```
pip install psycopg2-binary
```
- Configure o banco de dados PostgreSQL no arquivo *venda_veiculos/settings.py*:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'nome_do_banco',
        'USER': 'seu_usuario',
        'PASSWORD': 'sua_senha',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **Modelos (Models)**

- Edite o arquivo *core/models.py* para definir as tabelas:

```python
from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=15)

    def __str__(self):
        return self.nome

class Veiculo(models.Model):
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    ano = models.IntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.marca} {self.modelo}"

class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    data_venda = models.DateTimeField(auto_now_add=True)
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venda de {self.veiculo} para {self.cliente}"
```

4. **Serializers**

- Crie o arquivo *core/serializers.py* e adicione os serializers:

```python
from rest_framework import serializers
from .models import Cliente, Veiculo, Venda

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class VeiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculo
        fields = '__all__'

class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = '__all__'
```

5. **Views**

- Edite o arquivo *core/views.py* para adicionar as views:

```python
from rest_framework import viewsets
from .models import Cliente, Veiculo, Venda
from .serializers import ClienteSerializer, VeiculoSerializer, VendaSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer

class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer

class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all()
    serializer_class = VendaSerializer

```

6. **URLs**

- Edite o arquivo *venda_veiculos/urls.py* para incluir as rotas:

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from core import views

router = DefaultRouter()
router.register(r'clientes', views.ClienteViewSet)
router.register(r'veiculos', views.VeiculoViewSet)
router.register(r'vendas', views.VendaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
```
7. **Configurações Finais**

- Adicione *rest_framework* e *core* ao *INSTALLED_APPS* no arquivo *venda_veiculos/settings.py*:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'core',
]
```

- Execute as migrações para criar as tabelas no banco de dados:

```python
python manage.py makemigrations
python manage.py migrate

```

8. **Testar a Aplicação**
- Inicie environment python para testar a aplicação:
  
```python
python3 -m venv env
source env/bin/activate

pip install django djangorestframework
pip install markdown       
pip install django-filter  
pip install psycopg2-binary
```

- Inicie o servidor de desenvolvimento:

```python
python manage.py runserver
```
- Acesse *http://127.0.0.1:8000/api/* para ver as APIs funcionando.


