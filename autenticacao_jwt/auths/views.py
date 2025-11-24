from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegistroSerializer, UsuarioSerializer

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def registro_view(request):
    """
    Endpoint para registro de novos usuários
    POST /api/registro/
    
    Body esperado:
    {
        "username": "joao",
        "email": "joao@email.com",
        "password": "senha123",
        "password_confirm": "senha123",
        "first_name": "João",
        "last_name": "Silva",
        "tipo_perfil": "CLIENTE",
        "telefone": "84999999999"
    }
    """
    serializer = RegistroSerializer(data=request.data)
    
    if serializer.is_valid():
        usuario = serializer.save()
        
        # Gerar tokens JWT
        refresh = RefreshToken.for_user(usuario)
        
        return Response({
            'message': 'Usuário registrado com sucesso!',
            'user': UsuarioSerializer(usuario).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def usuario_atual_view(request):
    """
    Endpoint para obter dados do usuário autenticado
    GET /api/usuario/
    
    Header necessário:
    Authorization: Bearer <access_token>
    """
    serializer = UsuarioSerializer(request.user)
    return Response(serializer.data)