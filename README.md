# Avaliação Prática - Django REST Framework
## Sistema de Gerenciamento de Oficina Mecânica

### Informações Gerais
**Disciplina:** Programação e Administração de Banco de Dados  
**Duração:** 3 horas (das 9h às 12h)  
**Assignment:** [https://classroom.github.com/a/SReEtNRx](https://classroom.github.com/a/SReEtNRx)  
**Pontuação:** 40 pontos

### Objetivos
- Avaliar a capacidade de modelagem de dados para sistemas reais
- Verificar o domínio de Django REST Framework
- Testar habilidades de implementação de regras de negócio
- Avaliar a capacidade de trabalho em equipe

### Regras Importantes
- Consulta permitida: documentação oficial do Django/DRF, anotações pessoais
- Consulta proibida: internet (exceto documentação), comunicação com outras pessoas
- Entrega: código fonte completo via GitHub Classroom
- Plágio resultará em nota zero para todos os envolvidos

---

## Contexto do Sistema

Você foi contratado para desenvolver um sistema de gerenciamento para a rede de oficinas **AutoTech Solutions**. O sistema deve gerenciar o estoque de peças, orçamentos de serviços, consertos de veículos e controle de mão de obra.

### Tipos de Usuários

O sistema terá três tipos de usuários:
- **Clientes:** podem visualizar seus veículos, orçamentos e histórico de serviços
- **Mecânicos:** gerenciam consertos, solicitam peças e atualizam status de serviços
- **Gerentes:** têm acesso completo ao sistema incluindo relatórios e configurações

---

## Questão 1 - Modelagem de Dados (5 pontos)

Implemente os modelos Django conforme a estrutura fornecida:

### a) Modelo Usuario
- Estenda o modelo User ou AbstractUser do Django
- Adicione campo `tipo` com choices (Cliente, Mecanico, Gerente)
- Adicione campos relevantes: CPF, telefone, data_nascimento

### b) Modelos de Veículo
- Implemente `Veiculo` com campos:
  - `placa` (CharField, unique)
  - `marca` (CharField)
  - `modelo` (CharField)
  - `ano` (IntegerField)
  - `cor` (CharField)
  - `cliente` (ForeignKey para Usuario)
  - `observacoes` (TextField, blank=True)

### c) Modelo Peca
- Implemente com campos:
  - `codigo` (CharField, unique)
  - `nome` (CharField)
  - `descricao` (TextField)
  - `fabricante` (CharField)
  - `quantidade_estoque` (IntegerField, default=0)
  - `preco_unitario` (DecimalField)
  - `estoque_minimo` (IntegerField, default=5)
  - `status` (CharField com choices: Disponivel, Esgotado, Descontinuado)

### d) Modelo Orcamento
- Implemente com todos os relacionamentos:
  - `veiculo` (ForeignKey)
  - `mecanico_responsavel` (ForeignKey para Usuario)
  - `data_criacao` (DateTimeField, auto_now_add)
  - `data_validade` (DateField)
  - `descricao_problema` (TextField)
  - `valor_mao_obra` (DecimalField)
  - `valor_pecas` (DecimalField, default=0)
  - `valor_total` (DecimalField)
  - `status` (CharField com choices: Pendente, Aprovado, Rejeitado, Expirado)
  - `observacoes` (TextField, blank=True)

### e) Modelos de Serviço
- Implemente `OrdemServico`:
  - `orcamento` (OneToOneField)
  - `data_inicio` (DateTimeField)
  - `data_previsao` (DateField)
  - `data_conclusao` (DateTimeField, null=True)
  - `status` (CharField com choices: Aguardando, EmAndamento, AguardandoPecas, Concluido, Cancelado)
  - `km_entrada` (IntegerField)
  
- Implemente `ItemPeca`:
  - `ordem_servico` (ForeignKey)
  - `peca` (ForeignKey)
  - `quantidade` (IntegerField)
  - `preco_unitario_cobrado` (DecimalField)

### Critérios de Avaliação:
- Nomenclatura correta dos campos
- Tipos de campos apropriados
- Relacionamentos corretos
- Configuração de choices
- Método __str__
- Validações no modelo
- Migrations funcionais

---

## Questão 2 - Serializers e Validações (5 pontos)

Crie serializers para manipulação de dados via API:

### a) Serializers Básicos
- `VeiculoSerializer`: todos os campos
- `PecaSerializer`: incluir campo calculado `em_estoque` (Boolean)
- `ItemPecaSerializer`: todos os campos

### b) OrcamentoSerializer
- Campos read-only: mecanico_responsavel (preencher automaticamente), valor_total, data_criacao
- Campos write-only quando apropriado
- Validação customizada:
  - Data de validade deve ser futura
  - Valor de mão de obra não pode ser negativo
  - Veículo deve ter cliente associado
  - Descrição do problema deve ter no mínimo 20 caracteres

### Critérios de Avaliação:
- Estrutura correta dos serializers
- Campos aninhados adequados
- Validações implementadas

---

## Questão 3 - Views e Endpoints (15 pontos)

Implemente as views utilizando ViewSets ou APIViews:

### a) PecaViewSet
- Listar peças com filtros (fabricante, status, estoque_minimo)
- Detalhes de uma peça específica
- Action customizada `verificar_estoque`:
  - Parâmetros: quantidade_desejada
  - Retorna se há estoque suficiente

### b) OrcamentoViewSet
- CRUD completo de orçamentos
- Filtros: cliente, status, período
- Permissions:
  - Cliente vê apenas seus orçamentos
  - Mecânico vê orçamentos atribuídos a ele
  - Gerente vê todos
- Actions customizadas:
  - `aprovar`: muda status para Aprovado (apenas Cliente)
  - `rejeitar`: muda status para Rejeitado com motivo
  - `gerar_ordem_servico`: cria OrdemServico a partir do orçamento aprovado

### c) OrdemServicoViewSet
- Criar ordem de serviço vinculada a um orçamento
- Listar ordens (filtrar por status, mecânico)
- Atualizar status (apenas Mecânico/Gerente)
- Action `adicionar_peca`:
  - Adiciona peça à ordem de serviço
  - Atualiza estoque automaticamente

### Critérios de Avaliação:
- Estrutura correta das views
- Implementação de filtros
- Actions customizadas funcionais
- Permissions adequadas
- Tratamento de exceções
- Responses HTTP corretos

---

## Questão 4 - Regras de Negócio (15 pontos)

Implemente as seguintes regras de negócio:

### **a) Validação de Estoque**
- Ao adicionar peça em uma ordem de serviço, verificar disponibilidade
- Reduzir quantidade do estoque ao confirmar uso
- Impedir uso de peça com status Descontinuado

### b) Cálculo de Valor Total
- Calcular automaticamente valor_total do orçamento:
  - valor_total = valor_mao_obra + valor_pecas
- Atualizar ao salvar orçamento

### c) Política de Aprovação
- Permitir aprovação apenas se status for Pendente
- Se orçamento expirado (data_validade < hoje):
  - Mudar automaticamente para status Expirado
  - Não permitir aprovação
- Se aprovado com mais de 30 dias da criação:
  - Adicionar campo `desconto_aplicado` (10% do valor_total)

### d) Controle de Ordem de Serviço
- Criar ordem apenas se:
  - Orçamento com status = Aprovado
  - Não existe ordem para este orçamento
- Ao concluir ordem:
  - Registrar data_conclusao
  - Enviar notificação (simular com print)
- Após conclusão, calcular valor final com peças utilizadas

### Critérios de Avaliação:
- Validação de estoque correta
- Política de aprovação implementada
- Lógica de ordem de serviço
- Cálculos automáticos funcionando

---

## Entregáveis

1. Código executo sem erros
2. Migrations criadas e aplicadas (Postgres)
3. Models com relacionamentos corretos
4. Serializers com validações
5. ViewSets com actions customizadas
6. Regras de negócio funcionando
7. README com instruções
8. requirements.txt atualizado

---

## Critérios de Avaliação

| Aspecto | Pontuação |
|---------|-----------|
| Questão 1 - Modelagem | 5 |
| Questão 2 - Serializers | 5 |
| Questão 3 - Views e Endpoints | 15 |
| Questão 4 - Regras de Negócio | 15 |
| **TOTAL** | **40** |

---

## Dicas Finais

- Leiam todo o enunciado antes de começar
- Organizem as tarefas entre a dupla
- Façam commits frequentes (se usar Git)
- Não deixem migrations para o final
- Usem o admin do Django para validar dados

---
