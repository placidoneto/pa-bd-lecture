# Certificação de Conhecimento - 2025.2

Link Assignment: https://classroom.github.com/a/FWp92XDa

# Certificação em Programação e Administração de Banco de Dados
## Sistema de Maquineta de Cartão - API de Pagamentos


Você foi contratado para desenvolver a API backend de um sistema de maquinetas de cartão. O sistema deve registrar transações de pagamento, gerenciar estabelecimentos comerciais e processar diferentes tipos de transações.

---

## Questão 1: Modelagem de Dados (10 pontos)

Crie os modelos Django para o sistema com os seguintes requisitos:

### Modelo `Estabelecimento`
- Nome do estabelecimento
- CNPJ (único)
- Endereço completo
- Taxa de serviço (decimal)
- Data de cadastro

### Modelo `Maquineta`
- Número de série (único)
- Estabelecimento vinculado (FK)
- Status (ativa/inativa/em_manutencao)
- Data de ativação

### Modelo `Transacao`
- Maquineta utilizada (FK)
- Valor da transação
- Tipo de pagamento (debito/credito/pix)
- Número de parcelas (quando aplicável)
- Status (pendente/aprovada/recusada/cancelada)
- NSU (número sequencial único)
- Data/hora da transação
- Dados do cartão (últimos 4 dígitos - mascarado)

**Entregável:** Código dos modelos em `models.py`

---

## Questão 2: Serializers (15 pontos)

Implemente os serializers para:

### `EstabelecimentoSerializer`
- Validação de CNPJ (14 dígitos numéricos)
- Campo `total_transacoes` (read-only) mostrando quantidade de transações
- Campo `valor_total_processado` (read-only)

### `TransacaoSerializer`
- Validação: parcelas apenas para crédito
- Validação: valor mínimo de R$ 1.00
- Método para calcular valor líquido (descontando taxa do estabelecimento)
- Campo nested com dados básicos da maquineta

### `TransacaoCreateSerializer`
- Serializer separado para criação
- Gerar NSU automaticamente
- Validar se maquineta está ativa

**Entregável:** Código dos serializers em `serializers.py`

---

## Questão 3: ViewSets e Rotas (25 pontos)

Implemente ViewSets com as seguintes funcionalidades:

### `EstabelecimentoViewSet`
- CRUD completo
- Filtro por CNPJ
- Busca por nome
- Action customizada: `@action` para relatório de transações do estabelecimento

### `TransacaoViewSet`
- Criar e listar transações
- Não permitir UPDATE de transações aprovadas
- Permitir DELETE apenas de transações pendentes
- Filtros: por estabelecimento, status, tipo de pagamento, período (data)
- Ordenação por data (mais recente primeiro)
- Action customizada: `cancelar_transacao` (POST) que muda status para cancelada

### Configurar URLs
- Usar DefaultRouter
- Endpoints REST completos

**Entregável:** `views.py` e `urls.py`

---

## Questão 4: Autenticação e Permissões (20 pontos)

Implemente:

### Autenticação
- Token Authentication
- Cada estabelecimento tem um usuário associado

### Permissões Customizadas
- Transações só podem ser criadas pela maquineta vinculada ao estabelecimento autenticado
- Administradores podem ver tudo

### Configuração
- Configurar permissões nos ViewSets

**Entregável:** `permissions.py` e configurações em `views.py`

---

## Questão 5: Filtragem Avançada com Django Filter (15 pontos)

Implemente filtros avançados utilizando `django-filter` para os endpoints principais:

### `TransacaoFilterSet`

Crie uma classe FilterSet customizada para transações com os seguintes filtros:

#### Filtros Básicos:
- **status**: Filtro exato por status da transação
- **tipo_pagamento**: Filtro exato por tipo (debito/credito/pix)
- **estabelecimento**: Filtro por ID ou CNPJ do estabelecimento
- **maquineta**: Filtro por número de série da maquineta

#### Filtros de Valor:
- **valor_min**: Transações com valor maior ou igual
- **valor_max**: Transações com valor menor ou igual
- **valor_range**: Filtro de faixa de valores (ex: `valor_min=100&valor_max=1000`)

#### Filtros de Data/Período:
- **data_inicio**: Transações a partir desta data
- **data_fim**: Transações até esta data
- **mes**: Filtro por mês específico (1-12)
- **ano**: Filtro por ano
- **ultimos_dias**: Transações dos últimos N dias (ex: `ultimos_dias=7`)

### Implementação nos ViewSets

Configure os ViewSets para usar os FilterSets:

### Exemplos de Uso da API

#### Exemplo 1: Buscar transações por período e valor
```
GET /api/transacoes/?data_inicio=2025-01-01&data_fim=2025-01-31&valor_min=100&valor_max=1000
```

#### Exemplo 2: Transações aprovadas dos últimos 7 dias
```
GET /api/transacoes/?status=aprovada&ultimos_dias=7
```

### Configuração no Settings

Adicione ao `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'django_filters',
    'rest_framework',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 50,
}
```

### Documentação da API

Documente os filtros disponíveis no README e usando ferramentas como Swagger/OpenAPI:

```markdown
## Filtros Disponíveis

### Endpoint: /api/transacoes/

| Parâmetro | Tipo | Descrição | Exemplo |
|-----------|------|-----------|---------|
| status | string | Status da transação | ?status=aprovada |
| tipo_pagamento | string | Tipo de pagamento | ?tipo_pagamento=credito |
| valor_min | decimal | Valor mínimo | ?valor_min=100.00 |
| valor_max | decimal | Valor máximo | ?valor_max=1000.00 |
| data_inicio | date | Data inicial | ?data_inicio=2025-01-01 |
| data_fim | date | Data final | ?data_fim=2025-12-31 |
```

**Entregável:** `filters.py` com as classes FilterSet, ViewSets configurados e testes dos filtros

---

## Questão 6: Otimizações e Boas Práticas (15 pontos)

### Documentação
- Usar Swagger e Redoc
- Usar Postgres para acesso ao Banco
- Testar a API usando um Frontend Python CLI

**Entregável:** Código documentado e CLI feito

---

## Estrutura de Entrega Esperada

```
projeto/
├── manage.py
├── requirements.txt
├── payment_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── transactions/
    ├── __init__.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── permissions.py
    ├── urls.py
    ├── tests.py
    └── admin.py
```

---

## Instruções de Submissão

1. Crie um repositório Git
2. Inclua arquivo `requirements.txt` com dependências
3. Inclua `README.md` com instruções de setup
4. Commit frequentes mostrando evolução
5. Código deve rodar com `python manage.py runserver`

---

## Dependências Esperadas no requirements.txt

```
Django>=4.2,<5.0
djangorestframework>=3.14
django-filter>=23.0
```

---

## Dicas Importantes

- Use `CharField` com `choices` para campos com opções fixas
- `DecimalField` para valores monetários (max_digits=10, decimal_places=2)
- Implemente `__str__` nos modelos para melhor visualização no admin
- Valide dados tanto no serializer quanto no modelo quando fizer sentido