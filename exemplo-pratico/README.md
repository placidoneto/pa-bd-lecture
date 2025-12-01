# Exemplo prático com Quarkus e PostgreSQL

## Conceder benefício ao aluno dentro de um auxílio

Imagine que você está desenvolvendo a aplicação do Conta Comigo e uma das funcionalidades permite que a Assistente Social registre que um aluno recebeu um benefício específico dentro de um auxílio. Importante frisar que cada benefício pertence a um auxílio, e um aluno não pode receber o mesmo benefício mais de uma vez enquanto ele estiver ativo.

## Passo a Passo

Antes de criar a aplicação em Quarkus, é necessário instalá-lo. Para isso, basta rodar os seguintes comandos no PowerShell:

```powershell
iex "& { $(iwr https://ps.jbang.dev) } trust add https://repo1.maven.org/maven2/io/quarkus/quarkus-cli/"

iex "& { $(iwr https://ps.jbang.dev) } app install --fresh --force quarkus@quarkusio"
```

### 1. Configuração inicial 

- Crie um novo projeto Quarkus com artefato 'meuprojeto' e extensão REST + HibernatePanache + JDBC Postgres:

```powershell
quarkus create app com.seuprojeto:meuprojeto --extensions='resteasy-reactive-jackson,hibernate-orm-panache,agroal,quarkus-jdbc-postgresql, smallrye-openapi'
```

#### Explicando cada comando
 - ```resteasy-reactive-jackson```: Cria endpoint REST e converte objetos JSON automaticamente.
 - ```hibernate-orm-panache```: O  Hibernate é um framework de ORM para Java, ele vai permitir que você trabalhe com banco de dados usando objetos java, sem precisar escrever SQL manual e junto com o ele o Panache vai permitir que você simplifique o uso do Hibernate ORM, deixando o código muito mais limpo.
 - ```quarkus-jdbc-postgresql```: API padrão do Java para se conectar ao banco de dados, nesse caso o postgres. 
 - ```agroal```: Gerenciador de conexões para JDBC. 
 - ```smallrye-openapi```: Extensão pro Swagger.

Estrutura de diretórios

```
meuprojeto
└── src
|    └── main
|        └── java
|        |   └── com
|        |   └── seuprojeto
|        └── docker
|        |    |── Dockerfile.jvm
|        |    |── Dockerfile.legacy-jar
|        |    |── Dockerfile.native
|        |    |── Dockerfile.native-micro
|        └── resources
|            └── application.properties
└── .mvn
|    └── wrapper
|        └── maven-wrapper.properties
|── .dockerignore
|── .gitignore
|── mvnw
|── mvnw.cmd
|── pom.xml
|── README.md
```

- Crie todas as pastas e arquivos dentro de com/seuprojeto.

### 2. Configuração do PostgreSQL

Crie o banco pelo PgAdmin com o nome ```meuprojetodb``` ou rode o comando abaixo alterando para o seu password do postgres.

```powershell
$env:PGPASSWORD="postgres"; psql -U postgres -h localhost -c "CREATE DATABASE meuprojetodb;"
```

- Configure o banco de dados PostgreSQL no arquivo src/main/resources/application.properties
```
# porta HTTP
quarkus.http.port=8080

# configuração do banco postgres
quarkus.datasource.db-kind=postgresql
quarkus.datasource.jdbc.url=jdbc:postgresql://localhost:5432/meuprojetodb
quarkus.datasource.username=postgres
quarkus.datasource.password=postgres

# geração de schema em dev 
quarkus.hibernate-orm.database.generation=update

# pool: define o máximo de conexões simultaneas
quarkus.datasource.jdbc.max-size=20
```

### 3. Classes de domínio 

Nas classes de domínio vai conter as entidades utilizadas no nosso sistema, ou seja, as classes que representam as tabelas do banco de dados.

Estrutura de diretórios 
```   
src
└── main
    └── java
        └── com/seuprojeto
            └── domain
                ├── Aluno.java
                ├── Auxilio.java
                ├── Beneficio.java
                └── BeneficioAluno.java
```

- Na pasta src/main/java/com/seuprojeto insira as 4 classes de domínio.

```java
package com.seuprojeto.domain;
import io.quarkus.hibernate.orm.panache.PanacheEntity;
import jakarta.persistence.Entity;

@Entity
public class Aluno extends PanacheEntity{

    public String nome;
    public String email;
    public Boolean ativo;

}
```

Iniciamos com um exemplo bem simples da classe Aluno, onde temos os campos de nome, email e se o aluno está ativo ou não no sistema. No java com o hibernate e panache utilizamos decoradores para marcar o tipo de classe ou atributo que estamos usando, no caso das classes de domínio todas são entidades e para isso utilizamos a anotação ```@Entity```. 

