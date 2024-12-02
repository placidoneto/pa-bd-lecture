from django.shortcuts import render
from rest_framework import viewsets
from .models import Cliente, Endereco, Servico, TipoServico, Fotografo, Usuario, Parentesco
from .serializers import ClienteSerializer, EnderecoSerializer, ServicoSerializer, TipoServicoSerializer, FotografoSerializer, UsuarioSerializer, ParentescoSerializer
from rest_framework.decorators import api_view, action
from rest_framework.response import Response 

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer 

    @action(detail=True, methods=['get'])
    def total_servicos(self, request, pk=None):
        cliente = self.get_object()
        servicos_count = Servico.objects.filter(cliente=cliente).count()
        return Response({'total_serviços': servicos_count})

class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer

class ServicoViewSet(viewsets.ModelViewSet):
    queryset = Servico.objects.all()
    serializer_class = ServicoSerializer

class TipoServicoViewSet(viewsets.ModelViewSet):
    queryset = TipoServico.objects.all()
    serializer_class = TipoServicoSerializer

class FotografoViewSet(viewsets.ModelViewSet):
    queryset = Fotografo.objects.all()
    serializer_class = FotografoSerializer

    @api_view(['GET'])
    def hello(request):
        return Response({'message': 'Hello, World!'})


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer

class ParentescoViewSet(viewsets.ModelViewSet):
    queryset = Parentesco.objects.all()
    serializer_class = ParentescoSerializer



