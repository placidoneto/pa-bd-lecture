# 🧪 Trabalho Prático - Expansão do Sistema PetCare

## 🎯 Descrição da Atividade

Neste trabalho prático, você irá **expandir o sistema PetCare** adicionando duas novas entidades com relacionamento entre si. Toda a implementação deverá seguir o padrão de arquitetura utilizado no projeto original: **Model, Repository, Service, Controller**, e também deverá estar integrada ao sistema de **Backup Neo4j**. Ou seja, você irá realizar todos os passos aprendidos anteriomente utilizando como banco de dados principal o Postgres e depois fazer o backup para o Neo4j.

## 📚 Tema da Expansão

Você deverá implementar as seguintes entidades:

### 📁 `Exame`

Representa exames realizados pelos pets.

* `id`: identificador do exame
* `nome`: nome do exame (ex: Hemograma)
* `data`: data de realização
* `resultado`: texto descritivo com o resultado

### 📁 `Laboratório`

Representa o local onde os exames são realizados.

* `id`: identificador do laboratório
* `nome`: nome do laboratório
* `endereco`: endereço físico
* `responsavelTecnico`: nome do responsável técnico

### 🔗 Relacionamento

Um exame é realizado **em apenas um laboratório**, mas **um laboratório pode realizar vários exames** (relacionamento muitos-para-um).

---

## 📦 Requisitos da Implementação

Você deverá:

1. **Criar as classes `Model` para Exame e Laboratório**.
2. Criar os **Repositories (JPA)** para ambas as entidades.
3. Criar os **Services** para manipular a lógica de negócios de ambas.
4. Criar os **Controllers REST**, com os seguintes endpoints:

   * `GET /api/exames`
   * `GET /api/laboratorios`
   * `POST /api/exames`
   * `POST /api/laboratorios`
   * `PUT /api/exames/{id}`
   * `PUT /api/laboratorios/{id}`
   * `DELETE /api/exames/{id}`
   * `DELETE /api/laboratorios/{id}`
5. Atualizar o **Swagger** para que os novos endpoints apareçam.
6. Fazer o backup de dados no neo4j, seguindo o mesmo esquema apresentado na aula anterior (verifique o readme de explicação da apresentação, em casos de dúvida).

---

## 🧬 Integração com Backup

Adicione os métodos no `BackupService` e `BackupController` para exportar os dados de Exames e Laboratórios para o **Neo4j**.

Exemplo de grafo esperado:

```text
(Pet)-[:REALIZOU]->(Exame)-[:REALIZADO_EM]->(Laboratório)
```

---

## 🛠 Populando o Banco

Para popular o banco você tem duas opções:

1. Atualizar na mão;

ou

2. Atualizar via o script Python `populate_database.py` com a criação de:

* 3 laboratórios
* 5 exames (relacionados a pets e a laboratórios)

---

## 🚀 Dicas

* Baseie-se na estrutura existente do projeto para copiar padrões de implementação.
* Reaproveite o funcionamento dos endpoints existentes.
* Use o Swagger para testar os endpoints.
* Teste se o grafo está aparecendo corretamente no Neo4j Aura.
* Verifique o readme anterior se esqueceu de completar algum passo.
* Peça ajuda a nós, o grupo, em caso de dúvida 