```java
package com.seuprojeto.domain;

import io.quarkus.hibernate.orm.panache.PanacheEntity;
import jakarta.persistence.Entity;

@Entity
public class Auxilio extends PanacheEntity {
    public String titulo;
    public String descricao;
    public Boolean ativo;
}
```

Depois vemos o modelo Auxílio que é o conceito geral contendo o titulo, descricao e se o auxílio está ativo ou não no sistema.

```java
package com.seuprojeto.domain;

import io.quarkus.hibernate.orm.panache.PanacheEntity;
import jakarta.persistence.Entity;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;

@Entity
public class Beneficio extends PanacheEntity {
    
    public String nome;
    public String descricao;
    public Boolean ativo;

    @ManyToOne
    @JoinColumn(name = "auxilio_id") // nome da coluna FK
    public Auxilio auxilio;

}
```

Agora temos a classe de Beneficio que é específico do auxílio, e nisso vemos a utilização de chave estrangeira para a tabela Auxilio utilizando a anotação ```@JoinColumn``` e a especificação de que é um relacionamento um para muitos com a anotação ```@ManyToOne```.

```java
package com.seuprojeto.domain;

import java.time.LocalDate;

import org.hibernate.annotations.CreationTimestamp; // já gera o id automaticamente

import io.quarkus.hibernate.orm.panache.PanacheEntity;
import jakarta.persistence.Entity;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;


@Entity
public class BeneficioAluno extends PanacheEntity {
    
    public String observacao;
    @CreationTimestamp // registra automaticamente quando é criado
    public LocalDate data_concessao;
    public Boolean ativo;

    @ManyToOne
    @JoinColumn(name = "aluno_id") // nome da coluna FK
    public Aluno aluno;

    @ManyToOne
    @JoinColumn(name = "auxilio_id") // nome da coluna FK
    public Auxilio auxilio;

}
```

Agora temos a tabela de relação entre Benefício e Aluno, visto que o aluno pode ter vários benefícios, porém apenas um benefício por auxílio. E novamento utilizamos os decoradores para marcar a cardinalidade e as chaves estrangeiras. Além disso utilizamos a anotação ```CreationTimeStamp``` para registrar a data_concessao no momento em que o objeto for criado.

### 4. Classes de DTO (Data Transfer Object)

Serve para separar o que entra e o que sai da API da sua entidade real. É útil para evitar expor as entidades e permite validar os dados separados da entidade. 

**Por exemplo:** Na entidade `BeneficioAluno` passamos os objetos completos de `Aluno` e `Auxilio`, já no DTO são passados apenas os IDs (`alunoId` e `auxilioId`), que são os dados necessários para a requisição. 

**Fluxo:** Quando você recebe uma requisição JSON, ela vem como DTO (com IDs), você converte para Entidade (com objetos completos) através do Mapper e salva no banco.

Estrutura de diretórios 

```
src
└── main
    └── java
        └── com/seuprojeto
            ...
            │
            ├── dto
                ├── AlunoDTO.java
                ├── BeneficioDTO.java
                ├── AuxilioDTO.java
                ├── BeneficioAlunoDTO.java
```

- Crie as 4 classes abaixo:

```java
package com.seuprojeto.DTO;

public class AlunoDTO {
    public Long id;
    public String nome;
    public String email;
    public Boolean ativo;
}
```

```java
package  com.seuprojeto.DTO;

public class AuxilioDTO {
    public Long id;
    public String titulo;
    public String descricao;
    public Boolean ativo;
}
```

```java
package  com.seuprojeto.DTO;
import java.time.LocalDate;

public class BeneficioAlunoDTO {
    public Long id;
    public String observacao;
    public LocalDate data_concessao;
    public Boolean ativo;
    public Long alunoId;
    public Long auxilioId;
}
```

```java
package  com.seuprojeto.DTO;

public class BeneficioDTO {
    public Long id;
    public String nome;
    public String descricao;
    public Boolean ativo;
    public Long auxilioId;
}
```
### 5. Classes de mapeamento 

Aqui vão ficar as classes responsáveis por converter DTO <-> Entidade. Isso vai evitar escrever código repetitivo de mapeamento dentro da camada de service.

Estrutura de diretórios
```
src
└── main
    └── java
        └── com/seuprojeto
            ...
            └── mapper
                ├── AlunoMapper.java
                └── BeneficioMapper.java
                └── AuxilioMapper.java
                └── BeneficioAlunoMapper.java
```

- Crie as 4 classes abaixo:

