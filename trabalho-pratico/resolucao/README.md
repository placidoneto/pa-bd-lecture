# RESOLUÇÃO - Atividade prática: Gerenciar chamado de um Aluno relacionado a um Auxílio

Este documento descreve a resolução implementada para gerenciar chamados abertos por alunos relacionados a auxílios. 

Projeto: `trabalho-pratico/resolucao/quarkus-chamados`

Objetivo: permitir que Alunos registrem chamados, que sejam atendidos por Assistentes Sociais, vinculados a um Auxílio. A API oferece criação, consulta, resposta, fechamento e remoção de chamados, além de CRUDs básicos para Alunos, Auxílios e Assistentes Sociais.

---

## Estrutura da aplicação

O código da resolução está em `trabalho-pratico/resolucao/quarkus-chamados`. Principais pacotes:

- `com.tpquarkus.domain` — entidades JPA (Panache)
- `com.tpquarkus.DTO` — objetos de transferência (entrada/saída)
- `com.tpquarkus.mapper` — conversores DTO <-> Entity
- `com.tpquarkus.repository` — repositórios Panache
- `com.tpquarkus.service` — regras de negócio
- `com.tpquarkus.resource` — endpoints REST (Resources)
- `src/main/resources/application.properties` — configuração da aplicação

---

## 1. Configuração inicial

O projeto foi criado usanndo Quarkus com as extensões recomendadas: RESTEasy Reactive (Jackson), Hibernate ORM + Panache, Agroal, driver JDBC PostgreSQL e Swagger UI. Use o Maven Wrapper incluído no projeto.

Comandos úteis:

```bash
./mvnw clean compile
./mvnw quarkus:dev
```

Acesse a Dev UI e o Swagger quando o app estiver rodando:

- Dev UI: `http://localhost:8080/q/dev-ui`
- Swagger UI: `http://localhost:8080/q/swagger-ui/`

---

## 2. Configuração do PostgreSQL

Arquivo: `trabalho-pratico/resolucao/quarkus-chamados/src/main/resources/application.properties`

Valores usados pela solução:

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

Crie manualmente o banco `quarkuschamadosdb` ou ajuste a URL/usuário/senha conforme seu ambiente.

---

## 3. Resolução — Gerenciar Chamados de Alunos (Quarkus)

Resumo curto
 - Projeto: `trabalho-pratico/resolucao/quarkus-chamados`
 - Objetivo: permitir que Alunos registrem chamados vinculados a um Auxílio e sejam atendidos por Assistentes Sociais.
 - Padrão: Quarkus + Hibernate ORM (Panache) + RESTEasy Reactive + PostgreSQL.

### ENUM do status
```java
package com.tpquarkus;

public enum StatusChamado {
    ABERTO,
    EM_ANALISE,
    FECHADO
}
```

### Classes de domínio 

```java
package com.tpquarkus.domain;

import io.quarkus.hibernate.orm.panache.PanacheEntity;
import jakarta.persistence.Entity;

@Entity
public class Aluno extends PanacheEntity {

    public String nome;
    public String matricula;
    public String curso;
    public Boolean ativo;

}
```

```java
package com.tpquarkus.domain;
import io.quarkus.hibernate.orm.panache.PanacheEntity;
import jakarta.persistence.Entity;

@Entity
public class AssistenteSocial extends PanacheEntity {

    public String nome;
    public String matricula;
    public Boolean ativo;
}
```

```java 
package com.tpquarkus.domain;

import io.quarkus.hibernate.orm.panache.PanacheEntity;
import jakarta.persistence.Entity;


@Entity
public class Auxilio extends PanacheEntity {

    public String nome;
    public String descricao;
    public Boolean ativo;
}

```java
package com.tpquarkus.domain;

import io.quarkus.hibernate.orm.panache.PanacheEntity;
import jakarta.persistence.*;

import java.time.LocalDateTime;
import com.tpquarkus.StatusChamado;

@Entity
public class Chamado extends PanacheEntity {

    @Column(nullable = false)
    public String descricao;

    public String resposta;

    @Enumerated(EnumType.STRING)
    public StatusChamado status;

    public LocalDateTime dataAbertura;

    public LocalDateTime dataAnalise;

    @ManyToOne
    public Aluno aluno;

    @ManyToOne
    public AssistenteSocial assistenteSocial;

