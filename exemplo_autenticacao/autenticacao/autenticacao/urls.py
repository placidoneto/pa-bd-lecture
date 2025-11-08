
from django.contrib import admin # type: ignore
from django.urls import path, re_path, include # type: ignore
from rest_framework.routers import DefaultRouter # type: ignore
from api import views # type: ignore
from drf_yasg.views import get_schema_view # type: ignore
from drf_yasg import openapi # type: ignore
from rest_framework import permissions # type: ignore
from api.views import RegistroUsuarioView, LoginUsuarioView, LogoutUsuarioView

router = DefaultRouter()

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

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    path('api/auth/registro/', RegistroUsuarioView.as_view(), name='registro'),
    path('api/auth/login/', LoginUsuarioView.as_view(), name='login'),
    path('api/auth/logout/', LogoutUsuarioView.as_view(), name='logout'),

]
