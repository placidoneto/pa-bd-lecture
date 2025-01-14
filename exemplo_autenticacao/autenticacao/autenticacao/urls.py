"""
URL configuration for autenticacao project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import path, re_path, include # type: ignore
from rest_framework.routers import DefaultRouter # type: ignore
from api import views # type: ignore
from drf_yasg.views import get_schema_view # type: ignore
from drf_yasg import openapi # type: ignore
from rest_framework import permissions # type: ignore


router = DefaultRouter()
router.register(r'meuusiario', views.MeuUsuarioViewSet)


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


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(router.urls)),

    re_path('login', views.MeuUsuarioViewSet.login),
    re_path('signup', views.MeuUsuarioViewSet.signup),
    re_path('test_token', views.MeuUsuarioViewSet.test_token),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
