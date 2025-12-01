# Quarkus

## Introdução

Quarkus é um framework Java de código aberto desenvolvido pela Red Hat, lançado inicialmente em 20 de março de 2019. Ele surgiu para atender as demandas do mercado por aplicações cloud-native, microserviços e ambientes de containers, como Kubernetes. Seu objetivo é tornar o Java competitivo em ambientes modernos, entregando inicialização ultra rápida, baixo consumo de memória e suporte à compilação nativa.

Quarkus facilita o desenvolvimento para quem já utiliza Java, trazendo recursos de agilidade, integração ao ecossistema open source e produtividade superior.

No site oficial o framework é apreseando como "Java Subatômico Supersônico".

## Fundamentos e Arquitetura

### Principais Características

Apps criados com Quarkus iniciam em apenas alguns milissegundos (daí o supersônico) e consomem muito menos memória do que soluções Java convencionais (por isso o subatômico). O suporte à compilação nativa, via GraalVM, permite gerar executáveis altamente otimizados para ambientes cloud, reduzindo tempo de startup e footprint. Um dos grandes diferenciais para quem desenvolve é o live coding: basta salvar o código para ver as mudanças refletidas instantaneamente na aplicação, sem reinicializações.

Adotando padrões consagrados no universo Java, como JAX-RS (REST), CDI (injeção de dependências), Hibernate (persistência), além de oferecer integração com Kafka, MicroProfile e muitas outras bibliotecas, o framework é flexível e expansível para diferentes estilos de arquitetura.

### Arquitetura Interna

O núcleo do Quarkus utiliza Vert.x, fornecendo modelo de programação reativa, e Eclipse MicroProfile, que agrega padrões para APIs corporativas. Além disso, grande parte das configurações e otimizações é processada no build, proporcionando máxima eficiência em produção.

## Princípios RESTful com Quarkus

- Design orientado a recursos, com cada endpoint representando um recurso do sistema, manipulado por métodos HTTP (GET, POST, PUT, DELETE).
- Uso correto e semântico dos status HTTP para representar os resultados das operações.
- Serialização e deserialização automáticas em JSON, com opção de customização por bibliotecas como Jackson.
- Validação de dados e padronização de tratamento de erros, facilitando o consumo das APIs por clientes diversos.

## Ecossistema e Extensões

Quarkus é modular: você escolhe apenas as extensões (bibliotecas de integração) que precisa, mantendo sua aplicação enxuta, rápida e fácil de manter. Exemplos comuns de extensões:
- Persistência: Hibernate ORM, Panache, MongoDB, JDBC
- Segurança: JWT, OAuth2, OpenID Connect
- Mensageria: Kafka, RabbitMQ
- Observabilidade: Prometheus, OpenTelemetry

Extensões são facilmente instaladas via Maven ou Gradle, adequando o projeto às necessidades específicas.

## Comparativo com Outros Frameworks

| Framework     | Inicialização          | Consumo de Memória   | Tempo de compilação | Foco em Cloud Native   | Ecossistema      | Documentação     | Curva de aprendizado |
|---------------|------------------------|----------------------|---------------------|------------------------|------------------|------------------|----------------------|
| Micronaut     | Muitíssimo rápida      | Baixo                | Rápido              | Excelente              | Pouco abrangente | Limitada         | Moderada             |
| Quarkus       | Muito rápida           | Baixo a moderado     | Rápido              | Excelente              | Em crescimento   | Boa              | Moderada             |
| Spring Boot   | Mais lenta             | Alto                 | Lento               | Bom                    | Amplo            | Extensa          | Mais simples         |

### Detalhes

- **Micronaut** é destaque em velocidade de inicialização, principalmente em imagens nativas, com um footprint leve de memória graças à compilação antecipada (AOT) e ausência de reflexão em runtime.
- **Quarkus** oferece excelente suporte para ambientes cloud-native, com integração nativa a Kubernetes e GraalVM, equilibrando performance com um ecossistema crescente e foco em produtividade.
- **Spring Boot** possui maior maturidade, ecosistema extenso e é amplamente adotado na indústria, porém com startup mais lenta e consumo mais alto de memória, especialmente em JVM (Java Virtual Machine) tradicional.

