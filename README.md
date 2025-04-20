
# Exercício de Fixação de Programação e Administração de Banco de Dados

Imagine que você é um desenvolvedor de software e precisa criar um banco de dados para uma aplicação de gerenciamento de biblioteca. O banco de dados deve conter informações sobre livros, autores e usuários.
O banco de dados deve ter as seguintes tabelas:
- **livros**: deve conter informações sobre os livros, como título, autor, ano de publicação e gênero.
- **autores**: deve conter informações sobre os autores, como nome, data de nascimento e nacionalidade.
- **usuários**: deve conter informações sobre os usuários, como nome, e-mail e data de registro.
- **empréstimos**: deve conter informações sobre os empréstimos de livros, como o ID do livro, o ID do usuário e a data de empréstimo.
- **reservas**: deve conter informações sobre as reservas de livros, como o ID do livro, o ID do usuário e a data da reserva.
- **multas**: deve conter informações sobre as multas aplicadas aos usuários, como o ID do usuário, o valor da multa e a data de pagamento.
- **categorias**: deve conter informações sobre as categorias dos livros, como o nome da categoria e a descrição.
- **editoras**: deve conter informações sobre as editoras dos livros, como o nome da editora e o endereço.
  

Você deve realizar as seguintes tarefas:
1. Definir o modelo conceitual do banco de dados:
   - Identificar as entidades, atributos e relacionamentos entre as tabelas.
   - Definir as chaves primárias e estrangeiras.
2. Criar o modelo lógico do banco de dados, incluindo as tabelas, colunas e tipos de dados.
3. Criar o modelo físico com a script SQL para criar as tabelas no banco de dados.
4. Inserir dados de exemplo em cada tabela.
5. Criar consultas SQL para responder às seguintes perguntas:
   - Quais são os livros disponíveis na biblioteca?
   - Quais são os usuários que mais solicitaram emprestimo de livros?
   - Quais são as multas pendentes?
   - Quais são os livros reservados por um usuário específico?
   - Quais os livros que não foram emprestados nos últimos 6 meses?
   - Quais os livros mais reservados?
   - Quais usuarios reservam mais livros?
   - Quais livros estão disponíveis para reserva?
   - Quais livros não estão disponíveis para empréstimo?
   - Liste de maneira agregada os livros por categoria.
  