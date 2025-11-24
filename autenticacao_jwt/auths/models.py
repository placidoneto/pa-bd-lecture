from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
   
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class Perfil(models.Model):
    
    TIPO_PERFIL_CHOICES = [
        ('GERENTE', 'Gerente'),
        ('CLIENTE', 'Cliente'),
        ('MECANICO', 'Mecânico'),
    ]
    
    usuario = models.OneToOneField(
        Usuario, 
        on_delete=models.CASCADE, 
        related_name='perfil'
    )
    tipo = models.CharField(
        max_length=20, 
        choices=TIPO_PERFIL_CHOICES
    )
    telefone = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.get_tipo_display()}"
