from django.shortcuts import render # type: ignore

from .models import MeuUsuario, User
from .serializers import MeuUsuarioSerializer, UserSerializer
from rest_framework import viewsets # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status  # type: ignore
from django.contrib.auth import authenticate, login # type: ignore
from rest_framework.decorators import api_view # type: ignore
from rest_framework.authentication import BasicAuthentication # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


from django.contrib.auth.models import User # type: ignore
from rest_framework.authtoken.models import Token # type: ignore

## Permissions
from rest_framework.decorators import authentication_classes, permission_classes # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework.authentication import TokenAuthentication, SessionAuthentication # type: ignore
from django.shortcuts import get_object_or_404 # type: ignore


class RegistroUsuarioView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginUsuarioView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            token, created = Token.objects.get_or_create(user=usuario)
            if created:
                token.delete()  
                token = Token.objects.create(user=usuario)
            return Response({'token': token.key, 'username': usuario.username, 'perfil': usuario.perfil})
        else:
            return Response({'mensagem': 'Login ou Senha Inválido'}, status=status.HTTP_401_UNAUTHORIZED)



class LogoutUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(request.headers) 
        token_key = request.auth.key
        token = Token.objects.get(key=token_key)
        token.delete()

        return Response({'detail': 'Usuário deslogado com sucesso.'})









# class MeuUsuarioViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = MeuUsuarioSerializer


#     @api_view(['POST'])
#     def login(request):
#         user = get_object_or_404(User, username=request.data['username'])
#         if not user.check_password(request.data['password']):
#             return Response({'message': 'Not Found!'}, status=status.HTTP_400_BAD_REQUEST)
        
#         token, created = Token.objects.get_or_create(user=user)
#         serializer = MeuUsuarioSerializer(instance=user)
#         return Response({'token': token.key, 'user':serializer.data})

#     @api_view(['POST'])
#     def signup(request):
#         serializer = MeuUsuarioSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             user = User.objects.get(username=request.data['username'])
#             user.set_password(request.data['password'])
#             user.save()
#             token = Token.objects.create(user=user)
#             return Response({'token': token.key, 'user':serializer.data})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     @api_view(['GET'])
#     @authentication_classes([TokenAuthentication, SessionAuthentication])
#     @permission_classes([IsAuthenticated])
#     def test_token(request):
#         return Response("passou para {}".format(request.user.email))

