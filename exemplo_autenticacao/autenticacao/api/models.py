from django.db import models # type: ignore
from django.contrib.auth.models import User, AbstractUser # type: ignore

class MeuUsuario(models.Model):
    cpf = models.CharField(max_length=11)

    def __str__(self):
        return self.username, self.email, self.first_name, self.last_name, self.cpf   