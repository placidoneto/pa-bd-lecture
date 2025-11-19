# Atividade Prática: Sistema de Autenticação e Perfis - Oficina Mecânica

## Objetivo
Desenvolver um sistema de autenticação com diferentes perfis de usuário para gerenciamento de uma oficina mecânica, implementando registro, login, logout e redirecionamento de página baseado em perfil.

- **Atividade em DUPLA**

## Competências a serem Desenvolvidas
- Implementação de autenticação simples (token) no Django REST Framework
- Criação de modelos customizados de usuário com múltiplos perfis
- Desenvolvimento de frontend React/Angular 
- Gerenciamento de estados de autenticação

## Descrição do Sistema

A **AutoTech Manager** é uma oficina mecânica que precisa de um sistema para gerenciar três tipos de usuários:

1. **Gerente**: Acesso total ao sistema, visualiza relatórios, gerencia mecânicos e clientes
2. **Mecânico**: Visualiza ordens de serviço atribuídas, atualiza status de serviços
3. **Cliente**: Visualiza seus veículos e histórico de serviços

## Parte 1: Backend (Django REST Framework)

### Estrutura do Projeto
```
oficina_backend/
├── manage.py
├── oficina/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── autenticacao/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
└── requirements.txt
```

### Requisitos Técnicos

#### 1. Modelo de Usuário Customizado
Crie um modelo `Usuario` que estenda `AbstractUser` com os seguintes campos:
- `email` (único, obrigatório)
- `cpf` (único, obrigatório)
- `telefone`
- `tipo_perfil` (choices: GERENTE, MECANICO, CLIENTE)
- `data_cadastro`
- `ativo` (boolean)

#### 2. Endpoints de Autenticação
Implemente os seguintes endpoints:

| Método | Endpoint | Descrição | Autenticação |
|--------|----------|-----------|--------------|
| POST | `/api/auth/registro/` | Cadastro de novo usuário | Não |
| POST | `/api/auth/login/` | Login com email e senha | Não |
| POST | `/api/auth/logout/` | Logout do usuário | Sim |
| GET | `/api/auth/perfil/` | Dados do usuário logado | Sim |
| PUT | `/api/auth/perfil/` | Atualizar perfil | Sim |

#### 3. Serializers Necessários
- `UsuarioRegistroSerializer`: Para cadastro (validação de CPF, senha forte)
- `LoginSerializer`: Para autenticação
- `UsuarioPerfilSerializer`: Para visualização/edição de perfil


### Tarefas Backend

- [ ] Instalar dependências: `djangorestframework`, `djangorestframework-simplejwt`, `django-cors-headers`
- [ ] Criar modelo de usuário customizado
- [ ] Implementar serializers com validações
- [ ] Criar views de autenticação
- [ ] Configurar CORS para permitir requisições do frontend
- [ ] Testar todos os endpoints antes de implementar o front

## Parte 2: Frontend (React ou Angular)

### Estrutura do Projeto (React)
```
oficina_frontend/
├── src/
│   ├── components/
│   │   ├── Login/
│   │   ├── Registro/
│   │   └── PrivateRoute/
│   ├── pages/
│   │   ├── DashboardGerente/
│   │   ├── DashboardMecanico/
│   │   └── DashboardCliente/
│   ├── services/
│   │   └── authService.js
│   ├── contexts/
│   │   └── AuthContext.js
│   └── App.js
```

### Requisitos Técnicos

#### Telas Obrigatórias

##### Tela de Login
- Campos: Email (ou username) e Senha
- Botão "Entrar"
- Link para registro
- Validação de campos
- Mensagens de erro

##### Tela de Registro
- Campos: Nome, Email, CPF, Telefone, Senha, Confirmar Senha, Tipo de Perfil
- Validações em tempo real
- Máscara para CPF e telefone
- Força da senha indicada visualmente

##### Dashboard Gerente
- Mensagem de boas-vindas com nome
- Menu com opções de gerenciamento
- Botão de logout

##### Dashboard Mecânico
- Mensagem de boas-vindas com nome
- Status dos serviços
- Botão de logout

##### Dashboard Cliente
- Mensagem de boas-vindas com nome
- Botão de logout

### Tarefas Frontend

- [ ] Configurar projeto React ou Angular
- [ ] Criar componente de rota 
- [ ] Desenvolver tela de login com validações
- [ ] Desenvolver tela de registro e validações
- [ ] Criar página SIMPLES específica por perfil
- [ ] Implementar logout com limpeza de estado


### Estrutura de Entrega
```
projeto_oficina/
├── backend/
│   ├── README.md (instruções de instalação)
│   ├── requirements.txt
│   └── [código do Django]
├── frontend/
│   ├── README.md (instruções de instalação)
│   ├── package.json
│   └── [código React/Angular]
└── DOCUMENTACAO.md (decisões técnicas, dificuldades, melhorias)
```

### Demonstração
Grave um vídeo de 3-5 minutos demonstrando:
1. Registro de um novo usuário
2. Login com cada tipo de perfil
3. Navegação nos dashboards
4. Processo de logout
5. Tentativa de acesso não autorizado

## Recursos de Apoio

- [Django REST Framework - Authentication](https://www.django-rest-framework.org/api-guide/authentication/)
- [Simple JWT Documentation](https://django-rest-framework-simplejwt.readthedocs.io/)
- [React Router - Authentication](https://reactrouter.com/en/main/start/examples#auth)
- [Angular Guards](https://angular.io/guide/router#milestone-5-route-guards)
- [JWT.io - Debugger](https://jwt.io/)
