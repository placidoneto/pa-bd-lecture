# Aula de Revisão: Sistema de Carona Compartilhada

## Django Rest Framework + CLI Python

---

## Objetivos da Aula de Revisão

- Revisar conceitos de Django Rest Framework
- Implementar modelos relacionados
- Criar serializers e viewsets
- Construir um CLI em Python para interagir com a API
- Praticar operações CRUD

---

## Estrutura do Projeto

```
carona_compartilhada/
├── backend/
│   ├── manage.py
│   ├── config/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   └── core/
│       ├── models.py
│       ├── serializers.py
│       ├── views.py
│       └── urls.py
└── cli/
    └── carona_cli.py
```

---

## PASSO 1: Configuração Inicial do Projeto

### 1.1 - Criar ambiente virtual e instalar dependências

```bash
# Criar diretório do projeto
mkdir carona_compartilhada
cd carona_compartilhada

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar dependências
pip install django djangorestframework pillow requests
```

### 1.2 - Criar projeto Django

```bash
django-admin startproject config .
python manage.py startapp core
```

### 1.3 - Configurar settings.py

```python
# config/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'core',
]

# Configuração do DRF
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

# Configuração de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

---

## PASSO 2: Criar os Modelos

### 2.1 - Definir modelos em core/models.py

```python
# core/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class Usuario(AbstractUser):
    
    TIPO_CHOICES = [
        ('MOTORISTA', 'Motorista'),
        ('PASSAGEIRO', 'Passageiro'),
        ('AMBOS', 'Ambos'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='PASSAGEIRO')
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return f"{self.username} ({self.get_tipo_display()})"


class PerfilUsuario(models.Model):
    
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='perfil')
    telefone = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='perfis/', blank=True, null=True)
    biografia = models.TextField(blank=True)
    verificado = models.BooleanField(default=False)
    nota_media = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
   
    def __str__(self):
        return f"Perfil de {self.usuario.username}"


class Veiculo(models.Model):
    
    motorista = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='veiculos',
        limit_choices_to={'tipo__in': ['MOTORISTA', 'AMBOS']}
    )
    modelo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    cor = models.CharField(max_length=50)
    ano = models.IntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    placa = models.CharField(max_length=10, unique=True)
    num_lugares = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(8)])
    ativo = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.placa}"


class Carona(models.Model):
    
    STATUS_CHOICES = [
        ('DISPONIVEL', 'Disponível'),
        ('CHEIA', 'Cheia'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    motorista = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='caronas_oferecidas'
    )
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='caronas')
    origem = models.CharField(max_length=255)
    destino = models.CharField(max_length=255)
    data_hora_saida = models.DateTimeField()
    vagas_disponiveis = models.IntegerField(validators=[MinValueValidator(0)])
    preco_por_pessoa = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DISPONIVEL')
    criado_em = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"{self.origem} → {self.destino} - {self.data_hora_saida.strftime('%d/%m/%Y %H:%M')}"


class Solicitacao(models.Model):
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('ACEITA', 'Aceita'),
        ('RECUSADA', 'Recusada'),
        ('CANCELADA', 'Cancelada'),
    ]
    
    carona = models.ForeignKey(Carona, on_delete=models.CASCADE, related_name='solicitacoes')
    passageiro = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='solicitacoes_carona'
    )
    num_lugares = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    data_solicitacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Solicitação de {self.passageiro.username} - {self.get_status_display()}"


class Avaliacao(models.Model):
    
    TIPO_CHOICES = [
        ('MOTORISTA', 'Como Motorista'),
        ('PASSAGEIRO', 'Como Passageiro'),
    ]
    
    carona = models.ForeignKey(Carona, on_delete=models.CASCADE, related_name='avaliacoes')
    avaliador = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='avaliacoes_feitas'
    )
    avaliado = models.ForeignKey(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='avaliacoes_recebidas'
    )
    nota = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comentario = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.avaliador.username} avaliou {self.avaliado.username} - Nota: {self.nota}"


class Chat(models.Model):
    carona = models.ForeignKey(Carona, on_delete=models.CASCADE, related_name='mensagens')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='mensagens')
    mensagem = models.TextField()
    data_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username}: {self.mensagem[:50]}"
```

### 2.2 - Configurar modelo customizado em settings.py

```python
# config/settings.py
AUTH_USER_MODEL = 'core.Usuario'
```

### 2.3 - Criar e aplicar migrações

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

---

## PASSO 3: Criar Serializers

### 3.1 - Definir serializers em core/serializers.py

```python
# core/serializers.py