Essa tabela  construída com base em análises e benchmarks detalhados encontrados em:  
- https://www.brilworks.com/blog/spring-boot-vs-quarkus-vs-micronaut/  
- https://www.indium.tech/blog/micronauat-quarkus-spring-boot-native-java-framework/
- https://blog.stackademic.com/%EF%B8%8F-java-frameworks-showdown-2025-spring-boot-vs-quarkus-vs-micronaut-f5828fa11139

## Melhores Práticas com Quarkus

Configure endpoints REST utilizando JAX-RS. Implemente validação e tratamento global de erros, sempre padronizando respostas. Para testes, utilize exemplos didáticos e o recurso Quarkus Dev Services (com containers integrados para bancos de dados, mensageria e outros serviços de apoio).

A documentação oficial é um excelente ponto de partida para aprender de forma incremental, explorando cada guia, extensão e cenário de uso à medida que evolui o seu conhecimento.

## Exemplo Simples — Começando com Quarkus

Este exemplo mostra como criar e executar uma aplicação simples usando Quarkus, seguindo os passos básicos para começar desenvolvendo uma API RESTful.

### Passo 1 — Instalação do Quarkus CLI

Para iniciar, instale o Quarkus CLI pelo terminal. Você pode usar JBang, que não exige Java previamente instalado.

#### No Linux, macOS ou Windows (usando WSL, Cygwin, MinGW ou bash compatível):
```
curl -Ls https://sh.jbang.dev | bash -s - trust add https://repo1.maven.org/maven2/io/quarkus/quarkus-cli/
curl -Ls https://sh.jbang.dev | bash -s - app install --fresh --force quarkus@quarkusio
```

#### No Windows (PowerShell):
```
iex "& { $(iwr https://ps.jbang.dev) } trust add https://repo1.maven.org/maven2/io/quarkus/quarkus-cli/"
iex "& { $(iwr https://ps.jbang.dev) } app install --fresh --force quarkus@quarkusio"
```

### Passo 2 — Criar o Projeto Inicial

No terminal, crie seu projeto Quarkus com o comando:
```
quarkus create app com.seuprojeto:meuprojeto && cd meuprojeto
````

### Passo 3 — Executar a Aplicação

Para rodar a aplicação em modo desenvolvimento com hot reload:
```
quarkus dev
```
Sua aplicação Quarkus estará rodando localmente em:
```
http://localhost:8080/q/dev-ui/extensions
````

### Passo 4 — Live Coding (Hot Reload)

Edite o arquivo `src/main/java/org/acme/GreetingResource.java` para modificar o texto retornado pelo endpoint REST.

Exemplo do conteúdo do arquivo:
```java
@Path("/hello")
public class GreetingResource {

    @GET
    @Produces(MediaType.TEXT_PLAIN)
    public String hello() {
        return "Hello RESTEasy";
    }
}
```
Altere a mensagem `"Hello RESTEasy"` para, por exemplo, `"Seminário Quarkus"`. Salve a modificação e atualize seu navegador para ver a mudança refletida instantaneamente, sem precisar reiniciar o servidor.

---

Esse fluxo simples está presente no site ofical do [Quarkus](https://pt.quarkus.io/get-started/) e demonstra a rapidez e a facilidade de desenvolvimento com Quarkus, especialmente seu suporte a live reload para desenvolvimento ágil de APIs RESTful.

## Material de Apoio

- [Documentação oficial do Quarkus](https://quarkus.io/)
- [Guia de primeiros passos](https://quarkus.io/guides/getting-started)
- [Quarkus — Wikipédia](https://pt.wikipedia.org/wiki/Quarkus_framework)
- [Guia Quarkus — Baeldung (inglês)](https://www.baeldung.com/quarkus-io)
- [Quarkus para Iniciantes — Kranio (inglês)](https://www.kranio.io/en/blog/quarkus-para-principiantes-soluciones-practicas-para-7-escenarios-iniciales)
