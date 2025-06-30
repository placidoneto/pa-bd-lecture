# Trabalho Prático 6 - Autenticação com múltiplos perfis de usuário

Existem vários tipos de autenticação, mas o mais comum é o uso de login e senha. A autenticação pode ser feita para múltiplos perfis de usuário, como por exemplo, administrador, usuário comum, etc.

Um exemplo importante de autenticação é o uso de tokens, que são gerados pelo servidor e enviados para o cliente. O cliente deve enviar o token em todas as requisições subsequentes para o servidor, que irá verificar se o token é válido.

Imagine que você está desenvolvimento um sistema de uma loja de carros, onde existem três tipos de usuários: administrador, vendedor e cliente. Cada tipo de usuário tem um perfil diferente e deve ter acesso a funcionalidades diferentes do sistema.

O administrador deve ter acesso a todas as funcionalidades do sistema, incluindo a gestão de usuários, produtos e vendas. O vendedor deve ter acesso apenas às funcionalidades relacionadas às vendas, como a criação de novos pedidos e a consulta de vendas realizadas. O cliente deve ter acesso apenas às funcionalidades relacionadas à sua conta, como a consulta de pedidos e a atualização de dados pessoais.

Para implementar a autenticação com múltiplos perfis de usuário usando Django Rest Framework, você deve seguir os seguintes passos:

1. **Criar os modelos de usuário**: Crie um modelo de usuário que herde de `AbstractUser` e adicione um campo para o tipo de usuário (por exemplo, `is_admin`, `is_vendedor`, `is_cliente`).
2. **Criar os serializers**: Crie serializers para o modelo de usuário e para os perfis de usuário. O serializer do usuário deve incluir o campo de tipo de usuário.
3. **Criar as views**: Crie views para a autenticação e para a gestão de usuários. As views devem verificar o tipo de usuário e permitir o acesso apenas às funcionalidades permitidas.
4. **Configurar as URLs**: Configure as URLs para as views de autenticação e gestão de usuários.
5. **Testar a autenticação**: Teste a autenticação com diferentes tipos de usuário para garantir que cada perfil tem acesso apenas às funcionalidades permitidas.


Link para o assigment no GitClassroom: [Trabalho Prático 6 - Autenticação com múltiplos perfis de usuário](https://classroom.github.com/a/88X8jnab)