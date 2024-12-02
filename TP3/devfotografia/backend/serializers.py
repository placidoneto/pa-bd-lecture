from rest_framework import serializers
from .models import Cliente, Endereco, Servico, TipoServico, Fotografo, Usuario, Parentesco 

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

class FotografoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotografo
        fields = '__all__'

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class ParentescoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parentesco
        fields = '__all__'