    @ManyToOne
    public Auxilio auxilio;

}
```

### Classes de DTO 

```java 
package com.tpquarkus.DTO;

public class AlunoDTO {
    public Long id;
    public String nome;
    public String matricula;
    public String curso;
    public Boolean ativo;
}
```

```java
package com.tpquarkus.DTO;

import jakarta.validation.constraints.NotBlank;

public class AssistenteSocialDTO {
    public Long id;

    @NotBlank(message = "O nome é obrigatório")
    public String nome;

    @NotBlank(message = "A matrícula é obrigatória")
    public String matricula;

    public Boolean ativo;
}
```

```java
package com.tpquarkus.DTO;

import jakarta.validation.constraints.NotBlank;

public class AuxilioDTO {
    public Long id;

    @NotBlank(message = "O nome do auxílio é obrigatório")
    public String nome;

    public String descricao;

    public Boolean ativo;
}
```

```java
package com.tpquarkus.DTO;
import java.time.LocalDateTime;
import jakarta.validation.constraints.NotBlank;

import com.tpquarkus.StatusChamado;

public class ChamadoDTO {
    public Long id;

    @NotBlank(message = "A descrição não pode estar vazia")
    public String descricao;

    public String resposta;
    public StatusChamado status;
    public LocalDateTime dataAbertura;
    public LocalDateTime dataAnalise;
    public Long alunoId;
    public Long assistenteSocialId;
    public Long auxilioId;
}
```

### Classes de mapeamento

```java
package com.tpquarkus.mapper;
import com.tpquarkus.DTO.AlunoDTO;
import com.tpquarkus.domain.Aluno;

public class AlunoMapper {
    // usado na api para entrada e saida de dados
    public static AlunoDTO toDTO(Aluno aluno) {
        AlunoDTO dto = new AlunoDTO();
        dto.id = aluno.id;
        dto.nome = aluno.nome;
        dto.matricula = aluno.matricula;
        dto.curso = aluno.curso;
        dto.ativo = aluno.ativo;
        return dto;
    }
    // usado  para persisitr o dado no banco
    public static Aluno toEntity(AlunoDTO dto) {
        Aluno aluno = new Aluno();
        aluno.nome = dto.nome;
        aluno.matricula = dto.matricula;
        aluno.curso = dto.curso;
        aluno.ativo = dto.ativo;
        return aluno;
    }    
}
```

```java
package com.tpquarkus.mapper;
import com.tpquarkus.DTO.AssistenteSocialDTO;
import com.tpquarkus.domain.AssistenteSocial;

public class AssistenteSocialMapper {
    // usado na api para entrada e saida de dados
    public static AssistenteSocialDTO toDTO(AssistenteSocial assistenteSocial) {
        AssistenteSocialDTO dto = new AssistenteSocialDTO();
        dto.id = assistenteSocial.id;
        dto.nome = assistenteSocial.nome;
        dto.matricula = assistenteSocial.matricula;
        dto.ativo = assistenteSocial.ativo;
        return dto;
    }

    // usado  para persisitr o dado no banco
    public static AssistenteSocial toEntity(AssistenteSocialDTO dto) {
        AssistenteSocial assistenteSocial = new AssistenteSocial();
        assistenteSocial.nome = dto.nome;
        assistenteSocial.matricula = dto.matricula;
        assistenteSocial.ativo = dto.ativo;
        return assistenteSocial;
    }
}
```

```java
package com.tpquarkus.mapper;
import com.tpquarkus.DTO.AuxilioDTO;
import com.tpquarkus.domain.Auxilio;

public class AuxilioMapper {

    public static AuxilioDTO toDTO(Auxilio auxilio) {
        AuxilioDTO dto = new AuxilioDTO();
        dto.id = auxilio.id;
        dto.nome = auxilio.nome;
        dto.descricao = auxilio.descricao;
        dto.ativo = auxilio.ativo;
        return dto;
    }
    public static Auxilio toEntity(AuxilioDTO dto) {
        Auxilio auxilio = new Auxilio();
        auxilio.nome = dto.nome;
        auxilio.descricao = dto.descricao;
        auxilio.ativo = dto.ativo;
        return auxilio;
    }    
}
```

```java
package com.tpquarkus.mapper;
import com.tpquarkus.DTO.ChamadoDTO;
import com.tpquarkus.domain.Chamado;
import com.tpquarkus.domain.Aluno;
import com.tpquarkus.domain.AssistenteSocial;
import com.tpquarkus.domain.Auxilio;

