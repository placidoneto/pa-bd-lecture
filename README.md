
# Exercício de Fixação de Programação e Administração de Banco de Dados

Imagine o exercício de fixação realizado em sala de aula para consultas SQL, mas agora com um tema diferente. Você deve criar os modelos, serializeres, views e rotas para uma API de acesso ao Banco de Dados para gerenciamento de biblioteca. 

Imagine que você é um desenvolvedor de software e precisa criar um banco de dados para uma aplicação de gerenciamento de biblioteca. O banco de dados deve conter informações sobre livros, autores e usuários.

O Modelo deve ter as seguintes classes:
- **livros**: deve conter informações sobre os livros, como título, autor, ano de publicação e gênero.
- **autores**: deve conter informações sobre os autores, como nome, data de nascimento e nacionalidade.
- **usuários**: deve conter informações sobre os usuários, como nome, e-mail e data de registro.
- **empréstimos**: deve conter informações sobre os empréstimos de livros, como o ID do livro, o ID do usuário e a data de empréstimo.
- **reservas**: deve conter informações sobre as reservas de livros, como o ID do livro, o ID do usuário e a data da reserva.
- **multas**: deve conter informações sobre as multas aplicadas aos usuários, como o ID do usuário, o valor da multa e a data de pagamento.
- **categorias**: deve conter informações sobre as categorias dos livros, como o nome da categoria e a descrição.
- **editoras**: deve conter informações sobre as editoras dos livros, como o nome da editora e o endereço.
  

Você deve realizar as seguintes tarefas:
1. Criar a configuração inicial para a implementação de um projeto Django Django Rest que ofereça acesso a uma API.
2. Criar os modelos de dados;
3. Criar os serializeres para os modelos;
4. Criar as views para os modelos;
5. Criar as rotas para os modelos;
6. Criar acesso a documentação da API usando Swagger;
7. Criar acesso a documentação da API usando Redoc;
8. Fazer os teste de API com o Postman ou algum outro software de sua preferência que possa testar as funções da API
9. Criar um arquivo README.md com as instruções de instalação e uso de acesso a API e suas respectivas funcionalidades.

**OBS: Neste primeiro momento não há necessidade de relacionar as tabelas. Os modelos devem ser independentes, sem interrelação.**