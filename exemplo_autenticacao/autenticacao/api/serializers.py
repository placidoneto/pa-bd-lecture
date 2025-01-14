from rest_framework import serializers #type: ignore
from django.contrib.auth.models import User #type: ignore

class MeuUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']
        