```java
package com.seuprojeto.mapper;

import com.seuprojeto.DTO.AlunoDTO;
import com.seuprojeto.domain.Aluno;

public class AlunoMapper {
    // usado na api para entrada e saida de dados
    public static AlunoDTO toDTO(Aluno aluno) {
        AlunoDTO dto = new AlunoDTO();
        dto.id = aluno.id;
        dto.nome = aluno.nome;
        dto.email = aluno.email;
        dto.ativo = aluno.ativo;
        return dto;
    }
    // usado  para persisitr o dado no banco
    public static Aluno toEntity(AlunoDTO dto) {
        Aluno aluno = new Aluno();
        aluno.nome = dto.nome;
        aluno.email = dto.email;
        aluno.ativo = dto.ativo;
        return aluno;
    }
}
```

```java
package com.seuprojeto.mapper;

import com.seuprojeto.DTO.AuxilioDTO;
import com.seuprojeto.domain.Auxilio;


public class AuxilioMapper {
    // usado na api para entrada e saida de dados
    public static AuxilioDTO toDTO(Auxilio auxlio) {
        AuxilioDTO dto = new AuxilioDTO();
        dto.id = auxlio.id;
        dto.titulo = auxlio.titulo;
        dto.descricao = auxlio.descricao;
        dto.ativo = auxlio.ativo;
        return dto;
    }
    // usado  para persisitr o dado no banco
    public static Auxilio toEntity(AuxilioDTO dto) {
        Auxilio auxlio = new Auxilio();
        auxlio.titulo = dto.titulo;
        auxlio.descricao = dto.descricao;
        auxlio.ativo = dto.ativo;
        return auxlio;
    }
}
```

```java
package com.seuprojeto.mapper;
import com.seuprojeto.DTO.BeneficioAlunoDTO;
import com.seuprojeto.domain.BeneficioAluno;
import com.seuprojeto.domain.Auxilio;
import com.seuprojeto.domain.Aluno;

public class BeneficioAlunoMapper {
     public static BeneficioAlunoDTO toDTO(BeneficioAluno benficioaluno) {
        BeneficioAlunoDTO dto = new BeneficioAlunoDTO();
        dto.id = benficioaluno.id;
        dto.observacao = benficioaluno.observacao;
        dto.data_concessao = benficioaluno.data_concessao;
        dto.ativo = benficioaluno.ativo;
        dto.alunoId = benficioaluno.aluno != null ? benficioaluno.aluno.id : null;
        dto.auxilioId = benficioaluno.auxilio != null ? benficioaluno.auxilio.id : null;
        return dto;
    }
    // usado  para persisitr o dado no banco
    public static BeneficioAluno toEntity(BeneficioAlunoDTO dto) {
        BeneficioAluno benficioaluno = new BeneficioAluno();
        benficioaluno.observacao = dto.observacao;
        benficioaluno.data_concessao = dto.data_concessao;
        benficioaluno.ativo = dto.ativo;
        // cria um Auxilio só com o ID
        Auxilio aux = new Auxilio();
        aux.id = dto.auxilioId;
        // cria um Aluno só com o ID
        Aluno aluno = new Aluno();
        aluno.id = dto.alunoId;

        benficioaluno.aluno = aluno;
        benficioaluno.auxilio = aux;
        return benficioaluno;
    }
}
```
``` java
package com.seuprojeto.mapper;

import com.seuprojeto.DTO.BeneficioDTO;
import com.seuprojeto.domain.Auxilio;
import com.seuprojeto.domain.Beneficio;


public class BeneficioMapper {
    // usado na api para entrada e saida de dados
    public static BeneficioDTO toDTO(Beneficio beneficio) {
        BeneficioDTO dto = new BeneficioDTO();
        dto.id = beneficio.id;
        dto.nome = beneficio.nome;
        dto.descricao = beneficio.descricao;
        dto.ativo = beneficio.ativo;
        dto.auxilioId = beneficio.auxilio != null ? beneficio.auxilio.id : null;
        return dto;
    }
    // usado  para persisitr o dado no banco
    public static Beneficio toEntity(BeneficioDTO dto) {
        Beneficio beneficio = new Beneficio();
        beneficio.nome = dto.nome;
        beneficio.descricao = dto.descricao;
        beneficio.ativo = dto.ativo;
        // cria um Auxilio só com o ID
        Auxilio aux = new Auxilio();
        aux.id = dto.auxilioId;

        beneficio.auxilio = aux;
        return beneficio;
    }
}

```

### 6. Classes de repositório

