# API REST com SpringBoot Java

## Alunos responsáveis

- Lucas
- Robson
- Victor
- Lucas Passos
- Romulo

## Vídeo da aula sobre Spring Boot

[Vídeo da aula sobre SpringBoot Java](https://drive.google.com/drive/folders/1eWShXi__HrOnjUZpPcjYiFNtamb2yPLI?usp=sharing)

## 🍃 Introdução ao Spring Boot com VSCode

O que vamos fazer?

Uma API REST com 4 CRUDs completos e multiplicidade. Para isso usaremos os módulos:

- Spring Web
- Spring Data JPA

## Começando o projeto

O Spring Boot tem uma forma não usual de criar um projeto: Vá até [https://start.spring.io/](spring.start.io) e selecione as sequintes opções:

- Project: Maven
- Spring Boot: Não altere
- Project Metadata: **Não altere**
- Dependencies: clique em "Add dependencies" e selecione as seguintes:

- Spring Web - O módulo principal do Spring
- Spring Data JPA - O ORM que usaremos
- PostgreSQL Driver - A conexão com o banco PostgresSQL
- Lombok - Anotações (decorators) que tornam o desenvolvimento mais dinâmico

Na parte inferior da página, clique em "GENERATE" e seu projeto vai estar criado dentro do .zip que seu navegador irá baixar.

Descompacte a pasta e a abra no seu editor de preferência.

## Vs Code

No Visual Studio Code é necessário instalar os seguintes pacotes

- Extension Pack for Java (da Microsoft) → Inclui suporte para Spring Boot
- Spring Boot Extension Pack → Facilita o desenvolvimento com Spring Boot

## Primeiro run

Vamos utilizar a forma mais simples de rodar nosso app: a linha de comando. Quando baixamos os arquivos iniciais do projeto, eles vieram com uma versão compacta do Maven, um gerenciador de pacotes do Java. Isso significa que você não precisa ter o maven instalado na sua máquina para executar o projeto.

no arquivo `application.properties` adicione as propriedades de conexão com o banco de dados:

```properties
    spring.application.name=demo
    spring.datasource.url=jdbc:postgresql://localhost:5432/seubanco
    spring.datasource.username=seuusername
    spring.datasource.password=suasenha
    spring.datasource.driver-class-name=org.postgresql.Driver
    spring.jpa.database-platform=org.hibernate.dialect.PostgreSQLDialect
    spring.jpa.hibernate.ddl-auto=update
```

Procure pelo arquivo `DemoApplicationTests.java` e adicione a linha de código

```java
    @SpringBootTest(classes = DemoApplication.class)
    public class DemoApplicationTests {
        // Seus testes aqui
    }
```
isso fará com que o teste procure especificamente o seu DemoApplication.class

Na raiz do projeto, execute o comando:

    ./mvnw spring-boot:run

Abra a url [localhost:8080](localhost:8080) no seu navegador.

Se você se deparar com a "Whitelabel error page", estamos indo bem.

## Implementando o Swagger

No seu arquivo `pom.xml`, adicione a dependência do Springdoc OpenApi.

```xml
    <dependency>
        <groupId>org.springdoc</groupId>
        <artifactId>springdoc-openapi-starter-webmvc-ui</artifactId>
        <version>2.3.0</version>
    </dependency>
```
Rode o comando abaixo para instalar as dependências

```bash
    ./mvnw clean install
```

Agora configure o swagger no `application.properties`

```properties
    # Ativar o Swagger
    springdoc.api-docs.enabled=true
    springdoc.swagger-ui.path=/swagger-ui.html
    springdoc.api-docs.path=/v3/api-docs
```

Rode a aplicação, para utilizar o swagger entre na URL [localhost:8080/swagger-ui.html](localhost:8080/swagger-ui.html)

## Criando o nosso CRUD

OBS.: Quando o projeto é criado, por padrão, também é criada uma pasta _/example_ antes da demo. Se faz necessário, então, mover a pasta demo para `src/main/java/com/`. Nesse sentido,  também deve ser feita a exclusão da pasta _/example_ para poder prosseguir com o tutorial.


Dentro da pasta `src/main/java/com/demo` vamos criar a pasta `/model` e adicionar o arquivo `Usuario.java` dentro. Vamos começar a declarar esse model:

```java
    package com.demo.model;

    import jakarta.persistence.*;
    import lombok.*;
    import com.fasterxml.jackson.annotation.JsonProperty
    
    @Entity
    @Data
    @NoArgsConstructor
    @AllArgsConstructor
    @Table(name = "usuarios")
    public class Usuario {
        
        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        @JsonProperty(access = JsonProperty.Access.READ_ONLY)
        private Long id;
        
        private String nome;
        private String email;
    }
```

Agora na mesma pasta `src/main/java/com/demo` vamos criar a pasta de Repositório `repository` e adicionar o arquivo `UsuarioRepository.java`.

```java
    package com.demo.repository;
    
    import com.demo.model.Usuario;
    import org.springframework.data.jpa.repository.JpaRepository;
    import org.springframework.stereotype.Repository;
    
    @Repository
    public interface UsuarioRepository extends JpaRepository<Usuario, Long> {
    }

```
O arquivo **`UsuarioRepository.java`** é responsável por fornecer acesso ao banco de dados para manipulação da entidade **`Usuario`**.

Ainda na mesma pasta `src/main/java/com/demo` vamos adicionar pasta `/service` e criar o arquivo `UsuarioService.java`


```java
    package com.demo.service;
    
    import com.demo.model.Usuario;
    import com.demo.repository.UsuarioRepository;
    import org.springframework.stereotype.Service;
    import java.util.List;
    
    @Service
    public class UsuarioService {
    
        private final UsuarioRepository usuarioRepository;
    
        public UsuarioService(UsuarioRepository usuarioRepository) {
            this.usuarioRepository = usuarioRepository;
        }
    
        public List<Usuario> listarUsuarios() {
            return usuarioRepository.findAll();
        }
    
        public Usuario buscarPorId(Long id) {
            return usuarioRepository.findById(id).orElseThrow(() -> new RuntimeException("Usuário não encontrado"));
        }
    
        public Usuario salvarUsuario(Usuario usuario) {
            return usuarioRepository.save(usuario);
        }
    
        public Usuario atualizarUsuario(Long id, Usuario usuarioAtualizado) {
            Usuario usuario = buscarPorId(id);
            usuario.setNome(usuarioAtualizado.getNome());
            usuario.setEmail(usuarioAtualizado.getEmail());
            return usuarioRepository.save(usuario);
        }
    
        public void deletarUsuario(Long id) {
            usuarioRepository.deleteById(id);
        }
    }
```

Por fim vamos adicionar a pasta `/controller` na mesma pasta `src/main/java/com/demo` e adicionar o arquivo `UsuarioController.java`

```java
    package com.demo.controller;
    
    import com.demo.model.Usuario;
    import com.demo.service.UsuarioService;
    import org.springframework.http.ResponseEntity;
    import org.springframework.web.bind.annotation.*;
    
    import java.util.List;
    
    @RestController
    @RequestMapping("/api/usuarios")
    public class UsuarioController {
    
        private final UsuarioService usuarioService;
    
        public UsuarioController(UsuarioService usuarioService) {
            this.usuarioService = usuarioService;
        }
    
        @GetMapping
        public List<Usuario> listarUsuarios() {
            return usuarioService.listarUsuarios();
        }
    
        @GetMapping("/{id}")
        public ResponseEntity<Usuario> buscarPorId(@PathVariable Long id) {
            return ResponseEntity.ok(usuarioService.buscarPorId(id));
        }
    
        @PostMapping
        public ResponseEntity<Usuario> criarUsuario(@RequestBody Usuario usuario) {
            return ResponseEntity.ok(usuarioService.salvarUsuario(usuario));
        }
    
        @PutMapping("/{id}")
        public ResponseEntity<Usuario> atualizarUsuario(@PathVariable Long id, @RequestBody Usuario usuario) {
            return ResponseEntity.ok(usuarioService.atualizarUsuario(id, usuario));
        }
    
        @DeleteMapping("/{id}")
        public ResponseEntity<Void> deletarUsuario(@PathVariable Long id) {
            usuarioService.deletarUsuario(id);
            return ResponseEntity.noContent().build();
        }
    }

```



[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/ysMqsypr)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=17905344)

# 🛠️ Trabalho Prático - Spring Boot

## 🎯 Objetivo

O objetivo deste trabalho é desenvolver um modelo de dados e uma CRUD básico em uma API REST para acesso aos dados.

## 📜 Descrição

Imagine que um tatuador quer registrar seus trabalhos em um aplicativo. Você foi designado para desenvolver a API REST desse sistema.

O tatuador quer saber, em cada tatuagem, qual foi o número do cliente, quando a tatuagem foi feita e qual o valor cobrado. Também deve haver um campo que armazene o estilo da tatuagem feita.

## 🗿 Requisitos de Entrega
- Baseado no contexto descrito, implementar uma API REST que permita a criação, leitura, atualização e exclusão de registros no banco de dados.
- A API deve ter todos os dados (classe e atributos) definidos no contexto;
- Todas as operações devem ser realizadas via API usando o Swagger;

O trabalho deve ser entregue de acordo com as instruções na [página do Google Classroom da disciplina de PABD](https://classroom.google.com/c/Njg1OTg3ODU3NDUz).
