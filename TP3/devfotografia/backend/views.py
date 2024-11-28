from django.shortcuts import render
from rest_framework import viewsets
from .models import Cliente, Endereco, Servico, TipoServico
from .serializers import ClienteSerializer, EnderecoSerializer, ServicoSerializer, TipoServicoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer 

class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer

class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer

class TipoServicoViewSet(viewsets.ModelViewSet):
    queryset = TipoServico.objects.all()
    serializer_class = TipoServicoSerializer

    