from rest_framework import serializers
from .models import Usuario, PerfilUsuario, Veiculo, Carona, Solicitacao, Avaliacao, Chat

class PerfilUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilUsuario
        fields = ['telefone', 'foto', 'biografia', 'verificado', 'nota_media']


class UsuarioSerializer(serializers.ModelSerializer):
    perfil = PerfilUsuarioSerializer(read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'tipo', 'perfil']
        read_only_fields = ['id']


class VeiculoSerializer(serializers.ModelSerializer):
    motorista_nome = serializers.CharField(source='motorista.username', read_only=True)
    
    class Meta:
        model = Veiculo
        fields = [
            'id', 'motorista', 'motorista_nome', 'modelo', 'marca', 
            'cor', 'ano', 'placa', 'num_lugares', 'ativo'
        ]
        read_only_fields = ['id']


class CaronaSerializer(serializers.ModelSerializer):
    motorista_nome = serializers.CharField(source='motorista.username', read_only=True)
    veiculo_info = serializers.CharField(source='veiculo.__str__', read_only=True)
    
    class Meta:
        model = Carona
        fields = [
            'id', 'motorista', 'motorista_nome', 'veiculo', 'veiculo_info',
            'origem', 'destino', 'data_hora_saida', 'vagas_disponiveis',
            'preco_por_pessoa', 'observacoes', 'status', 'criado_em'
        ]
        read_only_fields = ['id', 'criado_em']


class SolicitacaoSerializer(serializers.ModelSerializer):
    passageiro_nome = serializers.CharField(source='passageiro.username', read_only=True)
    carona_info = serializers.CharField(source='carona.__str__', read_only=True)
    
    class Meta:
        model = Solicitacao
        fields = [
            'id', 'carona', 'carona_info', 'passageiro', 'passageiro_nome',
            'num_lugares', 'status', 'data_solicitacao'
        ]
        read_only_fields = ['id', 'data_solicitacao']


class AvaliacaoSerializer(serializers.ModelSerializer):
    avaliador_nome = serializers.CharField(source='avaliador.username', read_only=True)
    avaliado_nome = serializers.CharField(source='avaliado.username', read_only=True)
    
    class Meta:
        model = Avaliacao
        fields = [
            'id', 'carona', 'avaliador', 'avaliador_nome', 
            'avaliado', 'avaliado_nome', 'nota', 'comentario', 
            'tipo', 'criado_em'
        ]
        read_only_fields = ['id', 'criado_em']


class ChatSerializer(serializers.ModelSerializer):
    usuario_nome = serializers.CharField(source='usuario.username', read_only=True)
    
    class Meta:
        model = Chat
        fields = ['id', 'carona', 'usuario', 'usuario_nome', 'mensagem', 'data_hora']
        read_only_fields = ['id', 'data_hora']
```

---

## PASSO 4: Criar Views e ViewSets

### 4.1 - Definir viewsets em core/views.py

```python
# core/views.py

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Usuario, PerfilUsuario, Veiculo, Carona, Solicitacao, Avaliacao, Chat
from .serializers import (
    UsuarioSerializer, PerfilUsuarioSerializer, VeiculoSerializer,
    CaronaSerializer, SolicitacaoSerializer, AvaliacaoSerializer, ChatSerializer
)

class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']


class PerfilUsuarioViewSet(viewsets.ModelViewSet):
    queryset = PerfilUsuario.objects.all()
    serializer_class = PerfilUsuarioSerializer


class VeiculoViewSet(viewsets.ModelViewSet):
    queryset = Veiculo.objects.all()
    serializer_class = VeiculoSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['motorista', 'ativo']
    search_fields = ['modelo', 'marca', 'placa']


class CaronaViewSet(viewsets.ModelViewSet):
    queryset = Carona.objects.all()
    serializer_class = CaronaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['motorista', 'status', 'origem', 'destino']
    search_fields = ['origem', 'destino']
    ordering_fields = ['data_hora_saida', 'preco_por_pessoa']
    
    @action(detail=False, methods=['get'])
    def disponiveis(self, request):
        """Retorna apenas caronas disponíveis"""
        caronas = self.queryset.filter(status='DISPONIVEL', vagas_disponiveis__gt=0)
        serializer = self.get_serializer(caronas, many=True)
        return Response(serializer.data)