public class ChamadoMapper {
    public static ChamadoDTO toDTO(Chamado chamado) {
        ChamadoDTO dto = new ChamadoDTO();
        dto.id = chamado.id;
        dto.descricao = chamado.descricao;
        dto.resposta = chamado.resposta;
        dto.status = chamado.status;
        dto.dataAbertura = chamado.dataAbertura;
        dto.dataAnalise = chamado.dataAnalise;

        dto.alunoId = chamado.aluno.id;
        dto.assistenteSocialId = chamado.assistenteSocial.id;
        dto.auxilioId = chamado.auxilio.id;
        return dto;
    }

    public static Chamado toEntity(ChamadoDTO dto) {
        Chamado chamado = new Chamado();
        chamado.descricao = dto.descricao;
        chamado.status = dto.status;
        chamado.dataAbertura = dto.dataAbertura;
        chamado.dataAnalise = dto.dataAnalise;
        chamado.resposta = dto.resposta;

        Aluno aluno = new Aluno();
        aluno.id = dto.alunoId;
        chamado.aluno = aluno;

        AssistenteSocial assistenteSocial = new AssistenteSocial();
        assistenteSocial.id = dto.assistenteSocialId;
        chamado.assistenteSocial = assistenteSocial;

        Auxilio auxilio = new Auxilio();
        auxilio.id = dto.auxilioId;
        chamado.auxilio = auxilio;

        return chamado;
    }

}
```

### Classes de repositório
```java
package com.tpquarkus.repository;
import com.tpquarkus.domain.Aluno;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;

@ApplicationScoped
public class AlunoRepository implements PanacheRepository<Aluno>{
    //Retorna todos os alunos ativos 
    public List<Aluno> ativos(){
        return find("ativo", true).list();
    }

    //Retorna todos os alunos desativados
    public List<Aluno> desativados(){
        return find("ativo", false).list();
    }
}

```

```java
package com.tpquarkus.repository;
import com.tpquarkus.domain.AssistenteSocial;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;

@ApplicationScoped
public class AssistenteSocialRepository implements PanacheRepository<AssistenteSocial>{
    
}
```

```java
package com.tpquarkus.repository;
import com.tpquarkus.domain.Auxilio;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;

@ApplicationScoped
public class AuxilioRepository implements PanacheRepository<Auxilio>{
    //Retorna todos os auxilios ativos
    public List<Auxilio> ativos(){
        return find("ativo", true).list();
    }

    //Retorna todos os auxilio desativados
    public List<Auxilio> desativados(){
        return find("ativo", false).list();
    }

}
```

```java
package com.tpquarkus.repository;
import com.tpquarkus.StatusChamado;
import com.tpquarkus.domain.Chamado;

import io.quarkus.hibernate.orm.panache.PanacheRepository;
import jakarta.enterprise.context.ApplicationScoped;
import java.util.List;

@ApplicationScoped
public class ChamadoRepository implements PanacheRepository<Chamado>{
    //Busca chamado por status
    public List<Chamado> findByStatus(StatusChamado status){
        return find("status", status).list();
    }

    //Busca chamado por aluno
    public List<Chamado> findByAluno(String matricula){
        return find("aluno.matricula", matricula).list();
    }

    //Busca chamado por auxilio 
    public List<Chamado> findByAuxilio(String nome){
        return find("auxilio.nome", nome).list();
    }
}
```

### Classes de serviço

```java
package com.tpquarkus.service;

import com.tpquarkus.DTO.AlunoDTO;
import com.tpquarkus.domain.Aluno;
import com.tpquarkus.mapper.AlunoMapper;
import com.tpquarkus.repository.AlunoRepository;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.NotFoundException;
import io.quarkus.panache.common.Sort;
import java.util.List;
import java.util.stream.Collectors;

@ApplicationScoped
public class AlunoService {

    @Inject
    AlunoRepository alunoRepository;

    public List<AlunoDTO> listarTodos() {
        return alunoRepository.listAll(Sort.by("nome")).stream()
                .map(AlunoMapper::toDTO)
                .collect(Collectors.toList());
    }

