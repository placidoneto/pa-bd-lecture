
from django.contrib import admin # type: ignore
from django.urls import path, re_path, include # type: ignore
from rest_framework.routers import DefaultRouter # type: ignore
from api import views # type: ignore
from drf_yasg.views import get_schema_view # type: ignore
from drf_yasg import openapi # type: ignore
from rest_framework import permissions # type: ignore
from api.views import * # type: ignore



router = DefaultRouter()
router.register(r'alunos', views.AlunoViewSet)
router.register(r'disciplinas', views.DisciplinaViewSet)
#router.register(r'meuusiario', views.MeuUsuarioViewSet)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

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

    #re_path('login', views.MeuUsuarioViewSet.login),
    #re_path('signup', views.MeuUsuarioViewSet.signup),
    #re_path('test_token', views.MeuUsuarioViewSet.test_token),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    #Autenticação JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),


    path('api/auth/registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('api/auth/login/', LoginUsuarioView.as_view(), name='login'),
    path('api/auth/logout/', LogoutUsuarioView.as_view(), name='logout'),


    path('api/auth/registro/aluno/', AlunoRegistrationView.as_view(), name='registro-aluno'),
    path('api/auth/login/aluno/', AlunoLoginView.as_view(), name='login-aluno'),

    path('api/auth/registro/professor/', ProfessorRegistrationView.as_view(), name='registro-professor'),
    path('api/auth/login/professor/', ProfessorLoginView.as_view(), name='login-professor'),

    path('api/auth/registro/coordenador/', CoordenadorRegistrationView.as_view(), name='registro-coordenador'),


]
