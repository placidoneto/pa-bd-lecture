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
    nome = models.CharField(max_length=100, blank=True, null=True,)
    matricula = models.CharField(max_length=10, unique=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='aluno')    


class Professor(models.Model):    
    matricula = models.CharField(max_length=10, unique=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='professor')  

    
class Coordenador(models.Model):    
    funcao = models.CharField(max_length=30, unique=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='coordenador')      
    
class MeuUsuario(models.Model):
    cpf = models.CharField(max_length=11)
    def __str__(self):
        return self.username, self.email, self.first_name, self.last_name, self.cpf   
    

class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    carga_horaria = models.IntegerField()
    professor = models.ForeignKey(Professor, blank=True, null=True, on_delete=models.CASCADE, related_name='disciplinas')
    alunos = models.ManyToManyField(Aluno, blank=True, null=True, related_name='disciplinas')
    
    def __str__(self):
        return self.nome