class SolicitacaoViewSet(viewsets.ModelViewSet):
    queryset = Solicitacao.objects.all()
    serializer_class = SolicitacaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['carona', 'passageiro', 'status']
    
    @action(detail=True, methods=['post'])
    def aceitar(self, request, pk=None):
        """Aceitar uma solicitação"""
        solicitacao = self.get_object()
        solicitacao.status = 'ACEITA'
        solicitacao.save()
        return Response({'status': 'Solicitação aceita'})
    
    @action(detail=True, methods=['post'])
    def recusar(self, request, pk=None):
        """Recusar uma solicitação"""
        solicitacao = self.get_object()
        solicitacao.status = 'RECUSADA'
        solicitacao.save()
        return Response({'status': 'Solicitação recusada'})


class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['carona', 'avaliador', 'avaliado', 'tipo']


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['carona', 'usuario']
```

---

## PASSO 5: Configurar URLs

### 5.1 - Criar core/urls.py

```python
# core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UsuarioViewSet, PerfilUsuarioViewSet, VeiculoViewSet,
    CaronaViewSet, SolicitacaoViewSet, AvaliacaoViewSet, ChatViewSet
)

router = DefaultRouter()
router.register(r'usuarios', UsuarioViewSet, basename='usuario')
router.register(r'perfis', PerfilUsuarioViewSet, basename='perfil')
router.register(r'veiculos', VeiculoViewSet, basename='veiculo')
router.register(r'caronas', CaronaViewSet, basename='carona')
router.register(r'solicitacoes', SolicitacaoViewSet, basename='solicitacao')
router.register(r'avaliacoes', AvaliacaoViewSet, basename='avaliacao')
router.register(r'chats', ChatViewSet, basename='chat')

urlpatterns = [
    path('', include(router.urls)),
]
```

### 5.2 - Configurar config/urls.py

```python
# config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## PASSO 6: Testar a API

```bash
# Executar servidor
python manage.py runserver

# Acessar no navegador:
# http://localhost:8000/api/
# http://localhost:8000/api/caronas/
# http://localhost:8000/api/usuarios/
```

---

## PASSO 7: Criar CLI em Python

### 7.1 - Criar arquivo cli/carona_cli.py

