# Autenticação em Django Rest Framework Usando Perfil de Usuário

Na maioria das aplicações há a necessidade de autenticação de usuários. O Django Rest Framework (DRF) possui um sistema de autenticação que é bastante flexível e pode ser customizado para atender as necessidades de diferentes aplicações. Neste tutorial, vamos ver como autenticar usuários usando o perfil de usuário.

Os modelos da aplicação se relacionam com tipode usuario diferentes. Por exemplo, um sistema acadêmico pode ter os seguintes tipos de usuários: aluno, professor e coordenador. Cada tipo de usuário tem suas próprias características e permissões. O modelo de usuário do Django é bastante flexível e permite a criação de diferentes tipos de usuários. No entanto, o modelo de usuário padrão do Django não é suficiente para atender a todas as necessidades de uma aplicação. Por isso, é comum criar um modelo de perfil de usuário para armazenar informações adicionais sobre o usuário.  

Para criação de modelos que permitam a autenticação de diferentes tipos de usuários, é necessário criar um modelo de perfil de usuário que estenda o modelo de usuário padrão do Django. O modelo de perfil de usuário deve conter os campos necessários para armazenar as informações adicionais sobre o usuário. Além disso, é necessário criar um serializer para o modelo de perfil de usuário e um viewset para permitir a criação, atualização e exclusão de perfis de usuário.

O modelo `AbstractUser`  do Django é uma classe abstrata que pode ser estendida para criar um modelo de perfil de usuário. O modelo `AbstractUser` contém os campos básicos de um usuário, como nome de usuário, email, senha, etc. Para criar um modelo de perfil de usuário, basta criar uma classe que estenda o modelo AbstractUser e adicionar os campos adicionais necessários. Por exemplo, o modelo de perfil de usuário pode conter campos como nome, sobrenome, data de nascimento, etc.

```python

from django.contrib.auth.models import AbstractUser

class User(AbstractUser): # modelo de perfil de usuário (esse usuário User não é a classe de autenticação do Django)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    data_nascimento = models.DateField()
    PERFIL = (
        ('admin', 'Administrador'),
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
        ('coordenador', 'Coordenador'),
        ('diretor', 'Diretor'),
    )

    perfil = models.CharField(max_length=15, choices=PERFIL)
    # outros campos

```

O serializer do modelo de perfil de usuário deve ser criado para permitir a serialização e desserialização dos objetos do modelo. O serializer deve conter os campos do modelo de perfil de usuário que serão serializados e desserializados. Além disso, o serializer deve conter métodos para validar os dados recebidos e criar ou atualizar objetos do modelo de perfil de usuário.

```python

from rest_framework import serializers
from .models import User

class Meta:
        model = User
        fields = ['username', 'email', 'perfil', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

```

A variável `extra_kwargs` é usada para definir opções adicionais para os campos do serializer. Neste caso, estamos definindo que o campo `password` é de escrita apenas, ou seja, ele não será incluído na resposta da API.

A função `create` é usada para criar um novo objeto do modelo de perfil de usuário com os dados validados recebidos da requisição. Neste caso, estamos criando um novo usuário usando o método `create_user` do modelo de perfil de usuário.

O método `create_user` é um método personalizado que deve ser criado no modelo de perfil de usuário para criar um novo usuário. O método `create_user` deve receber os dados necessários para criar um novo usuário e retornar o novo usuário criado.

Uma vez definido o serializer, é necessário criar um viewset para permitir a criação, atualização e exclusão de perfis de usuário. Além disso, o viewset deve conter métodos para autenticar usuários e gerar tokens de autenticação.

```python
class RegistroUsuarioView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

```

O método `post` da classe `RegistroUsuarioView` é usado para criar um novo perfil de usuário com os dados recebidos da requisição. O método verifica se os dados recebidos são válidos usando o método `is_valid` do serializer. Se os dados forem válidos, o método `save` do serializer é chamado para criar um novo perfil de usuário. Em seguida, a resposta da API é retornada com os dados do novo perfil de usuário e o status HTTP 201 CREATED.

O método `is_valid` é usado para verificar se os dados recebidos da requisição são válidos de acordo com as regras de validação definidas no serializer. Se os dados forem válidos, o método `is_valid` retorna `True`, caso contrário, retorna `False`.

O método `save` é usado para criar um novo objeto do modelo de perfil de usuário com os dados validados recebidos da requisição. O método `save` retorna o objeto criado.