As classes de repositório são responsáveis por toda a comunicação com o banco de dados. Quando usamos o Panache, seguimos essa convenção para manter uma camada dedicada exclusivamente às operações de acesso a dados. Essa camada contém métodos responsáveis por executar: SELECT, INSERT, UPDATE e DELETE.
O objetivo é garantir a separação de responsabilidades, deixando: a entidade representando os dados, o serviço contendo a lógica de negócio e o repositório cuidando apenas do acesso ao banco.

Estrutura de diretórios
```
src
└── main
    └── java
        └── com/seuprojeto
            ...
            ├── repository
            │   ├── AlunoRepository.java
            │   ├── AuxilioRepository.java
            │   ├── BeneficioRepository.java
            |   ├── BeneficioAlunoRepository.java
```

```java
package com.seuprojeto.repository;
import com.seuprojeto.domain.Aluno;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;

@ApplicationScoped
public class AlunoRepository implements PanacheRepository<Aluno> {
    // Retorna todos os alunos ativos
    public List<Aluno> ativos(){
        return find("ativo", true).list();
    }
}
```

A anotação ```@ApplicationScoped``` faz parte do CDI (Contexts and Dependency Injection) que define o ciclo de vida do objeto, serve para performande pois faz com que a classe tenha apenas uma instância durante toda a aplicação (singleton), ou seja, é criada na primeira vez que é necessária e depois só é reutilizada por todas as partes do código que a injetam.


```java
package com.seuprojeto.repository;
import com.seuprojeto.domain.Auxilio;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;

@ApplicationScoped
public class AuxilioRepository implements PanacheRepository<Auxilio> {
    public List<Auxilio> ativos(){
        return find("ativo", true).list();
    }
}
```

```java
package com.seuprojeto.repository;
import com.seuprojeto.domain.Aluno;
import com.seuprojeto.domain.Auxilio;
import com.seuprojeto.domain.BeneficioAluno;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;

@ApplicationScoped
public class BeneficioAlunoRepository implements PanacheRepository<BeneficioAluno> {
    public BeneficioAluno buscarAtivo(Aluno aluno, Auxilio auxilio) {
        return find("aluno = ?1 AND auxilio = ?2 AND ativo = true", // faz uma consulta JPQL, ?1 vai ser substituído por aluno e ?2 por beneficioAluno
                aluno, auxilio).firstResult(); // vai retornar o primeiro resultado encontrado ou null
    }

    public List<BeneficioAluno> listarBeneficiosAlunosAtivos() {
        return find("ativo", true).list();
    }
}
```

```java
package com.seuprojeto.repository;
import com.seuprojeto.domain.Beneficio;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;

@ApplicationScoped
public class BeneficioRepository implements PanacheRepository<Beneficio> {
    public List<Beneficio> ativos(){
        return find("ativo", true).list();
    }
}
```

### 7. Classes de serviço

Contém as regras de negócio, ou seja, a lógica do sistema e nisso vamos ter duas classes de serviço: Aluno e Beneficio. Nossas regras de negócio vão ser:
- O aluno deve existir e estar ativo.
- O auxílio deve existir e estar ativo.
- O benefício deve existir e pertencer ao auxílio informado.
- O benefício deve estar ativo.
- O aluno não pode ter o mesmo benefício ativo dentro do mesmo auxílio.
- A data de concessão é registrada automaticamente.
- O campo ativo em BeneficioAluno indica se o aluno ainda está recebendo aquele benefício.

Estrutura de diretórios 
```
src
└── main
    └── java
        └── com/seuprojeto
            ...
            ├── service
            |    ├── AlunoService.java
            |    └── BeneficioService.java
            |    ├── AuxilioService.java
            |    ├── BeneficioAlunoService.java
```

- Crie as seguintes classes 

```java
package com.seuprojeto.service;

import java.util.List;

import com.seuprojeto.domain.Aluno;
import com.seuprojeto.repository.AlunoRepository;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

@ApplicationScoped
public class AlunoService {

    @Inject
    AlunoRepository repository;

    public List<Aluno> listarAlunos() {
        return repository.listAll();
    }

    public List<Aluno> listarAlunosAtivos() {
        return repository.ativos();
    }

    public Aluno buscarPorId(Long id) {
        return repository.findById(id);
    }

    public void salvar(Aluno aluno) {
        repository.persist(aluno);
    }

    public boolean remover(Long id) {
        return repository.deleteById(id);
    }
}
```

Utiliza as classes de repositório para acessar os dados necessários e fazer as regras de negócio.