```python
#!/usr/bin/env python3
# cli/carona_cli.py

import requests
import json
from datetime import datetime
from typing import Optional, Dict, List

class CaronaCLI:
    """CLI para interagir com a API de Carona Compartilhada"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """Faz requisição HTTP para a API"""
        url = f"{self.base_url}/{endpoint}"
        try:
            if method == "GET":
                response = self.session.get(url)
            elif method == "POST":
                response = self.session.post(url, json=data)
            elif method == "PUT":
                response = self.session.put(url, json=data)
            elif method == "DELETE":
                response = self.session.delete(url)
            
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição: {e}")
            return {}
    
    def listar_caronas(self):
        """Lista todas as caronas disponíveis"""
        print("\nCARONAS DISPONÍVEIS")
        print("=" * 80)
        
        caronas = self._make_request("GET", "caronas/disponiveis/")
        
        if not caronas:
            print("Nenhuma carona disponível no momento.")
            return
        
        for carona in caronas:
            print(f"\nID: {carona['id']}")
            print(f"   Origem: {carona['origem']} → Destino: {carona['destino']}")
            print(f"   Motorista: {carona['motorista_nome']}")
            print(f"   Data/Hora: {carona['data_hora_saida']}")
            print(f"   Vagas: {carona['vagas_disponiveis']}")
            print(f"   Preço: R$ {carona['preco_por_pessoa']}")
            if carona['observacoes']:
                print(f"   Obs: {carona['observacoes']}")
    
    def criar_carona(self):
        """Cria uma nova carona"""
        print("\nCRIAR NOVA CARONA")
        print("=" * 80)
        
        try:
            motorista_id = int(input("ID do motorista: "))
            veiculo_id = int(input("ID do veículo: "))
            origem = input("Origem: ")
            destino = input("Destino: ")
            data_hora = input("Data/Hora de saída (YYYY-MM-DD HH:MM): ")
            vagas = int(input("Vagas disponíveis: "))
            preco = float(input("Preço por pessoa: "))
            observacoes = input("Observações (opcional): ")
            
            data = {
                "motorista": motorista_id,
                "veiculo": veiculo_id,
                "origem": origem,
                "destino": destino,
                "data_hora_saida": data_hora,
                "vagas_disponiveis": vagas,
                "preco_por_pessoa": preco,
                "observacoes": observacoes,
                "status": "DISPONIVEL"
            }
            
            resultado = self._make_request("POST", "caronas/", data)
            
            if resultado:
                print(f"\nCarona criada com sucesso! ID: {resultado.get('id')}")
            else:
                print("\nErro ao criar carona.")
                
        except ValueError:
            print("Erro: Valores inválidos inseridos.")
    
    def solicitar_carona(self):
        """Solicita participação em uma carona"""
        print("\nSOLICITAR CARONA")
        print("=" * 80)
        
        try:
            carona_id = int(input("ID da carona: "))
            passageiro_id = int(input("ID do passageiro: "))
            num_lugares = int(input("Número de lugares solicitados: "))
            
            data = {
                "carona": carona_id,
                "passageiro": passageiro_id,
                "num_lugares": num_lugares,
                "status": "PENDENTE"
            }
            
            resultado = self._make_request("POST", "solicitacoes/", data)
            
            if resultado:
                print(f"\nSolicitação enviada com sucesso! ID: {resultado.get('id')}")
            else:
                print("\nErro ao solicitar carona.")
                
        except ValueError:
            print("Erro: Valores inválidos inseridos.")
    
    def listar_solicitacoes(self):
        """Lista todas as solicitações"""
        print("\nSOLICITAÇÕES")
        print("=" * 80)
        
        solicitacoes = self._make_request("GET", "solicitacoes/")
        
        if not solicitacoes.get('results'):
            print("Nenhuma solicitação encontrada.")
            return
        
        for sol in solicitacoes['results']:
            print(f"\n🎫 ID: {sol['id']}")
            print(f"   Carona: {sol['carona_info']}")
            print(f"   Passageiro: {sol['passageiro_nome']}")
            print(f"   Lugares: {sol['num_lugares']}")
            print(f"   Status: {sol['status']}")
            print(f"   Data: {sol['data_solicitacao']}")
    
    def gerenciar_solicitacao(self):
        """Aceitar ou recusar solicitação"""
        print("\nGERENCIAR SOLICITAÇÃO")
        print("=" * 80)
        
        try:
            sol_id = int(input("ID da solicitação: "))
            acao = input("Ação (aceitar/recusar): ").lower()
            
            if acao not in ['aceitar', 'recusar']:
                print("Ação inválida!")
                return
            
            resultado = self._make_request("POST", f"solicitacoes/{sol_id}/{acao}/")
            
            if resultado:
                print(f"\nSolicitação {acao}a com sucesso!")
            else:
                print(f"\n Erro ao {acao} solicitação.")
                
        except ValueError:
            print("Erro: Valores inválidos inseridos.")
    
    def criar_veiculo(self):
        """Cadastra um novo veículo"""
        print("\nCADASTRAR VEÍCULO")
        print("=" * 80)
        
        try:
            motorista_id = int(input("ID do motorista: "))
            modelo = input("Modelo: ")
            marca = input("Marca: ")
            cor = input("Cor: ")
            ano = int(input("Ano: "))
            placa = input("Placa: ")
            num_lugares = int(input("Número de lugares: "))
            
            data = {
                "motorista": motorista_id,
                "modelo": modelo,
                "marca": marca,
                "cor": cor,
                "ano": ano,
                "placa": placa,
                "num_lugares": num_lugares,
                "ativo": True
            }
            
            resultado = self._make_request("POST", "veiculos/", data)
            
            if resultado:
                print(f"\nVeículo cadastrado com sucesso! ID: {resultado.get('id')}")
            else:
                print("\n Erro ao cadastrar veículo.")
                
        except ValueError:
            print(" Erro: Valores inválidos inseridos.")
    
    def menu_principal(self):
        """Menu principal do CLI"""
        while True:
            print("\n" + "=" * 80)
            print("SISTEMA DE CARONA COMPARTILHADA - CLI")
            print("=" * 80)
            print("1. Listar caronas disponíveis")
            print("2. Criar nova carona")
            print("3. Solicitar carona")
            print("4. Listar solicitações")
            print("5. Gerenciar solicitação (aceitar/recusar)")
            print("6. Cadastrar veículo")
            print("0. Sair")
            print("=" * 80)
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.listar_caronas()
            elif opcao == "2":
                self.criar_carona()
            elif opcao == "3":
                self.solicitar_carona()
            elif opcao == "4":
                self.listar_solicitacoes()
            elif opcao == "5":
                self.gerenciar_solicitacao()
            elif opcao == "6":
                self.criar_veiculo()
            elif opcao == "0":
                print("\n FIM!")
                break
            else:
                print("\n Opção inválida!")
            
            input("\nPressione ENTER para continuar...")


def main():
    """Função principal"""
    cli = CaronaCLI()
    cli.menu_principal()


if __name__ == "__main__":
    main()
```

