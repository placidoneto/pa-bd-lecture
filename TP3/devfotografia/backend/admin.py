from django.contrib import admin
from .models import Cliente, Endereco, Servico, TipoServico, Fotografo, Usuario

admin.site.register(Cliente)
admin.site.register(Endereco)
admin.site.register(TipoServico)
admin.site.register(Servico)
admin.site.register(Fotografo)
admin.site.register(Usuario)


# Register your models here.