```java
package com.seuprojeto.service;
import java.util.List;

import com.seuprojeto.domain.Auxilio;
import com.seuprojeto.repository.AuxilioRepository;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

@ApplicationScoped
public class AuxilioService {
    
    @Inject
    AuxilioRepository repository;

    public List<Auxilio> listarAuxilios() {
        return repository.listAll();
    }

    public List<Auxilio> listarAuxiliosAtivos() {
        return repository.ativos();
    }

    public Auxilio buscarPorId(Long id) {
        return repository.findById(id);
    }

    public void salvar(Auxilio auxilio) {
        repository.persist(auxilio);
    }   

    public boolean remover(Long id) {
        return repository.deleteById(id);
    }   

}
```

```java
package com.seuprojeto.service;
import java.util.List;

import com.seuprojeto.DTO.BeneficioAlunoDTO;
import com.seuprojeto.domain.Aluno;
import com.seuprojeto.domain.Auxilio;
import com.seuprojeto.domain.BeneficioAluno;
import com.seuprojeto.exception.BusinessException;
import com.seuprojeto.repository.AlunoRepository;
import com.seuprojeto.repository.AuxilioRepository;
import com.seuprojeto.repository.BeneficioAlunoRepository;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;

@ApplicationScoped
public class BeneficioAlunoService {

    @Inject
    BeneficioAlunoRepository repository;

    @Inject
    AuxilioRepository auxilioRepository;

    @Inject
    AlunoRepository alunoRepository;

    public List<BeneficioAluno> listarBeneficiados() {
        return repository.listAll();
    }

    public List<BeneficioAluno> listarBeneficiadosAtivos() {
        return repository.ativos();
    }

    public BeneficioAluno buscarPorId(Long id) {
        return repository.findById(id);
    }

    @Transactional
    public void salvar(BeneficioAluno beneficiado) {
        repository.persist(beneficiado);
    }

    @Transactional
    public boolean remover(Long id) {
        return repository.deleteById(id);
    }

    @Transactional
    public BeneficioAluno inserirAlunoBeneficio(BeneficioAlunoDTO request) {

        // 1. Busca o benefício (auxílio) correto e o aluno de acordo com id fornecido 
        Auxilio auxilio = auxilioRepository.findById(request.auxilioId);
        Aluno aluno = alunoRepository.findById(request.alunoId);

        if (aluno == null) {
            throw new BusinessException("Aluno não encontrado");
        }

        if (auxilio == null) {
            throw new BusinessException("Auxílio não encontrado");
        }

        // 2. Verifica se esse aluno já tem esse mesmo benefício ativo
        BeneficioAluno beneficioAtivo = repository.buscarAtivo(aluno, auxilio);

        if (beneficioAtivo != null) {
            throw new BusinessException("Aluno já possui esse benefício ativo");
        }

        // 3. Cria um novo vínculo
        BeneficioAluno novo = new BeneficioAluno();
        novo.aluno = aluno;
        novo.auxilio = auxilio;
        novo.observacao = request.observacao;
        novo.data_concessao = request.data_concessao;
        novo.ativo = true;

        repository.persist(novo);
        return novo;
    }
}
```

```java
package com.seuprojeto.service;
import java.util.List;

import com.seuprojeto.domain.Beneficio;
import com.seuprojeto.repository.BeneficioRepository;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;

@ApplicationScoped
public class BeneficioService {
    
    @Inject
    BeneficioRepository repository;

    public List<Beneficio> listarBeneficio() {
        return repository.listAll();
    }

    public List<Beneficio> listarBeneficiosAtivos() {
        return repository.ativos();
    }

    public Beneficio buscarPorId(Long id) {
        return repository.findById(id);
    }

    public void salvar(Beneficio auxilio) {
        repository.persist(auxilio);
    }   

    public boolean remover(Long id) {
        return repository.deleteById(id);
    }   

}
```
### 8. Classes de Resource

Contém as rotas REST. Aqui vai ficar as classes que recebem requisições HTTP e chamam o service. Vão ter anotações como ```@Path```, ```@GET```, ```@POST```, ```@PUT``` e ```@DELETE```.

Estrutura de diretórios 
```
src
└── main
    └── java
        └── com/seuprojeto
            ...
            ├── resource
                ├── AlunoResource.java
                ├── AuxilioResource.java
                └── BeneficioResource.java
                └── BeneficioAlunoResource.java
```

- Crie as 4 classes abaixo:

```java
package com.seuprojeto.resource;

import java.util.List;

import com.seuprojeto.DTO.AlunoDTO;
import com.seuprojeto.domain.Aluno;
import com.seuprojeto.mapper.AlunoMapper;
import com.seuprojeto.service.AlunoService;

import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.NotFoundException;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;


@Path("/aluno")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AlunoResource {

    @Inject
    AlunoService alunoService;

    @GET
    @Path("/lista")
    public List<Aluno> listAll() {
        return alunoService.listarAlunos();
    }

    @GET
    @Path("/ativos")
    public List<Aluno> listAtivos() {
        return alunoService.listarAlunosAtivos();
    }

    @GET
    @Path("/{id}")
    public AlunoDTO findById(@PathParam("id") Long id) {
        Aluno aluno = alunoService.buscarPorId(id);
        if (aluno == null) {
            throw new NotFoundException("Aluno não encontrado");
        }
        return AlunoMapper.toDTO(aluno);
    }

    @POST
    @Transactional
    public AlunoDTO create(AlunoDTO dto) {
        Aluno aluno = new Aluno();
        aluno.nome = dto.nome;
        aluno.email = dto.email;
        aluno.ativo = dto.ativo;

        alunoService.salvar(aluno);
        return AlunoMapper.toDTO(aluno);
    }

    @PUT
    @Path("/{id}")
    @Transactional
    public AlunoDTO update(@PathParam("id") Long id, AlunoDTO updated) {
        Aluno aluno = alunoService.buscarPorId(id);
        if (aluno == null) {
            throw new NotFoundException("Aluno não encontrado");
        }

        aluno.nome = updated.nome;
        aluno.email = updated.email;
        aluno.ativo = updated.ativo;

        return AlunoMapper.toDTO(aluno);
    }

    @DELETE
    @Path("/{id}")
    @Transactional
    public void delete(@PathParam("id") Long id) {
        boolean deleted = alunoService.remover(id);
        if (!deleted) {
            throw new NotFoundException("Aluno não encontrado");
        }
    }
}
```

Nas classes de resource são utilizadas as anotações ```@Produces``` e ```@Consumes``` para indicar que tanto as requisições quanto as respostas são trocadas no formato JSON. E nesse exemplo acima, o serviço ```alunoService``` é injetado na classe para que o controller consiga delegar as regras de negócio e operações de banco de dados. E por fim, temos o CRUD simples de informações.

```java
package com.seuprojeto.resource;
import java.util.List;

import com.seuprojeto.DTO.AuxilioDTO;
import com.seuprojeto.domain.Auxilio;
import com.seuprojeto.mapper.AuxilioMapper;
import com.seuprojeto.service.AuxilioService;

import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.NotFoundException;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

@Path("/auxilio")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AuxilioResource {

    @Inject
    AuxilioService auxilioService;

    @GET
    public List<Auxilio> listAll() {
        return auxilioService.listarAuxilios();
    }

    @GET
    @Path("/ativos")
    public List<Auxilio> listAtivos() {
        return auxilioService.listarAuxiliosAtivos();
    }

    @GET
    @Path("/{id}")
    public AuxilioDTO findById(@PathParam("id") Long id) {
        Auxilio auxilio = auxilioService.buscarPorId(id);
        if (auxilio == null) {
            throw new NotFoundException("Auxilio não encontrado");
        }
        return AuxilioMapper.toDTO(auxilio);
    }

    @POST
    @Transactional
    public AuxilioDTO create(AuxilioDTO dto) { // cria um auxilio
        Auxilio auxilio = new Auxilio();
        auxilio.titulo = dto.titulo;
        auxilio.descricao = dto.descricao;
        auxilio.ativo = dto.ativo;

        auxilioService.salvar(auxilio);
        return AuxilioMapper.toDTO(auxilio);
    }

    @PUT
    @Path("/{id}")
    @Transactional
    public AuxilioDTO update(@PathParam("id") Long id, AuxilioDTO updated) {
        Auxilio auxilio = auxilioService.buscarPorId(id);
        if (auxilio == null) {
            throw new NotFoundException("Auxilio não encontrado");
        }

        auxilio.titulo = updated.titulo;
        auxilio.descricao = updated.descricao;
        auxilio.ativo = updated.ativo;

        return AuxilioMapper.toDTO(auxilio);
    }

    @DELETE
    @Path("/{id}")
    @Transactional
    public void delete(@PathParam("id") Long id) {
        boolean deleted = auxilioService.remover(id);
        if (!deleted) {
            throw new NotFoundException("Auxilio não encontrado");
        }
    }
}
```

