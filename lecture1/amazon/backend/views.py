from django.shortcuts import render
from rest_framework import viewsets
from .models import Cliente, Endereco, Item, FormaPagamento, Vendedor, Pedido
from .serializers import ClienteSerializer, EnderecoSerializer, ItemSerializer, FormaPagamentoSerializer, VendedorSerializer, PedidoSerializer

class ClienteViewSet(viewsets.ModelViewSet):
    
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    
class EnderecoViewSet(viewsets.ModelViewSet):
    
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer
    
class ItemViewSet(viewsets.ModelViewSet):        
        queryset = Item.objects.all()
        serializer_class = ItemSerializer
        
class FormaPagamentoViewSet(viewsets.ModelViewSet):
    
    queryset = FormaPagamento.objects.all()
    serializer_class = FormaPagamentoSerializer
    
class VendedorViewSet(viewsets.ModelViewSet):    
    queryset = Vendedor.objects.all()
    serializer_class = VendedorSerializer
    
class PedidoViewSet(viewsets.ModelViewSet):
    
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    


    

