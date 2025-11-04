# TP4 1o Bimestre - Sistema de Gerenciamento de Hotel

**Disciplina:** Programação e Administração de Banco de Dados  
**Duração:** 3 horas (das 9h às 12h)  
**Modalidade:** Em dupla 
**Assignment:** https://classroom.github.com/a/SReEtNRx 
**Pontuação:** 40 pontos

---

## Informações Gerais

### Objetivos da Avaliação
- Avaliar a capacidade de modelagem de dados para sistemas reais
- Verificar o domínio de Django REST Framework
- Testar habilidades de implementação de regras de negócio
- Avaliar a capacidade de trabalho em equipe

### Orientações Importantes
- **Trabalho em dupla (opcional))**
- **Consulta permitida:** documentação oficial do Django/DRF, anotações pessoais
- **Consulta proibida:** internet (exceto documentação), comunicação com outras duplas
- **Entrega:** código fonte completo via GitHub Classroom
- **Plágio resultará em nota zero para todos os envolvidos**

---

## Cenário do Sistema

Você foi contratado para desenvolver um sistema de gerenciamento para a rede de hotéis **Grand Comfort Hotels**. O sistema deve gerenciar reservas de quartos, processos de check-in/check-out, solicitação de serviços adicionais e avaliações de estadias.

O sistema terá três tipos de usuários:
- **Hóspedes:** podem buscar quartos disponíveis, fazer reservas e solicitar serviços
- **Recepcionistas:** gerenciam check-in/check-out e visualizam todas as reservas
- **Gerentes:** têm acesso completo ao sistema incluindo relatórios e configurações

---

## Estrutura da Avaliação

### Questão 1 - Modelagem de Dados 

Implemente os modelos Django conforme a estrutura fornecida:

**a) Modelo Usuario**
- Estenda o modelo User ou AbstractUser do Django
- Adicione campo `tipo` com choices (Hospede, Recepcionista, Gerente)
- Adicione campos relevantes: CPF, telefone, data_nascimento

**b) Modelos de Quarto**
- Implemente `TipoQuarto` com todos os campos especificados
- Implemente `Quarto` com relacionamento adequado
- Configure choices para status do quarto

**c) Modelo Reserva**
- Implemente com todos os relacionamentos
- Configure choices para status da reserva
- Adicione validações básicas no modelo

**d) Modelos de Serviços**
- Implemente `ServicoAdicional` e `SolicitacaoServico`
- Configure relacionamentos adequados

**Critérios de Avaliação:**
- Nomenclatura correta dos campos 
- Tipos de campos apropriados 
- Relacionamentos corretos 
- Configuração de choices 
- Método __str__  
- Validações no modelo 
- Migrations funcionais 

---

### Questão 2 - Serializers 

Crie serializers para manipulação de dados via API:

**a) Serializers Básicos**
- `TipoQuartoSerializer`: todos os campos
- `QuartoSerializer`: incluir dados do tipo aninhado
- `ServicoAdicionalSerializer`: todos os campos

**b) ReservaSerializer**
- Campos read-only: hospede (preencher automaticamente), valor_total, status inicial
- Campos write-only quando apropriado
- Validação customizada:
  - Data check-in não pode ser no passado
  - Data check-out deve ser posterior ao check-in
  - Número de hóspedes não pode exceder capacidade do quarto
  - Quarto deve estar disponível no período

**Critérios de Avaliação:**
- Estrutura correta dos serializers 
- Campos aninhados adequados
- Validações implementadas 

---

### Questão 3 - Views e Endpoints 

Implemente as views utilizando ViewSets ou APIViews:

**a) QuartoViewSet**
- Listar quartos com filtros (tipo, status, capacidade mínima)
- Detalhes de um quarto específico
- Action customizada `disponibilidade`:
  - Parâmetros: data_inicio, data_fim
  - Retorna quartos disponíveis no período

**b) ReservaViewSet**
- CRUD completo de reservas
- Filtros: hospede, status, período
- Permissions: 
  - Hóspede vê apenas suas reservas
  - Recepcionista e Gerente veem todas
- Actions customizadas:
  - `fazer_checkin`: muda status para Checkin (apenas Recepcionista/Gerente)
  - `fazer_checkout`: muda status para Checkout e libera quarto
  - `cancelar`: implementa cancelamento com validações

**c) SolicitacaoServicoViewSet**
- Criar solicitação vinculada a uma reserva
- Listar solicitações (filtrar por reserva)
- Atualizar status (apenas Recepcionista/Gerente)

**Critérios de Avaliação:**
- Estrutura correta das views 
- Implementação de filtros 
- Actions customizadas funcionais 
- Permissions adequadas 
- Tratamento de exceções 
- Responses HTTP corretos 
---

### Questão 4 - Regras de Negócio 

Implemente as seguintes regras de negócio:

**a) Validação de Disponibilidade **
- Ao criar/editar reserva, verificar se quarto está disponível
- Considerar reservas existentes no período
- Impedir reserva de quarto em manutenção

**b) Cálculo de Valor Total**
- Calcular automaticamente valor_total da reserva:
  - valor_total = (data_checkout - data_checkin) × preco_diaria
- Atualizar ao salvar reserva

**c) Política de Cancelamento**
- Permitir cancelamento apenas se status for Pendente ou Confirmada
- Se cancelamento com menos de 48h da data_checkin:
  - Adicionar campo `valor_reembolso` (50% do valor_total)
- Se cancelamento com mais de 48h:
  - valor_reembolso = 100% do valor_total

**d) Controle de Check-in/Check-out**
- Check-in apenas se:
  - Status da reserva = Confirmada
  - Data atual = data_checkin
- Check-out atualiza status do quarto para Disponível
- Após checkout, permitir criação de Avaliacao

**Critérios de Avaliação:**
- Validação de disponibilidade correta 
- Política de cancelamento implementada
- Lógica de check-in/check-out 
---


## Checklist de Entrega

- [ ] Código executa sem erros
- [ ] Migrations criadas e aplicadas
- [ ] Models com relacionamentos corretos
- [ ] Serializers com validações
- [ ] ViewSets com actions customizadas
- [ ] Regras de negócio funcionando
- [ ] README com instruções
- [ ] requirements.txt atualizado

---

## 📝 Critérios de Correção

| Aspecto | Pontuação |
|---------|-----------|
| Questão 1 - Modelagem | 5 |
| Questão 2 - Serializers | 5 |
| Questão 3 - Views e Endpoints | 15 |
| Questão 4 - Regras de Negócio | 15 |
| **TOTAL** | **40** |


---

## Dicas Importantes

1. **Leiam todo o enunciado antes de começar**
2. **Organizem as tarefas entre a dupla**
3. **Façam commits frequentes (se usar Git)**
4. **Não deixem migrations para o final**
5. **Usem o admin do Django para validar dados**

---
