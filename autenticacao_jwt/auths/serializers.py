from rest_framework import serializers
from .models import Usuario, Perfil

class PerfilSerializer(serializers.ModelSerializer):
    
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    
    class Meta:
        model = Perfil
        fields = ['tipo', 'tipo_display', 'telefone']


class UsuarioSerializer(serializers.ModelSerializer):
    
    perfil = PerfilSerializer(read_only=True)
    
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'perfil']


class RegistroSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, min_length=6)
    tipo_perfil = serializers.ChoiceField(
        choices=Perfil.TIPO_PERFIL_CHOICES,
        write_only=True
    )
    telefone = serializers.CharField(required=False, allow_blank=True)
    
    class Meta:
        model = Usuario
        fields = [
            'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'tipo_perfil', 'telefone'
        ]
    
    def validate(self, data):
        """
        Validar se as senhas coincidem
        """
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': 'As senhas não coincidem.'
            })
        return data
    
    def create(self, validated_data):
        """
        Criar usuário e perfil associado
        """
        # Remover campos que não fazem parte do modelo Usuario
        validated_data.pop('password_confirm')
        tipo_perfil = validated_data.pop('tipo_perfil')
        telefone = validated_data.pop('telefone', '')
        
        # Criar usuário
        usuario = Usuario.objects.create_user(**validated_data)
        
        # Criar perfil associado
        Perfil.objects.create(
            usuario=usuario,
            tipo=tipo_perfil, 
            telefone=telefone
        )
        
        return usuario