```java
package com.seuprojeto.resource;

import java.util.List;

import com.seuprojeto.DTO.BeneficioAlunoDTO;
import com.seuprojeto.domain.BeneficioAluno;
import com.seuprojeto.mapper.BeneficioAlunoMapper;
import com.seuprojeto.service.BeneficioAlunoService;

import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.NotFoundException;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

@Path("/beneficioAluno")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class BeneficioAlunoResource {

    @Inject
    BeneficioAlunoService beneficioAlunoService;

    @GET
    public List<BeneficioAluno> listAll() {
        return beneficioAlunoService.listarBeneficiados();
    }

    @GET
    @Path("/ativos")
    public List<BeneficioAluno> listAtivos() {
        return beneficioAlunoService.listarBeneficiadosAtivos();
    }

    @GET
    @Path("/{id}")
    public BeneficioAlunoDTO findById(@PathParam("id") Long id) {
        BeneficioAluno beneficioAluno = beneficioAlunoService.buscarPorId(id);
        if (beneficioAluno == null) {
            throw new NotFoundException("Vinculo não encontrado");
        }
        return BeneficioAlunoMapper.toDTO(beneficioAluno);
    }

    @POST
    @Transactional
    public BeneficioAlunoDTO create(BeneficioAlunoDTO request) {
        BeneficioAluno beneficio = beneficioAlunoService.inserirAlunoBeneficio(request);
        return BeneficioAlunoMapper.toDTO(beneficio);
    }

    @PUT
    @Path("/{id}")
    @Transactional
    public BeneficioAlunoDTO update(@PathParam("id") Long id, BeneficioAlunoDTO updated) {
        BeneficioAluno beneficio = beneficioAlunoService.buscarPorId(id);
        if (beneficio == null) {
            throw new NotFoundException("Vinculo não encontrado");
        }

        beneficio.observacao = updated.observacao;
        beneficio.ativo = updated.ativo;

        return BeneficioAlunoMapper.toDTO(beneficio);
    }

    @DELETE
    @Path("/{id}")
    @Transactional
    public void delete(@PathParam("id") Long id) {
        boolean deleted = beneficioAlunoService.remover(id);
        if (!deleted) {
            throw new NotFoundException("Vinculo não encontrado");
        }
    }
}
```

```java
package com.seuprojeto.resource;

import java.util.List;

import com.seuprojeto.DTO.BeneficioDTO;
import com.seuprojeto.domain.Auxilio;
import com.seuprojeto.domain.Beneficio;
import com.seuprojeto.mapper.BeneficioMapper;
import com.seuprojeto.service.BeneficioService;    

import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.NotFoundException;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

@Path("/beneficio")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class BeneficioResource {

    @Inject
    BeneficioService beneficioService;

    @GET
    public List<Beneficio> listAll() {
        return beneficioService.listarBeneficio();
    }

    @GET
    @Path("/ativos")
    public List<Beneficio> listAtivos() {
        return beneficioService.listarBeneficiosAtivos();
    }

    @GET
    @Path("/{id}")
    public BeneficioDTO findById(@PathParam("id") Long id) {
        Beneficio beneficio = beneficioService.buscarPorId(id);
        if (beneficio == null) {
            throw new NotFoundException("Beneficio não encontrado");
        }
        return BeneficioMapper.toDTO(beneficio);
    }

    @POST
    @Transactional
    public BeneficioDTO create(BeneficioDTO beneficiorequest) {
        Beneficio beneficio = new Beneficio();
        beneficio.nome = beneficiorequest.nome;
        beneficio.descricao = beneficiorequest.descricao;
        beneficio.ativo = beneficiorequest.ativo;
        Auxilio aux = new Auxilio();
        aux.id = beneficiorequest.auxilioId;    
        beneficio.auxilio = aux;

        beneficioService.salvar(beneficio);
        return BeneficioMapper.toDTO(beneficio);
    }

    @PUT
    @Path("/{id}")
    @Transactional
    public BeneficioDTO update(@PathParam("id") Long id, BeneficioDTO updated) {
        Beneficio beneficio = beneficioService.buscarPorId(id);
        if (beneficio == null) {
            throw new NotFoundException("Beneficio não encontrado");
        }

        beneficio.nome = updated.nome;
        beneficio.descricao = updated.descricao;
        beneficio.ativo = updated.ativo;

        return BeneficioMapper.toDTO(beneficio);
    }

    @DELETE
    @Path("/{id}")
    @Transactional
    public void delete(@PathParam("id") Long id) {
        boolean deleted = beneficioService.remover(id);
        if (!deleted) {
            throw new NotFoundException("Beneficio não encontrado");
        }
    }
}
```



### 9. Testar a aplicação 

O Quarkus retorna ```http://localhost:8080``` como mensagem padrão, porém os caminhos certos para ver a aplicação são:

 ```http://localhost:8080/q/dev-ui``` → Interface de desenvolvimento do Quarkus onde você consegue acessar as extensões e documentação, como o Swagger.

```http://localhost:8080/aluno``` → Exemplo de API REST funcionando

#### Execute os comandos abaixo para rodar a aplicação localmente ```http://localhost:8080/q/dev-ui```

