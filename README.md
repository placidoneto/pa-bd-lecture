# Prova Final - Desenvolvimento de APIs com Django REST Framework

## Objetivo

O objetivo desta avaliação é praticar o uso de ViewSets, Routers e Filters no Django REST Framework para criar *endpoints* diversos de uma API Rest.

Você deverá se  basear no gerenciamento de livros em uma biblioteca. A API deve permitir a criação, listagem, atualização e exclusão de livros, autores e editoras.

## Descrição

Imagine que você foi contratado para desenvolver uma API REST para a Biblioteca Central do CNAT/IFRN. A API deve permitir o gerenciamento de livros, autores e editoras. Em geral, o domínio de uma biblioteca possui modelos base para gerenciamento de livros como: `Livro`, `Autor` e `Editora`. No entanto há também modelos de `Emprestimo` e `Reserva` que são relacionados com o modelo `Livro` e também com o modelo `Usuario` da biblioteca.

Nesse sentido, você deve criar os seguintes modelos e *endpoints* de CRUD para que a API da Biblioteca possa ser utilizada e consumida por um aplicativo de gerenciamento de biblioteca:

1. **Livros**
2. **Autores**
3. **Editoras**
4. **Emprestimos**
5. **Reservas**
6. **Usuarios**

Para melhorar a estrutura da API, você deve utilizar ViewSets e Routers do Django REST Framework para criar os *endpoints* de forma mais específicas, eficiente e organizada.

### Requisitos de Implementação
- Utilizar o Django REST Framework para criar a API.
- Utilizar ViewSets e Routers para criar os *endpoints*.
- Criar *endpoints* de CRUD para os modelos `Livro`, `Autor`, `Editora`, `Emprestimo`, `Reserva` e `Usuario`.
- Criar métodos customizados para os *endpoints* de `Emprestimo` e `Reserva` que permitam a consulta de empréstimos e reservas de um livro específico.
- Criar endpoints de pesquisa e filtragem com django filter para pelo menos 2 dos modelos `Livro`, `Autor`, `Editora`, `Emprestimo`, `Reserva` e `Usuario`.

## Entrega

A prova final deve ser entregue via GitHub Classroom, em um repositório privado. O repositório deve conter o código fonte do projeto, e um arquivo README.md na raiz do projeto com a descrição do modelo de dados.

[Link Assigment - Prova Final](https://classroom.github.com/a/yRDq53wP)
