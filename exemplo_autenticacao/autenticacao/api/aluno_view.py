from django.shortcuts import render # type: ignore

from .models import MeuUsuario, User, Aluno
from .serializers import MeuUsuarioSerializer, UserSerializer, AlunoSerializer
from rest_framework.authtoken.models import Token # type: ignore
from rest_framework import viewsets # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status  # type: ignore
from django.contrib.auth import authenticate, login # type: ignore
from rest_framework.decorators import api_view # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token


class AlunoRegistrationView(APIView):
    def post(self, request):
        serializer = AlunoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AlunoViewSet(APIView):

    @api_view(['POST'])
    def registro(self, request):
        serializer = AlunoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['POST'])
    def login(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            if created:
                token.delete()  # Delete the token if it was already created
                token = Token.objects.create(user=user)

            response_data = {
                'token': token.key,
                'username': user.username,
                'perfil': user.perfil,
            }

            if user.perfil == 'aluno':
                aluno = user.conta_aluno
                if aluno is not None:
                    # Add student data to the response data
                    aluno_data = AlunoSerializer(aluno).data
                    response_data['data'] = aluno_data

            return Response(response_data)
        else:
            return Response({'message': 'Inválido Login ou Senha'}, status=status.HTTP_401_UNAUTHORIZED)