    public AlunoDTO buscarPorId(Long id) {
        Aluno aluno = alunoRepository.findById(id);

        if (aluno == null) {
            throw new NotFoundException("Aluno não encontrado com o ID: " + id);
        }

        return AlunoMapper.toDTO(aluno);
    }

    @Transactional
    public AlunoDTO criar(AlunoDTO request) {
        if (alunoRepository.count("matricula", request.matricula) > 0) {
            throw new IllegalArgumentException("Já existe um aluno com esta matrícula.");
        }

        Aluno aluno = new Aluno();
        aluno.nome = request.nome;
        aluno.matricula = request.matricula;
        aluno.curso = request.curso;

        aluno.ativo = true;

        alunoRepository.persist(aluno);

        return AlunoMapper.toDTO(aluno);
    }

    public List<AlunoDTO> listarAtivos() {
        return alunoRepository.list("ativo", true).stream()
                .map(AlunoMapper::toDTO)
                .collect(Collectors.toList());
    }

    public List<AlunoDTO> listarDesativados() {
        return alunoRepository.list("ativo", false).stream()
                .map(AlunoMapper::toDTO)
                .collect(Collectors.toList());
    }

    @Transactional
    public AlunoDTO atualizar(Long id, AlunoDTO request) {
        Aluno aluno = alunoRepository.findById(id);

        if (aluno == null) {
            throw new NotFoundException("Aluno não encontrado");
        }

        aluno.nome = request.nome;
        aluno.curso = request.curso;

        if (request.ativo != null) {
            aluno.ativo = request.ativo;
        }

        return AlunoMapper.toDTO(aluno);
    }
}
```

```java
package com.tpquarkus.service;

import com.tpquarkus.DTO.AssistenteSocialDTO;
import com.tpquarkus.domain.AssistenteSocial;
import com.tpquarkus.mapper.AssistenteSocialMapper;
import com.tpquarkus.repository.AssistenteSocialRepository;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.NotFoundException;
import io.quarkus.panache.common.Sort;
import java.util.List;
import java.util.stream.Collectors;

@ApplicationScoped
public class AssistenteSocialService {

    @Inject
    AssistenteSocialRepository repository;

    public List<AssistenteSocialDTO> listarTodos() {
        return repository.listAll(Sort.by("nome")).stream()
                .map(AssistenteSocialMapper::toDTO)
                .collect(Collectors.toList());
    }

    public AssistenteSocialDTO buscarPorId(Long id) {
        AssistenteSocial entity = repository.findById(id);

        if (entity == null) {
            throw new NotFoundException("Assistente Social não encontrada com ID: " + id);
        }

        return AssistenteSocialMapper.toDTO(entity);
    }

    @Transactional
    public AssistenteSocialDTO criar(AssistenteSocialDTO request) {
        if (repository.count("matricula", request.matricula) > 0) {
            throw new IllegalArgumentException("Já existe uma Assistente Social com esta matrícula.");
        }

        AssistenteSocial entity = new AssistenteSocial();
        entity.nome = request.nome;
        entity.matricula = request.matricula;

        entity.ativo = (request.ativo != null) ? request.ativo : true;

        repository.persist(entity);

        return AssistenteSocialMapper.toDTO(entity);
    }
}
```

```java
package com.tpquarkus.service;

import com.tpquarkus.DTO.AuxilioDTO;
import com.tpquarkus.domain.Auxilio;
import com.tpquarkus.mapper.AuxilioMapper;
import com.tpquarkus.repository.AuxilioRepository;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.ws.rs.NotFoundException;
import io.quarkus.panache.common.Sort;
import java.util.List;
import java.util.stream.Collectors;

@ApplicationScoped
public class AuxilioService {

    @Inject
    AuxilioRepository repository;

    public List<AuxilioDTO> listarTodos() {
        return repository.listAll(Sort.by("nome")).stream()
                .map(AuxilioMapper::toDTO)
                .collect(Collectors.toList());
    }

    public AuxilioDTO buscarPorId(Long id) {
        Auxilio auxilio = repository.findById(id);

        if (auxilio == null) {
            throw new NotFoundException("Auxílio não encontrado com o ID: " + id);
        }

        return AuxilioMapper.toDTO(auxilio);
    }

