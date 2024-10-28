from django.contrib import admin
from .models import Cliente, Endereco, Item, FormaPagamento, Vendedor, Pedido

admin.site.register(Cliente) 
admin.site.register(Endereco)
admin.site.register(Item)
admin.site.register(FormaPagamento)
admin.site.register(Vendedor)
admin.site.register(Pedido)
 