# Relacionamento e CRUD para todas as classes do sistema PetCare
Este repositório se refere a 2° etapa do desenvolvimento do projeto PetCare, expandindo a estrutura inicial criada pelo Grupo 1. A implementação engloba os relacionamentos entre todas as classes do modelo e os respectivos endpoints CRUD).

## Relacionamentos Implementados
As entidades foram modeladas com base nas regras de negócio do sistema, utilizando anotações JPA para refletir os relacionamentos no banco de dados PostgreSQL:<br>
Tutor ↔ Pet → Um-para-Muitos <br>
Pet ↔ Atendimento → Um-para-Muitos <br>
Pet ↔ Vacina, Medicamento, Cirurgia → Um-para-Muitos <br>
Veterinário ↔ Atendimento → Um-para-Muitos <br>
Todos os relacionamentos foram testados e verificados via Postman e pgAdmin. <br>

## Endpoints CRUD
Para cada entidade do projeto, foram desenvolvidos endpoints RESTful com as seguintes operações: <br>
GET /entidade – Listagem completa <br>
GET /entidade/{id} – Busca por ID <br>
POST /entidade – Cadastro de novo registro <br>
PUT /entidade/{id} – Atualização de registro existente <br>
DELETE /entidade/{id} – Exclusão <br>
As entidades cobertas: 
- Tutor
- Pet
- Atendimento
- Veterinário
- Vacina
- Medicamento
- Cirurgia

## Como testar

### 1. Clone o Repositório

```bash
git clone https://github.com/IFRN/semin-rios-framework-spring-boot-2o-bimestre-tema2-relacionamento-crud-todas-classes.git
cd petcare/petcare
```

### 2. Configurar o Banco de Dados

No PGAdmin (Postgres), crie um banco chamado `petcare`.  
Depois, abra o arquivo `src/main/resources/application.properties` e edite com suas configurações:

```properties
spring.datasource.url=jdbc:postgresql://localhost:5432/petcare
spring.datasource.username=seu_usuario
spring.datasource.password=sua_senha
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=true
spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.PostgreSQLDialect
```

### 3. Rode o Projeto

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

### 4. Acesse o Swagger

Com o projeto rodando, abra no navegador:

```
http://localhost:8080/swagger-ui/index.html
```

Lá você pode testar todos os endpoints da API de forma interativa.

## Membros da equipe
<table style>
  <tr>
    <td align="center"><a href="https://github.com/namariaa">
        <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/namariaa" width="100px;" alt="Bolsista 2"/>
        <br />
        <a href="https://github.com/namariaa"><b>Ana Maria</b></a>
    </td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/rielps">
        <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/170769111?v=4" width="100px;" alt="Jesrriel Moura"/>
        <br />
        <a href="https://github.com/rielps"><b>Jesrriel Moura</b></a>
    </td>
    <td align="center"><a href="https://github.com/luuiizf">
        <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/97256376?v=4" width="100px;" alt="Luiz Fernando"/>
        <br />
        <a href="https://github.com/luuiizf"><b>Luiz Fernando</b></a>
    </td>
    <td align="center"><a href="https://github.com/luiizr">
        <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/164033637?v=4" width="100px;" alt="Luiz Roberto"/>
        <br />
        <a href="https://github.com/luiizr"><b>Luiz Roberto</b></a>
    </td>
  </tr>

</table>

## Trabalho prático
Depois de trabalharmos juntos nos modelos de atendimento, vacina, tutores e mais, está na hora de darmos o próximo passo no projeto. E pra deixar o sistema ainda mais completo, vamos construir dois novos modelos super importantes: Clinica e Agendamento. <br>
-Clínica: Esse modelo vai permitir registrar todas as informações essenciais sobre uma clínica veterinária, como nome, localização e dados de contato. Com isso, o sistema poderá conectar cada agendamento ao local onde será realizado, garantindo mais organização e controle para os profissionais e tutores.
 <br>
- Agendamento: Com esse modelo, os atendimentos podem ser marcados com mais organização. Vocês vão registrar a data, o veterinário, o tipo de atendimento e até a clínica onde o pet será cuidado. Tudo com praticidade e controle! <br>
**A missão de vocês Agora é com vocês!** A ideia é que cada um coloque a mão na massa e ajude a construir esses modelos no sistema. <br>
### 1. Modelo Clínica 
Objetivo: Representar uma clínica veterinária onde os atendimentos podem ser realizados. <br>
**Atributos** <br>
- **id** (Long): Identificador único da clínica
- **nome** (String): Nome da clínica
- **endereco** (String): Localização da clínica (rua, número, bairro etc.)
- **telefone** (String): Contato principal da clínica

### 2. Modelo Agendamento
Objetivo: Representar um agendamento envolvendo atendimento, pet, veterinário e clínica. <br>
**Atributos** <br>
- **id** (Long): Identificador único <br>
- **dataAgendada** (LocalDate): Data marcada para o atendimento <br>
- **pet** (Pet): Pet que será atendido <br>
- **veterinario** (Veterinario): Veterinário responsável <br>
- **atendimento** (Atendimento): Qual atendimento ele está relacionado <br>
- **clinica** (Clinica): Local do agendamento <br>



