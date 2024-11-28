from rest_framework import serializers
from .models import Cliente, Endereco, Servico, TipoServico

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__' 

class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = '__all__'

class TipoServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServico
        fields = '__all__'

        