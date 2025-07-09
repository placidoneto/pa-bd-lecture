
# PetCare - Sistema de Gerenciamento de Atendimentos Veterinários

Este projeto é um sistema para gerenciamento de atendimentos de pets em clínicas veterinárias. Ele permite o cadastro e gerenciamento de tutores, pets e atendimentos, além de registrar informações importantes como vacinas, medicamentos e cirurgias.

O sistema foi desenvolvido como parte de um trabalho acadêmico utilizando **Spring Boot** com **JPA** e **PostgreSQL**.


Link Assigment: [Spring Boot - Tema 1 - PetCare](https://classroom.github.com/a/8jYobUms)
---

## Funcionalidades

- Cadastro de tutores com informações de contato
- Cadastro de pets e associação com tutores
- Cadastro de atendimentos veterinários
- Registro de vacinas, medicamentos e cirurgias por pet
- Histórico de atendimentos consultável por veterinários e tutores
- Autenticação de usuários (tutores e veterinários)
- Consultas avançadas com filtros (por data, raça, tipo, etc.)
- Backup de dados planejado com integração ao banco de grafos **Neo4j** (em desenvolvimento)

---

## Tecnologias Utilizadas

- Java 17 ou 21
- Spring Boot
- Spring Web
- Spring Data JPA
- PostgreSQL
- Maven
- Lombok (opcional)
- Neo4j (para futura extensão)

---

## Estrutura do Projeto

```
petcare/
├── src/
│   ├── main/
│   │   ├── java/com/example/petcare/
│   │   │   ├── controller/
│   │   │   ├── model/
│   │   │   ├── repository/
│   │   │   └── PetcareApplication.java
│   │   └── resources/
│   │       ├── application.properties
│   │       └── ...
├── pom.xml
└── README.md
```

---

## Modelos e Relacionamentos

- **Tutor**: id, nome, telefone, lista de pets
- **Pet**: id, nome, idade, tipo, raça, tutor, histórico de atendimentos
- **Atendimento**: id, data, descrição, veterinário, pet
- **Veterinário**: id, nome, especialidade
- **Vacina**: id, nome, data de aplicação, pet
- **Medicamento**: id, nome, dosagem, pet
- **Cirurgia**: id, nome, data, pet

---

## Como Rodar o Projeto

### 1. Requisitos

Antes de iniciar, você precisa ter os seguintes softwares instalados:

- **Java JDK 17 ou 21**
  - Verifique se o Java está instalado com: `java -version`
- **Git**
  - Verifique com: `git --version`
- **PostgreSQL**
  - Crie um banco chamado `petcare` com um usuário e senha configurados
  - O usuário padrão é `postgres´ e a porta 5432 - porta de uso padrão.
- **VS Code ou IntelliJ**
- **Maven (ou use o Maven Wrapper incluso)**

### 2. Clonar o Repositório

```bash
git clone https://github.com/IFRN/semin-rios-framework-spring-boot-2o-bimestre-tema1-crud-springboot-postgre.git
cd petcare
```

### 3. Configurar o Banco de Dados

No PostgreSQL, crie um banco chamado `petcare`.  
Depois, abra o arquivo `src/main/resources/application.properties` e edite com suas configurações:

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/petcare
spring.datasource.username=seu_usuario
spring.datasource.password=sua_senha
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
```

### 4. Rodar o Projeto

#### No Windows (com Maven Wrapper):

```bash
.\mvnw spring-boot:run
```

#### No Linux/macOS:

```bash
./mvnw spring-boot:run
```

Caso esteja usando Maven instalado no sistema, use:

```bash
mvn spring-boot:run
```

---

## Acesse o Swagger

Com o projeto rodando, abra no navegador:

```
http://localhost:8081/swagger-ui/index.html
```

Lá você pode testar todos os endpoints da API de forma interativa.

---

## Verifique os dados no PostgreSQL

Para visualizar os dados persistidos:

1. Acesse o banco `petcare` pelo **pgAdmin**
2. Vá até a aba de consultas (`Query Tool`)
3. Execute:

```sql
SELECT * FROM pet;
```


## Contribuidores

- Marya Eduarda Alexandre
- Wesley Costa
- Neemias Renan
- Jeremias
- Lucas 

---
# Link público para a apresentação
[https://www.canva.com/design/DAGsblaVi18/BjY426DbTCgD_cSEYhtXCQ/view?utm_content=DAGsblaVi18&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=h6ab7844645]



## Trabalho Prático

### Tarefa: Implementação de Novos Modelos
**Objetivo**: Criar novos modelos para expandir o sistema PetCare com as seguintes entidades:


#### 1. Modelo Atendimento
- **Atributos**:
  - `id` (Long) - Identificador único
  - `data` (LocalDate) - Data do atendimento
  - `descricao` (String) - Descrição do atendimento realizado

#### 2. Modelo Vacina
- **Atributos**:
  - `id` (Long) - Identificador único
  - `nome` (String) - Nome da vacina
  - `dataAplicacao` (LocalDate) - Data de aplicação da vacina

#### 3. Modelo Medicamento
- **Atributos**:
  - `id` (Long) - Identificador único
  - `nome` (String) - Nome do medicamento
  - `dosagem` (String) - Dosagem prescrita

#### 4. Modelo Cirurgia
- **Atributos**:
  - `id` (Long) - Identificador único
  - `nome` (String) - Nome/tipo da cirurgia
  - `data` (LocalDate) - Data da cirurgia

#### Detalhes e Requisitos da Implementação:
OBS:Para esse TP não será necessário criar os relacionamentos entre os Modelos.

- Criar os modelos seguindo o padrão dos modelos existentes (Pet, Tutor, Veterinario)
- Implementar repositories para cada modelo
- Criar services com métodos para listar e salvar
- Desenvolver controllers com endpoints GET (listar) e POST (criar)