    @Transactional
    public AuxilioDTO criar(AuxilioDTO request) {
        if (repository.count("LOWER(nome)", request.nome.toLowerCase()) > 0) {
            throw new IllegalArgumentException("Já existe um auxílio com este nome.");
        }

        Auxilio auxilio = new Auxilio();
        auxilio.nome = request.nome;
        auxilio.descricao = request.descricao;

        auxilio.ativo = (request.ativo != null) ? request.ativo : true;

        repository.persist(auxilio);

        return AuxilioMapper.toDTO(auxilio);
    }

    public List<AuxilioDTO> listarAtivos() {
        return repository.list("ativo", true).stream()
                .map(AuxilioMapper::toDTO)
                .collect(Collectors.toList());
    }

    public List<AuxilioDTO> listarDesativados() {
        return repository.list("ativo", false).stream()
                .map(AuxilioMapper::toDTO)
                .collect(Collectors.toList());
    }

    @Transactional
    public AuxilioDTO atualizar(Long id, AuxilioDTO request) {
        Auxilio auxilio = repository.findById(id);

        if (auxilio == null) {
            throw new NotFoundException("Auxílio não encontrado");
        }

        auxilio.nome = request.nome;
        auxilio.descricao = request.descricao;

        if (request.ativo != null) {
            auxilio.ativo = request.ativo;
        }

        return AuxilioMapper.toDTO(auxilio);
    }
}
```

```java
package com.tpquarkus.service;

import java.time.LocalDateTime;
import java.time.ZoneId;
import java.util.List;
import java.util.stream.Collectors;

import com.tpquarkus.DTO.ChamadoDTO;
import com.tpquarkus.StatusChamado;
import com.tpquarkus.domain.Aluno;
import com.tpquarkus.domain.AssistenteSocial;
import com.tpquarkus.domain.Auxilio;
import com.tpquarkus.domain.Chamado;
import com.tpquarkus.mapper.ChamadoMapper;
import com.tpquarkus.repository.AlunoRepository;
import com.tpquarkus.repository.AssistenteSocialRepository;
import com.tpquarkus.repository.AuxilioRepository;
import com.tpquarkus.repository.ChamadoRepository;

import io.quarkus.panache.common.Sort;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.inject.Inject;
import jakarta.transaction.Transactional;
import jakarta.validation.Valid;
import jakarta.ws.rs.NotFoundException;

@ApplicationScoped
public class ChamadoService {

    @Inject
    ChamadoRepository chamadoRepository;

    @Inject
    AlunoRepository alunoRepository;
    @Inject
    AssistenteSocialRepository assistenteSocialRepository;
    @Inject
    AuxilioRepository auxilioRepository;

    public List<ChamadoDTO> listarTodos() {
        return chamadoRepository.listAll(Sort.descending("dataAbertura")).stream()
                .map(ChamadoMapper::toDTO)
                .collect(Collectors.toList());
    }

    public ChamadoDTO buscarPorId(Long id) {
        Chamado chamado = chamadoRepository.findById(id);

        if (chamado == null) {
            throw new NotFoundException("Chamado não encontrado com o ID: " + id);
        }

        return ChamadoMapper.toDTO(chamado);
    }

    public List<ChamadoDTO> buscarPorStatus(StatusChamado status) {
        return chamadoRepository.list("status", status).stream()
                .map(ChamadoMapper::toDTO)
                .collect(Collectors.toList());
    }

    public List<ChamadoDTO> buscarPorMatriculaAluno(String matricula) {
        return chamadoRepository.list("aluno.matricula", matricula).stream()
                .map(ChamadoMapper::toDTO)
                .collect(Collectors.toList());
    }

    public List<ChamadoDTO> buscarPorNomeAuxilio(String nome) {
        return chamadoRepository.list("LOWER(auxilio.nome) = ?1", nome.toLowerCase()).stream()
                .map(ChamadoMapper::toDTO)
                .collect(Collectors.toList());
    }

    @Transactional
    public ChamadoDTO create(@Valid ChamadoDTO request) {
        Aluno aluno = alunoRepository.findById(request.alunoId);
        if (aluno == null) throw new NotFoundException("Aluno não encontrado");

        AssistenteSocial assistenteSocial = assistenteSocialRepository.findById(request.assistenteSocialId);
        if (assistenteSocial == null) throw new NotFoundException("Assistente Social não encontrado");

        Auxilio auxilio = auxilioRepository.findById(request.auxilioId);
        if (auxilio == null) throw new NotFoundException("Auxílio não encontrado");

        LocalDateTime agora = LocalDateTime.now(ZoneId.of("America/Sao_Paulo"));

        Chamado chamado = new Chamado();
        chamado.descricao = request.descricao;
        chamado.resposta = null;
        chamado.status = StatusChamado.ABERTO;
        chamado.dataAbertura = agora;
        chamado.dataAnalise = null;
        chamado.aluno = aluno;
        chamado.assistenteSocial = assistenteSocial;
        chamado.auxilio = auxilio;

        chamadoRepository.persist(chamado);

        return ChamadoMapper.toDTO(chamado);
    }