O método `Response` é usado para retornar a resposta da API com os dados do perfil de usuário e o status HTTP. O método `Response` recebe dois argumentos: os dados a serem retornados e o status HTTP da resposta.

O status HTTP 201 CREATED é usado para indicar que um novo recurso foi criado com sucesso. O status HTTP 400 BAD REQUEST é usado para indicar que a requisição não pôde ser processada devido a erros nos dados recebidos.

```python



class LoginUsuarioView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            token, created = Token.objects.get_or_create(user=usuario)
            if created:
                token.delete()  
                token = Token.objects.create(user=usuario)
            return Response({'token': token.key, 'username': usuario.username, 'perfil': usuario.perfil})
        else:
            return Response({'mensagem': 'Login ou Senha Inválido'}, status=status.HTTP_401_UNAUTHORIZED)

```

O método `post` da classe `LoginUsuarioView` é usado para autenticar um usuário com os dados recebidos da requisição. O método verifica se o usuário e a senha recebidos são válidos usando a função `authenticate` do Django. Se o usuário e a senha forem válidos, um token de autenticação é gerado usando a função `get_or_create` do modelo de token de autenticação. Se o token já existir, ele é excluído e um novo token é criado. Em seguida, a resposta da API é retornada com o token de autenticação, o nome de usuário e o perfil do usuário autenticado.

O método `authenticate` é usado para autenticar um usuário com o nome de usuário e a senha recebidos da requisição. Se o usuário e a senha forem válidos, a função `authenticate` retorna o usuário autenticado, caso contrário, retorna `None`.

O método `login` é usado para autenticar um usuário na sessão atual. O método `login` recebe dois argumentos: o objeto de requisição e o usuário a ser autenticado.

O método `get_or_create` é usado para obter ou criar um objeto do modelo de token de autenticação para o usuário autenticado. Se o token já existir, ele é retornado, caso contrário, um novo token é criado.

O método `delete` é usado para excluir um objeto do modelo de token de autenticação. O método `delete` recebe o objeto a ser excluído como argumento.

O método `create` é usado para criar um novo objeto do modelo de token de autenticação para o usuário autenticado. O método `create` recebe o usuário a ser autenticado como argumento e retorna o novo objeto criado.

O status HTTP 401 UNAUTHORIZED é usado para indicar que a requisição não foi autorizada devido a credenciais inválidas.

```python


class LogoutUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.headers) 
        token_key = request.auth.key
        token = Token.objects.get(key=token_key)
        token.delete()

        return Response({'detail': 'Usuário deslogado com sucesso.'})

```

O método `post` da classe `LogoutUsuarioView` é usado para deslogar um usuário autenticado. O método verifica se o usuário está autenticado usando a classe `IsAuthenticated` do Django Rest Framework. Em seguida, o token de autenticação do usuário é obtido a partir do cabeçalho da requisição e excluído. Por fim, a resposta da API é retornada com a mensagem de sucesso.

O cabeçalho da requisição contém informações sobre a requisição, como o tipo de conteúdo, o tamanho do conteúdo, etc. O cabeçalho da requisição é um dicionário que contém pares chave-valor, onde a chave é o nome do cabeçalho e o valor é o valor do cabeçalho.

O método `get` é usado para obter o valor de um cabeçalho da requisição. O método `get` recebe o nome do cabeçalho como argumento e retorna o valor do cabeçalho.

O método `delete` é usado para excluir um objeto do modelo de token de autenticação. O método `delete` recebe o objeto a ser excluído como argumento.

O status HTTP 401 UNAUTHORIZED é usado para indicar que a requisição não foi autorizada devido a credenciais inválidas.

```python

from django.urls import path

from .views import RegistroUsuarioView, LoginUsuarioView, LogoutUsuarioView

urlpatterns = [
    path('api/auth/registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('api/auth/login/', LoginUsuarioView.as_view(), name='login'),
    path('api/auth/logout/', LogoutUsuarioView.as_view(), name='logout'),
]

```

As rotas da API são definidas no arquivo `urls.py` da aplicação. As rotas são mapeadas para as views correspondentes usando a função `path`. A função `path` recebe três argumentos: o padrão da rota, a view correspondente e o nome da rota.

O padrão da rota é uma string que define o padrão da URL da rota. O padrão da rota pode conter variáveis de caminho, que são definidas entre chaves `{}`. As variáveis de caminho são capturadas da URL da requisição e passadas para a view correspondente como argumentos.

