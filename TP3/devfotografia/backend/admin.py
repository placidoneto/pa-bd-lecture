from django.contrib import admin
from .models import Cliente, Endereco, Servico, TipoServico

admin.site.register(Cliente)
admin.site.register(Endereco)
admin.site.register(TipoServico)
admin.site.register(Servico)

# Register your models here.
