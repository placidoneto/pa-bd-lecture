# TP - Atividade Prática: API de Gestão de Eventos Acadêmicos com Laravel

## Objetivo
Aplicar os conceitos fundamentais do framework **Laravel** (Rotas, Controllers, Migrations, Models e Eloquent ORM) para construir uma API RESTful. 

O sistema simulará o gerenciamento de eventos acadêmicos, onde **Participantes** podem realizar **Inscrições** em **Eventos**, desde que respeitem as regras de capacidade e datas.

## Tecnologias
- Linguagem: PHP 8.2+
- Framework: Laravel 10 ou 11
- Banco de Dados: MySQL ou PostgreSQL

---

## Entidades do Domínio

O sistema deve possuir obrigatoriamente as 3 tabelas abaixo, com os relacionamentos adequados.

### 1. Evento
Representa uma palestra, workshop ou curso.
- `id` (Primary Key)
- `titulo` (String) - *Obrigatório*
- `descricao` (String) - *Opcional*
- `data_evento` (DateTime) - *Obrigatório (deve ser uma data futura no cadastro)*
- `local` (String) - *Obrigatório*
- `capacidade_maxima` (Integer) - *Obrigatório (ex: 50 vagas)*

### 2. Participante
Representa o aluno ou pessoa externa interessada.
- `id` (Primary Key)
- `nome` (String) - *Obrigatório*
- `email` (String) - *Obrigatório e único*
- `cpf` (String) - *Obrigatório*

### 3. Inscricao
Representa o vínculo entre um participante e um evento.
- `id` (Primary Key)
- `evento_id` (Foreign Key -> Eventos)
- `participante_id` (Foreign Key -> Participantes)
- `data_inscricao` (DateTime) - *Gerada automaticamente no momento do cadastro*

---

### Estrutura de diretórios

```
projeto-eventos/
├── app/
│   ├── Http/
│   │   ├── Controllers/
│   │   │   ├── Controller.php
│   │   │   ├── EventoController.php          # CRUD de eventos
│   │   │   ├── ParticipanteController.php    # Gestão de participantes
│   │   │   └── InscricaoController.php        # Inscrições em eventos
│   │   │
│   │   └── Requests/                          # Validação de dados (opcional, recomendado)
│   │       ├── StoreEventoRequest.php         # Validação para criação de eventos
│   │       └── StoreInscricaoRequest.php      # Validação para inscrições
│   │
│   ├── Models/
│   │   ├── User.php                           # Usuário do sistema
│   │   ├── Evento.php                         # Entidade Evento
│   │   ├── Participante.php                   # Entidade Participante
│   │   └── Inscricao.php                      # Relação Evento x Participante
│   │
│   └── Services/                              # Camada de regras de negócio (opcional, recomendado)
│       └── InscricaoService.php               # Lógica de inscrição
│
├── database/
│   ├── factories/
│   │   └── EventoFactory.php                  # Geração de dados fictícios para testes
│   │
│   ├── migrations/
│   │   ├── 0001_01_01_000000_create_users_table.php
│   │   ├── xxxx_xx_xx_create_eventos_table.php
│   │   ├── xxxx_xx_xx_create_participantes_table.php
│   │   └── xxxx_xx_xx_create_inscricoes_table.php
│   │
│   └── seeders/
│       └── DatabaseSeeder.php                 # Popula o banco de dados
│
├── routes/
│   ├── web.php                                # Rotas web
│   └── api.php                                # Rotas da API
│
├── .env                                      # Variáveis de ambiente
├── composer.json                             # Dependências do projeto
└── README.md                                 
```



## Regras de Negócio (Obrigatórias)

Aqui está a lógica que diferencia este trabalho de um CRUD simples. Você deve implementar essas validações no seu Controller ou Service.

1.  **Limite de Vagas:** Antes de confirmar uma inscrição, o sistema deve verificar se o número de inscritos no evento é menor que a `capacidade_maxima`. Caso contrário, deve retornar erro indicando "Evento Lotado" (HTTP 400 ou 422).
2.  **Duplicidade:** Um mesmo participante não pode se inscrever duas vezes no mesmo evento.
3.  **Data do Evento:** Não deve ser possível criar inscrições para eventos que já aconteceram (data passada).
4.  **Validação de Dados:** Utilize `FormRequests` do Laravel para validar campos obrigatórios e formatos (ex: e-mail válido).

---

## Endpoints da API

Abaixo estão as rotas mínimas que a API deve responder.

### Eventos
- `GET /api/eventos` - Lista todos os eventos.
- `GET /api/eventos/{id}` - Detalhes de um evento.
- `POST /api/eventos` - Cadastra um novo evento.
- `PUT /api/eventos/{id}` - Atualiza dados do evento.
- `DELETE /api/eventos/{id}` - Cancela/Remove um evento (deve remover as inscrições atreladas ou impedir a deleção).

### Participantes
- `POST /api/participantes` - Cadastra um participante.
- `GET /api/participantes` - Lista participantes.

### Inscrições (O Core do Sistema)
- `POST /api/inscricoes` - Realiza a inscrição de um participante em um evento.
    - *Body esperado:* `{ "evento_id": 1, "participante_id": 5 }`
    - *Lógica:* Deve aplicar as regras de negócio descritas acima.
- `GET /api/eventos/{id}/participantes` - Lista todos os participantes inscritos em um evento específico.

---