A view correspondente é uma classe ou função que processa a requisição e retorna a resposta da API. A view pode ser uma classe baseada em função, uma classe baseada em método ou uma função baseada em classe.

## Migrações

Para criar as tabelas no banco de dados, é necessário executar as migrações. As migrações são arquivos Python que contêm as instruções SQL para criar as tabelas no banco de dados. As migrações são geradas automaticamente pelo Django quando são feitas alterações nos modelos da aplicação.

Para criar as migrações, execute o seguinte comando:

```bash
python manage.py makemigrations
```

Para aplicar as migrações, execute o seguinte comando:

```bash
python manage.py migrate
```

Os comandos `makemigrations` e `migrate` devem ser usado sempre que houver alterações nos modelos da aplicação. Os comandos geram as migrações necessárias para criar as tabelas no banco de dados e aplicam as migrações para criar as tabelas.

É importante verificar se a tabela `api_user` foi criada no banco de dados. Caso contrário, é necessário verificar se as migrações foram aplicadas corretamente. Essa tabela é criada para armazenar os perfis de usuário da sua aplicação. Essa tabela é diferente da tabela `auth_user` que é criada pelo Django para armazenar os usuários autenticados. A tabela `api_user` é criada para armazenar os perfis de usuário personalizados da sua aplicação.

## Testando a API

Para testar a API, é necessário usar um cliente HTTP, como o Postman ou o Insomnia. O cliente HTTP é usado para enviar requisições HTTP para a API e visualizar as respostas da API. O cliente HTTP permite testar as diferentes rotas da API e verificar se a API está funcionando corretamente.

Para testar a rota de registro de usuário, envie uma requisição POST para a rota `/api/auth/registro/` com os dados do usuário a ser registrado. Os dados do usuário devem ser enviados no corpo da requisição no formato JSON. A resposta da API deve conter os dados do usuário registrado e o status HTTP 201 CREATED.

```python

{
    "username": "usuario",
    "email": "usuario@email.com",
    "perfil": "admin",
    "password": "senha"

}

```

Para executar é possível usar a ferramenta `Postman` para testar as rotas da API. 


Para testar a rota de login de usuário, envie uma requisição POST para a rota `/api/auth/login/` com o nome de usuário e a senha do usuário a ser autenticado. Os dados do usuário devem ser enviados no corpo da requisição no formato JSON. A resposta da API deve conter o token de autenticação, o nome de usuário e o perfil do usuário autenticado e o status HTTP 200 OK.

```python

{
    "username": "usuario",
    "password": "senha"
}

``` 

Para testar a rota de logout de usuário, envie uma requisição POST para a rota `/api/auth/logout/` com o token de autenticação do usuário autenticado. O token de autenticação deve ser enviado no cabeçalho da requisição no formato `Authorization: Token <token>`. A resposta da API deve conter a mensagem de sucesso e o status HTTP 200 OK.

```python

Authorization: Token <token>

``` 

## Frontend React-Vite

```
npm create vite@latest front-autenticacao -- --template react

cd front-autenticacao

npm install

npm run dev
```

O código de instalação do React utilizando Vite é bastante simples e eficiente. O comando `npm create vite@latest front-autenticacao -- --template react` cria um novo projeto React chamado `front-autenticacao` utilizando o Vite como ferramenta de construção. O Vite é uma ferramenta moderna que oferece um ambiente de desenvolvimento rápido e otimizado, permitindo que os desenvolvedores aproveitem recursos como recarregamento a quente e construção rápida de pacotes. O uso do template `react` garante que a estrutura inicial do projeto já esteja configurada para um aplicativo React.

Após a criação do projeto, o comando `cd front-autenticacao` é utilizado para navegar até o diretório do projeto recém-criado. Em seguida, o comando `npm install` instala todas as dependências necessárias para o projeto, conforme especificado no arquivo `package.json`. Isso inclui bibliotecas essenciais para o funcionamento do React e do Vite. Por fim, o comando `npm run dev` inicia o servidor de desenvolvimento, permitindo que você visualize e interaja com seu aplicativo React em um navegador, facilitando o processo de desenvolvimento e testes.

## Estrutura do Projeto

O arquivo `App.jsx` é o componente principal inicial do projeto Vite. Ele serve como o ponto de entrada para a aplicação React, onde a estrutura e a lógica do aplicativo são definidas. Dentro do `App.jsx`, você pode organizar seus componentes, gerenciar estados e implementar a lógica de navegação.

