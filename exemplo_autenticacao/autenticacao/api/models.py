from django.db import models # type: ignore
from django.contrib.auth.models import AbstractUser # type: ignore
from django.conf import settings # type: ignore
from rest_framework.authtoken.models import Token # type: ignore


class Usuario(AbstractUser):
    PERFIL = (
        ('admin', 'Administrador'),
        ('professor', 'Professor'),
        ('aluno', 'Aluno'),
        ('coordenador', 'Coordenador'),
        ('diretor', 'Diretor'),
    )

    perfil = models.CharField(max_length=15, choices=PERFIL)

class MeuUsuario(models.Model):
    cpf = models.CharField(max_length=11)

    def __str__(self):
        return self.username, self.email, self.first_name, self.last_name, self.cpf   