    @Transactional
    public ChamadoDTO responder(Long id, String resposta) {
        Chamado chamado = chamadoRepository.findById(id);
        if (chamado == null) {
            throw new NotFoundException("Chamado não encontrado");
        }

        chamado.resposta = resposta;
        chamado.status = StatusChamado.EM_ANALISE;
        chamado.dataAnalise = LocalDateTime.now(ZoneId.of("America/Sao_Paulo"));

        return ChamadoMapper.toDTO(chamado);
    }

    @Transactional
    public ChamadoDTO update(Long id, ChamadoDTO request) {
        Chamado chamado = chamadoRepository.findById(id);
        if (chamado == null) {
            throw new NotFoundException("Chamado não encontrado");
        }

        chamado.descricao = request.descricao;
        chamado.resposta = request.resposta;
        chamado.status = request.status;
        chamado.dataAnalise = request.dataAnalise;

        if (request.alunoId != null) {
            Aluno aluno = alunoRepository.findById(request.alunoId);
            if (aluno == null) throw new NotFoundException("Aluno não encontrado");
            chamado.aluno = aluno;
        }

        if (request.assistenteSocialId != null) {
            AssistenteSocial as = assistenteSocialRepository.findById(request.assistenteSocialId);
            if (as == null) throw new NotFoundException("Assistente Social não encontrada");
            chamado.assistenteSocial = as;
        }

        if (request.auxilioId != null) {
            Auxilio auxilio = auxilioRepository.findById(request.auxilioId);
            if (auxilio == null) throw new NotFoundException("Auxílio não encontrado");
            chamado.auxilio = auxilio;
        }

        if (request.resposta != null){
            chamado.status = StatusChamado.EM_ANALISE;
            chamado.dataAnalise = LocalDateTime.now(ZoneId.of("America/Sao_Paulo"));
        }

        return ChamadoMapper.toDTO(chamado);
    }

    @Transactional
    public ChamadoDTO close(Long id) {
        Chamado chamado = chamadoRepository.findById(id);
        if (chamado == null) {
            throw new NotFoundException("Chamado não encontrado");
        }

        if (chamado.status != StatusChamado.EM_ANALISE) {
            throw new IllegalStateException("Somente chamados em análise podem ser fechados");
        }

        chamado.status = StatusChamado.FECHADO;
        return ChamadoMapper.toDTO(chamado);
    }

    @Transactional
    public void delete(Long id) {
        boolean deletou = chamadoRepository.deleteById(id);

        if (!deletou) {
            throw new NotFoundException("Não foi possível deletar: Chamado não encontrado");
        }
    }
}
```

### Classes de resource

```java
package com.tpquarkus.resource;

import java.util.List;

import com.tpquarkus.DTO.AlunoDTO;
import com.tpquarkus.service.AlunoService;

import jakarta.inject.Inject;
import jakarta.validation.Valid;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;


@Path("/alunos")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AlunoResource {

    @Inject
    AlunoService service;

    @GET
    public List<AlunoDTO> list() {
        return service.listarTodos();
    }

    @GET
    @Path("/{id}")
    public AlunoDTO get(@PathParam("id") Long id) {
        return service.buscarPorId(id);
    }

    @POST
    public Response create(@Valid AlunoDTO dto) {
        AlunoDTO criado = service.criar(dto);
        return Response.status(Response.Status.CREATED).entity(criado).build();
    }

    @GET
    @Path("/ativo")
    public List<AlunoDTO> listActive() {
        return service.listarAtivos();
    }

    @GET
    @Path("/desativados")
    public List<AlunoDTO> listInactive() {
        return service.listarDesativados();
    }

    @PUT
    @Path("/{id}")
    public AlunoDTO update(@PathParam("id") Long id, @Valid AlunoDTO dto) {
        return service.atualizar(id, dto);
    }
}
```

```java
package com.tpquarkus.resource;