O arquivo `main.jsx` é responsável por incorporar o `App` e inicializar a aplicação. Ele utiliza a função `createRoot` do React para renderizar o componente `App` no DOM. Essa abordagem permite que o React gerencie a interface do usuário de forma eficiente, garantindo que as atualizações sejam refletidas rapidamente na tela.

```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

Neste exemplo, o `main.jsx` importa o `App` e o renderiza dentro do elemento com o ID `root`, que é onde a aplicação será exibida no navegador.


## Configuração de CORS no Backend

Para permitir que o frontend React se comunique com o backend Django, é necessário configurar o CORS (Cross-Origin Resource Sharing). O CORS é um mecanismo de segurança que permite ou restringe solicitações HTTP de diferentes origens. Sem a configuração adequada, o navegador bloqueará as requisições do frontend para o backend.

### Instalação do django-cors-headers

Primeiro, instale o pacote `django-cors-headers`:

```bash
pip install django-cors-headers
```

### Configuração no settings.py

Adicione `corsheaders` à lista de aplicativos instalados e configure o middleware:

```python
INSTALLED_APPS = [
  # ...
  'corsheaders',
  'rest_framework',
  'rest_framework.authtoken',
  # ...
]

MIDDLEWARE = [
  'corsheaders.middleware.CorsMiddleware',  # Deve estar no topo
  'django.middleware.common.CommonMiddleware',
  # ...
]

# Permitir requisições do frontend em desenvolvimento
CORS_ALLOWED_ORIGINS = [
  "http://localhost:5173",  # Porta padrão do Vite
  "http://127.0.0.1:5173",
]

# Ou, apenas para desenvolvimento, permitir todas as origens (não recomendado em produção)
# CORS_ALLOW_ALL_ORIGINS = True
```

A configuração `CORS_ALLOWED_ORIGINS` especifica quais origens podem fazer requisições ao backend. No desenvolvimento, permitimos as URLs locais onde o Vite executa (porta 5173). Sem essa configuração, o navegador bloqueará requisições AJAX do frontend para o backend, exibindo erros de CORS no console.


## Implementação da Página de Registro no React

Além da página de login, é necessário criar uma página de registro para permitir que novos usuários se cadastrem na aplicação. O componente `Registro.jsx` se comunica com a API de registro do Django para criar novos perfis de usuário.

Crie um arquivo `Registro.jsx` na pasta `src`:

```javascript
import { useState } from 'react';
import './Registro.css';

