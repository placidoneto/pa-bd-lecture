# TP - Atividade prática: Gerenciar chamado de um Aluno relacionado a um Auxílio

## Objetivo 
Aplicar os conceitos do Quarkus para construir uma API RESTful para o sistema do Conta Comigo, a funcionalidade implementada permite que um aluno abra um chamado relacionado a um auxílio específico. Cada chamado pertence a um aluno, está vinculado a um auxílio e é atendido por uma assistente social. O chamado possui status e datas de criação e análise.

## Entidades de domínio
### Aluno
- id (Long)
- nome (String)
- matricula (String)
- curso (String)
- ativo (boolean)

### AssistenteSocial
- id (Long)
- nome (String)
- matricula (String)
- ativo (boolean)

### Auxilio
- id (Long)
- nome (String)
- descricao (String)
- ativo (boolean)

### Chamado
- id (Long)
- descricao (String)
- resposta (String)
- status (Enum: ABERTO, EM_ANALISE, FECHADO)
- dataAbertura (LocalDateTime – auto gerado)
- dataAnalise (LocalDateTime – atualizado ao mudar status)
- aluno (ManyToOne)
- assistenteSocial (ManyToOne)
- auxilio (ManyToOne)

## Regras de negócio 
1. O aluno deve existir e estar ativo.
2. A assistente social deve existir e estar ativa.
3. O auxílio deve existir e estar disponível.
4. A descrição do chamado é obrigatória.
5. Um chamado sempre inicia com status ABERTO.
6. A data de abertura é gerada automaticamente.
7. A data de análise deve ser atualizada sempre que o status for alterado.
8. Não existe chamado sem aluno, auxílio e assistente social.

## Configuração do Projeto
### Criar o projeto 

```powershell
quarkus create app com.tpquarkus:quarkus-chamados --extensions='resteasy-reactive-jackson,hibernate-orm-panache,agroal,quarkus-jdbc-postgresql, smallrye-openapi'
```

### Configuração PostgreSQL

- Configure o banco de dados PostgreSQL no arquivo src/main/resources/application.properties
```
# porta HTTP
quarkus.http.port=8080

# configuração do banco postgres
quarkus.datasource.db-kind=postgresql
quarkus.datasource.jdbc.url=jdbc:postgresql://localhost:5432/quarkuschamadosdb
quarkus.datasource.username=postgres
quarkus.datasource.password=postgres

# geração de schema em dev 
quarkus.hibernate-orm.database.generation=update

# pool: define o máximo de conexões simultaneas
quarkus.datasource.jdbc.max-size=20
```

### Estrutura de diretórios

```
quarkus-chamados/
│
├── src/
    ├── main/
        ├── java/
            └── org/
                └── tpquarkus/
                    ├── dto/
                    │   ├── ChamadoDTO.java
                    │   ├── AlunoDTO.java
                    |   ├── AuxilioDTO.java
                    |   └── AssistenteSocialDTO.java
                    │
                    ├── domain/
                    │   ├── Aluno.java
                    │   ├── AssistenteSocial.java
                    │   ├── Auxilio.java
                    │   └── Chamado.java
                    │
                    ├── repository/
                    │   ├── AlunoRepository.java
                    │   ├── AssistenteSocialRepository.java
                    │   ├── AuxilioRepository.java
                    │   └── ChamadoRepository.java
                    │
                    ├── service/
                    │   ├── AlunoService.java
                    │   ├── AssistenteSocialService.java
                    │   ├── AuxilioService.java
                    │   └── ChamadoService.java
                    │
                    └── resource/
                    │   ├── AlunoResource.java
                    │   ├── AssistenteSocialResource.java
                    │   ├── AuxilioResource.java
                    │   └── ChamadoResource.java
                    |
                    ├── mapper/
                    │   ├── AlunoMapper.java
                    │   ├── AssistenteSocialMapper.java
                    │   ├── AuxilioMapper.java
                    │   └── ChamadoMapper.java
                    |
```

### Endpoints da API 

#### Aluno

- ```GET /alunos``` - Retorna todos os alunos.
- ```GET /alunos/{id}``` - Retorna um aluno específico.
- ```POST /alunos``` - Cria um aluno.
- ```GET /alunos/ativo``` - Retorna alunos ativos no sistema.
- ```GET /alunos/desativados``` - Retorna alunos não ativos no sistema.
- ```PUT /alunos/{id}``` - Atualiza dados de um aluno específico.

#### Assistente Social

- ```GET /assistente_social``` - Retorna todos os assistente_social.
- ```GET /assistente_social/{id}``` - Retorna uma assistente social específica.
- ```POST /assistente_social``` - Cria uma assistente social.

### Auxílio

- ```GET /auxilios``` - Retorna todos os auxilios.
- ```GET /auxilios/{id}``` - Retorna um auxílio específico.
- ```POST /auxilios``` - Cria um auxílio.
- ```GET /auxilios/ativo``` - Retorna auxilios ativos no sistema.
- ```GET /auxilios/desativados``` - Retorna auxilios não ativos no sistema.
- ```PUT /auxilios/{id}``` - Atualiza dados de um auxílio específico.

#### Chamado

- ```GET /chamados``` - Lista todos os chamados.
- ```GET /chamados/{id}``` - Busca um chamado por ID.
- ```POST /chamados``` - Cria um chamado (status inicia como ABERTO).
- ```PUT /chamados/{id}``` - Atualizar chamado.
- ```DELETE chamados/{id}``` - Deletar um chamado.
- ```GET /chamados/status/{status}``` - Busca chamados por status.
- ```GET /chamados/aluno/{matricula}``` - Busca chamados de um aluno específico.
- ```GET /chamados/auxilio/{nome}``` - Busca chamados de um auxílio específico.
- ```PUT /chamados/{id}/fechar``` - Fechar chamado (só pode ser fechado caso esteja com o status EM_ANALISE)
- ```PUT /chamados/{id}/responder``` - Responder um chamado (quando responder o status é atualizado para EM_ANALISE e a data de análise é atualizada.)
