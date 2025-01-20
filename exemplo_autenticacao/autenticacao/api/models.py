from django.db import models # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore
from django.conf import settings # type: ignore
from rest_framework.authtoken.models import Token # type: ignore


class User(AbstractUser):
    PERFIL = (
        ('admin', 'Administrador'),
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
        ('coordenador', 'Coordenador'),
        ('diretor', 'Diretor'),
    )
    perfil = models.CharField(max_length=15, choices=PERFIL)

class Aluno(models.Model):    
    matricula = models.CharField(max_length=10, unique=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="conta_aluno")

class MeuUsuario(models.Model):
    cpf = models.CharField(max_length=11)
    def __str__(self):
        return self.username, self.email, self.first_name, self.last_name, self.cpf   