function Registro() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    perfil: 'admin',
    password: ''
  });

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const perfis = [
    { value: 'admin', label: 'Administrador' },
    { value: 'professor', label: 'Professor' },
    { value: 'aluno', label: 'Aluno' },
    { value: 'coordenador', label: 'Coordenador' },
    { value: 'diretor', label: 'Diretor' }
  ];

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validação básica
    if (!formData.username || !formData.email || !formData.password) {
      setError('Todos os campos são obrigatórios');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/auth/registro/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        const data = await response.json();
        setSuccess('Usuário registrado com sucesso!');
        setFormData({
          username: '',
          email: '',
          perfil: 'admin',
          password: ''
        });
      } else {
        const errorData = await response.json();
        setError(errorData.message || 'Erro ao registrar usuário');
      }
    } catch (err) {
      setError('Erro de conexão com o servidor');
    }
  };

  return (
    <div className="registro-container">
      <h2>Registro de Usuário</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Nome de Usuário:</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="perfil">Perfil:</label>
          <select
            id="perfil"
            name="perfil"
            value={formData.perfil}
            onChange={handleChange}
            required
          >
            {perfis.map((perfil) => (
              <option key={perfil.value} value={perfil.value}>
                {perfil.label}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="password">Senha:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        <button type="submit">Registrar</button>
      </form>
    </div>
  );
}

export default Registro;

```


### Explicação do Código

O componente `Registro.jsx` segue uma estrutura similar ao componente de login, mas com funcionalidades adicionais específicas para o cadastro de novos usuários. O hook `useState` é utilizado para gerenciar cinco campos de entrada: `username`, `email`, `password`, `confirmPassword` e `perfil`, além dos estados de erro e sucesso.

A função `handleChange` captura as mudanças em todos os campos do formulário, atualizando o estado `formData` dinamicamente. Isso permite que o componente mantenha os valores inseridos pelo usuário de forma reativa.

A função `handleSubmit` implementa validações no lado do cliente antes de enviar os dados para a API. Primeiro, verifica se todos os campos obrigatórios foram preenchidos. Em seguida, compara os campos `password` e `confirmPassword` para garantir que o usuário digitou a mesma senha duas vezes, prevenindo erros de digitação. Também valida o tamanho mínimo da senha, garantindo que tenha pelo menos 6 caracteres.

Após as validações locais, a função realiza uma requisição POST para o endpoint `/api/auth/registro/` do Django. Note que apenas os campos necessários (`username`, `email`, `password` e `perfil`) são enviados no corpo da requisição, excluindo o campo `confirmPassword`, que é usado apenas para validação no frontend.

O campo `perfil` é renderizado como um elemento `<select>`, permitindo que o usuário escolha entre os diferentes tipos de perfil disponíveis na aplicação (aluno, professor, coordenador, diretor e administrador). Esses valores correspondem às opções definidas no modelo `Usuario` do Django.

Quando o registro é bem-sucedido, uma mensagem de sucesso é exibida e o formulário é limpo, permitindo que o usuário seja redirecionado para a página de login. O tratamento de erros captura tanto erros de validação retornados pela API quanto erros de conexão, exibindo mensagens apropriadas ao usuário.

A estilização utiliza cores diferentes do componente de login (verde em vez de azul) para diferenciar visualmente as ações de registro das ações de login, melhorando a experiência do usuário através de pistas visuais consistentes.


## Implementação da Página de Login no React

Uma página de login funcional se comunica com a API de autenticação do Django. Primeiro, crie um componente `Login.jsx` na pasta `src`:

```javascript
import { useState } from 'react';
import './Login.css';

function Login() {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });

  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validação básica
    if (!formData.username || !formData.password) {
      setError('Todos os campos são obrigatórios');
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/api/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        const data = await response.json();
        setSuccess('Login realizado com sucesso!');

        // Armazenar o token no localStorage
        if (data.token) {
          localStorage.setItem('token', data.token);
        }

        // Limpar o formulário
        setFormData({
          username: '',
          password: ''
        });

        // Aqui você pode redirecionar o usuário ou atualizar o estado global
        console.log('Login successful:', data);
      } else {
        const errorData = await response.json();
        setError(errorData.mensagem || errorData.message || 'Credenciais inválidas');
      }
    } catch (err) {
      console.error('Erro completo:', err);
      setError('Erro de conexão com o servidor: ' + err.message);
    }
  };

  return (
    <div className="login-container">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="username">Nome de Usuário:</label>
          <input
            type="text"
            id="username"
            name="username"
            value={formData.username}
            onChange={handleChange}
            required
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Senha:</label>
          <input
            type="password"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
          />
        </div>

        {error && <div className="error-message">{error}</div>}
        {success && <div className="success-message">{success}</div>}

        <button type="submit">Entrar</button>
      </form>
    </div>
  );
}

export default Login;

```

### Atualização do App.jsx

Modifique o arquivo `App.jsx` para incluir o componente de login:

```javascript
import { useState } from 'react'
import './App.css'
import Login from './Login'
import Registro from './Registro'

function App() {
  const [showLogin, setShowLogin] = useState(true)

  return (
    <div className="App">
      <div className="toggle-container">
        <button
          className={showLogin ? 'active' : ''}
          onClick={() => setShowLogin(true)}
        >
          Login
        </button>
        <button
          className={!showLogin ? 'active' : ''}
          onClick={() => setShowLogin(false)}
        >
          Registro
        </button>
      </div>

      {showLogin ? <Login /> : <Registro />}
    </div>
  )
}

export default App

```

## Conclusão

Nesta aula vimos como autenticar usuários usando o perfil de usuário no Django Rest Framework. Criamos um modelo de perfil de usuário que estende o modelo de usuário padrão do Django e contém os campos adicionais necessários. Criamos um serializer para o modelo de perfil de usuário e um viewset para permitir a criação, atualização e exclusão de perfis de usuário. Além disso, criamos rotas para as views de registro, login e logout de usuários. Por fim, testamos a API usando um cliente HTTP e verificamos se a API está funcionando corretamente.



## Referências

- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Django](https://www.djangoproject.com/)
- [Postman](https://www.postman.com/)
- [Insomnia](https://insomnia.rest/)
- [Django Models](https://docs.djangoproject.com/en/3.2/topics/db/models/)
- [Django Serializers](https://www.django-rest-framework.org/api-guide/serializers/)
- [Django Views](https://docs.djangoproject.com/en/3.2/topics/http/views/)
- [Django Authentication](https://docs.djangoproject.com/en/3.2/topics/auth/)
- [Django Tokens](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
  