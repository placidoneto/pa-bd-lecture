from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import registro_view, usuario_atual_view

urlpatterns = [
    # Endpoint de registro
    path('registro/', registro_view, name='registro'),
    
    # Endpoints de autenticação JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Endpoint para obter usuário atual
    path('usuario/', usuario_atual_view, name='usuario_atual'),
]