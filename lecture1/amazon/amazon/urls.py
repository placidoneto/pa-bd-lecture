from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from backend import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation with Swagger",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'clientes', views.ClienteViewSet)
router.register(r'enderecos', views.EnderecoViewSet)
router.register(r'itens', views.ItemViewSet)
router.register(r'vendedores', views.VendedorViewSet)
router.register(r'formas_pagamento', views.FormaPagamentoViewSet)
router.register(r'pedidos', views.PedidoViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('amazon_api/', include(router.urls)),
]