**IMPORTANTE:** O arquivo `GreetingResourceTest.java` é um teste automatizado da API REST criado automaticamente quando um projeto Quarkus é iniciado. Você precisa modificá-lo inserindo uma rota da sua aplicação (como `/auxilio`) para verificar se ela retorna uma resposta de sucesso (status 200). Esse teste é executado automaticamente quando você inicia a aplicação em modo desenvolvimento (`quarkus:dev`) e quando pressiona a tecla `r` no terminal do Quarkus. 

**Comando maven:** O projeto utiliza o Maven como ferramenta de build, e por isso deve ser executado por meio do arquivo mvnw.cmd. Esse arquivo é o Maven Wrapper, que já vem configurado no projeto e garante que o Maven correto será usado mesmo que você não tenha o Maven instalado na máquina. O Quarkus, ao iniciar, depende do Maven para compilar, resolver dependências e executar o servidor de desenvolvimento.

### CMD ou PowerShell
- O comando ```mvnw.cmd clean compile``` serve para apagar a pasta target/ (onde ficam os arquivos compilados), o que garante uma compilação limpa.
- O comando ```mvnw.cmd quarkus:dev``` inicia a aplicação no modo desenvolvimento.

``` bash
mvnw.cmd clean compile 
mvnw.cmd quarkus:dev 

#ou 

.\mvnw.cmd clean compile
.\mvnw.cmd quarkus:dev
```

### Linux e MAC
``` bash
./mvnw clean compile 
./mvnw quarkus:dev
```

### 10. Exemplos de requisição

Acesse o Swagger UI em: `http://localhost:8080/q/swagger-ui/`

#### 1. Criar um Aluno (POST /aluno)
```json
{
  "nome": "Pafinha Silva",
  "email": "pafinha.silva@email.com",
  "ativo": true
}
```

#### 2. Criar um Auxílio (POST /auxilio)
```json
{
  "titulo": "Auxílio Alimentação",
  "descricao": "Benefício mensal para alimentação dos estudantes",
  "ativo": true
}
```

#### 3. Criar um Benefício (POST /beneficio)
```json
{
  "nome": "Benefício da alimentação",
  "descricao": "Benefício específico de um aluno",
  "ativo": true,
  "auxilioId": 1
}
```
**Nota:** O `auxilioId` deve ser o ID de um auxílio existente (criado no passo 2).

#### 4. Vincular Aluno ao Benefício (POST /beneficioAluno)
```json
{
  "observacao": "Aluno em situação de vulnerabilidade social",
  "ativo": true,
  "alunoId": 1,
  "auxilioId": 1
}
```
**Nota:** Use os IDs dos registros criados anteriormente.

#### 5. Listar todos os Alunos (GET /aluno/lista)
Não precisa enviar corpo na requisição.

#### 6. Buscar Aluno por ID (GET /aluno/{id})
Substitua `{id}` pelo ID do aluno. Exemplo: `/aluno/1`

#### 7. Atualizar um Aluno (PUT /aluno/{id})
```json
{
  "nome": "Pafinha Silva Santos",
  "email": "pafinha.santos@email.com",
  "ativo": true
}
```

#### 8. Desativar um Benefício do Aluno (PUT /beneficioAluno/{id})
```json
{
  "observacao": "Aluna concluiu o curso",
  "ativo": false,
  "alunoId": 1,
  "auxilioId": 1
}
```

#### 9. Deletar um Auxílio (DELETE /auxilio/{id})
Substitua `{id}` pelo ID do auxílio a ser deletado.

#### 10. Testar Regra de Negócio - Aluno não pode ter o mesmo benefício ativo duas vezes (POST /beneficioAluno)

**Cenário:** Tente cadastrar o mesmo aluno no mesmo auxílio novamente (deve retornar erro).

Depois, tente cadastrar novamente com os mesmos IDs:
```json
{
  "observacao": "Tentando cadastrar duplicado",
  "ativo": true,
  "alunoId": 1,
  "auxilioId": 1
}
```

**Resultado esperado:** A API deve retornar um erro informando que o aluno já possui esse benefício ativo neste auxílio.

---

### Ordem Recomendada para Testar:

1. **POST /aluno** → Criar alunos
2. **POST /auxilio** → Criar auxílios
3. **POST /beneficio** → Criar benefícios (vinculados aos auxílios)
4. **POST /beneficioAluno** → Vincular alunos aos benefícios
5. **POST /beneficioAluno** (duplicado) → Testar regra de negócio
6. **GET** endpoints → Listar e consultar os dados criados
7. **PUT** endpoints → Atualizar registros
8. **DELETE** endpoints → Remover registros (cuidado com dependências!)
