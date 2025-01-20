from django.shortcuts import render # type: ignore

from .models import MeuUsuario, User
from .serializers import MeuUsuarioSerializer, UserSerializer, AlunoSerializer, ProfessorSerializer, CoordenadorSerializer
from rest_framework import viewsets # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status  # type: ignore
from django.contrib.auth import authenticate, login # type: ignore
from rest_framework.decorators import api_view # type: ignore
from rest_framework.authentication import BasicAuthentication # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.views import APIView # type: ignore
from rest_framework.authtoken.views import ObtainAuthToken # type: ignore
from rest_framework.authtoken.models import Token # type: ignore


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

####

class AlunoRegistrationView(APIView):
    def post(self, request):
        serializer = AlunoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlunoLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token.delete()  # Deleta o token antigo
                token = Token.objects.create(user=user)

            response_data = {
                'token': token.key,
                'username': user.username,
                'perfil': user.perfil,
            }

            if user.perfil == 'aluno':
                aluno = user.aluno  # Assumindo que a relação tem nome "aluno"
                if aluno is not None:
                    # Adiciona os dados do aluno ao response_data
                    aluno_data = AlunoSerializer(aluno).data
                    response_data['data'] = aluno_data

            return Response(response_data)
        else:
            return Response({'message': 'Usuário ou Senha Inválido'}, status=status.HTTP_401_UNAUTHORIZED)

####

class ProfessorRegistrationView(APIView):
    def post(self, request):
        serializer = ProfessorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfessorLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token.delete()  # Deleta o token antigo
                token = Token.objects.create(user=user)

            response_data = {
                'token': token.key,
                'username': user.username,
                'perfil': user.perfil,
            }

            if user.perfil == 'professor':
                professor = user.professor  # Assumindo que a relação tem nome "professor"
                if professor is not None:
                    # Adiciona os dados do professor ao response_data
                    professor_data = ProfessorSerializer(professor).data
                    response_data['data'] = professor_data

            return Response(response_data)
        else:
            return Response({'message': 'Usuário ou Senha Inválido'}, status=status.HTTP_401_UNAUTHORIZED)

####

####

class CoordenadorRegistrationView(APIView):
    def post(self, request):
        serializer = CoordenadorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