### 7.2 - Tornar o CLI executável

```bash
chmod +x cli/carona_cli.py
```

### 7.3 - Executar o CLI

```bash
python cli/carona_cli.py
```

---

## PASSO 8: Registro no Admin

### 8.1 - Configurar core/admin.py

```python
# core/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, PerfilUsuario, Veiculo, Carona, Solicitacao, Avaliacao, Chat

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'tipo', 'is_staff']
    list_filter = ['tipo', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Extras', {'fields': ('tipo',)}),
    )

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'telefone', 'verificado', 'nota_media']
    list_filter = ['verificado']
    search_fields = ['usuario__username', 'telefone']

@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ['placa', 'marca', 'modelo', 'motorista', 'ativo']
    list_filter = ['ativo', 'marca']
    search_fields = ['placa', 'modelo', 'motorista__username']

@admin.register(Carona)
class CaronaAdmin(admin.ModelAdmin):
    list_display = ['origem', 'destino', 'motorista', 'data_hora_saida', 'status', 'vagas_disponiveis']
    list_filter = ['status', 'data_hora_saida']
    search_fields = ['origem', 'destino', 'motorista__username']
    date_hierarchy = 'data_hora_saida'

@admin.register(Solicitacao)
class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ['carona', 'passageiro', 'num_lugares', 'status', 'data_solicitacao']
    list_filter = ['status', 'data_solicitacao']
    search_fields = ['passageiro__username']

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ['avaliador', 'avaliado', 'nota', 'tipo', 'criado_em']
    list_filter = ['nota', 'tipo']
    search_fields = ['avaliador__username', 'avaliado__username']

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['carona', 'usuario', 'mensagem', 'data_hora']
    list_filter = ['data_hora']
    search_fields = ['usuario__username', 'mensagem']
    date_hierarchy = 'data_hora'
```

---

## Exercícios Práticos

### Exercício 1: Popular o Banco de Dados
Crie um script para popular o banco com dados de teste:
- 5 usuários (2 motoristas, 2 passageiros, 1 ambos)
- 3 veículos
- 5 caronas
- 10 solicitações

### Exercício 2: Adicionar Filtros Avançados
Implemente filtros no CLI para:
- Buscar caronas por faixa de preço
- Buscar caronas por data
- Filtrar por cidade de origem/destino

### Exercício 3: Implementar Autenticação
Adicione autenticação no projeto usando Token do AbstractUser ou User:
```bash
pip install djangorestframework-simplejwt
```

---

## Conceitos Importantes para Revisão

### 1. **Relacionamentos no Django**
- `ForeignKey`: Relação um-para-muitos (1:N)
- `OneToOneField`: Relação um-para-um (1:1)
- `ManyToManyField`: Relação muitos-para-muitos (N:N)

### 2. **Django Rest Framework**
- **Serializers**: Convertem modelos Django em JSON
- **ViewSets**: Agrupam lógica de CRUD
- **Routers**: Geram URLs automaticamente

### 3. **Status HTTP**
- `200 OK`: Sucesso
- `201 Created`: Recurso criado
- `400 Bad Request`: Dados inválidos
- `404 Not Found`: Recurso não encontrado

### 4. **Boas Práticas**
- Use `related_name` em ForeignKeys
- Valide dados nos serializers
- Use `choices` para campos com opções fixas
- Implemente métodos `__str__` nos modelos

---

## Checklist de Verificação

- [ ] Modelos criados e relacionamentos corretos
- [ ] Migrações aplicadas com sucesso
- [ ] Serializers funcionando corretamente
- [ ] ViewSets respondendo nos endpoints
- [ ] URLs configuradas corretamente
- [ ] Admin configurado e acessível
- [ ] CLI interagindo com a API

---

## Recursos Adicionais

### Documentação Oficial
- [Django Documentation](https://docs.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Python Requests Library](https://requests.readthedocs.io/)

### Comandos Úteis

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor
python manage.py runserver

```