import java.util.List;

import com.tpquarkus.DTO.AssistenteSocialDTO;
import com.tpquarkus.service.AssistenteSocialService;
import jakarta.inject.Inject;
import jakarta.validation.Valid;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

@Path("/assistente_social")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AssistenteSocialResource {

    @Inject
    AssistenteSocialService service;

    @GET
    public List<AssistenteSocialDTO> list() {
        return service.listarTodos();
    }

    @GET
    @Path("/{id}")
    public AssistenteSocialDTO get(@PathParam("id") Long id) {
        return service.buscarPorId(id);
    }

    @POST
    public Response create(@Valid AssistenteSocialDTO dto) {
        AssistenteSocialDTO criado = service.criar(dto);
        return Response.status(Response.Status.CREATED).entity(criado).build();
    }
}
```

```java
package com.tpquarkus.resource;

import java.util.List;


import com.tpquarkus.DTO.AuxilioDTO;
import com.tpquarkus.service.AuxilioService;
import jakarta.inject.Inject;
import jakarta.validation.Valid;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

@Path("/auxilios")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class AuxilioResource {

    @Inject
    AuxilioService service;

    @GET
    public List<AuxilioDTO> list() {
        return service.listarTodos();
    }

    @GET
    @Path("/{id}")
    public AuxilioDTO get(@PathParam("id") Long id) {
        return service.buscarPorId(id);
    }

    @POST
    public Response create(@Valid AuxilioDTO dto) {
        AuxilioDTO criado = service.criar(dto);
        return Response.status(Response.Status.CREATED).entity(criado).build();
    }

    @GET
    @Path("/ativo")
    public List<AuxilioDTO> listActive() {
        return service.listarAtivos();
    }

    @GET
    @Path("/desativados")
    public List<AuxilioDTO> listInactive() {
        return service.listarDesativados();
    }

    @PUT
    @Path("/{id}")
    public AuxilioDTO update(@PathParam("id") Long id, @Valid AuxilioDTO dto) {
        return service.atualizar(id, dto);
    }
}
```

```java
package com.tpquarkus.resource;

import java.util.List;

import com.tpquarkus.DTO.ChamadoDTO;
import com.tpquarkus.StatusChamado;
import com.tpquarkus.service.ChamadoService;

import jakarta.inject.Inject;
import jakarta.ws.rs.Consumes;
import jakarta.ws.rs.DELETE;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.POST;
import jakarta.ws.rs.PUT;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.PathParam;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;


@Path("/chamados")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class ChamadoResource {

    @Inject
    ChamadoService chamadoService;

    @GET
    public List<ChamadoDTO> list() {

        return chamadoService.listarTodos();
    }

    @GET
    @Path("/{id}")
    public ChamadoDTO get(@PathParam("id") Long id) {

        return chamadoService.buscarPorId(id);
    }

    @GET
    @Path("/status/{status}")
    public List<ChamadoDTO> getByStatus(@PathParam("status") StatusChamado status) {

        return chamadoService.buscarPorStatus(status);
    }

    @GET
    @Path("/aluno/{matricula}")
    public List<ChamadoDTO> getByAluno(@PathParam("matricula") String matricula) {

        return chamadoService.buscarPorMatriculaAluno(matricula);
    }

    @GET
    @Path("/auxilio/{nome}")
    public List<ChamadoDTO> getByAuxilio(@PathParam("nome") String nome) {

        return chamadoService.buscarPorNomeAuxilio(nome);
    }

    @POST
    public ChamadoDTO create(ChamadoDTO dto) {

        return chamadoService.create(dto);
    }

    @PUT
    @Path("/{id}")
    public ChamadoDTO update(@PathParam("id") Long id, ChamadoDTO dto) {

        return chamadoService.update(id, dto);
    }

    @PUT
    @Path("/{id}/responder")
    public ChamadoDTO responder(@PathParam("id") Long id, String resposta) {

        return chamadoService.responder(id, resposta);
    }

    @PUT 
    @Path("/{id}/fechar")
    public ChamadoDTO fechar(@PathParam("id") Long id) {

        return chamadoService.close(id);
    }

    @DELETE
    @Path("/{id}")
    public Response delete(@PathParam("id") Long id) {
        chamadoService.delete(id);

        return Response.noContent().build();
    }
}
``` 
