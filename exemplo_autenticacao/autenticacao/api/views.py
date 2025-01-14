from django.shortcuts import render # type: ignore

from .models import MeuUsuario
from .serializers import MeuUsuarioSerializer
from rest_framework import viewsets # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status  # type: ignore
from django.contrib.auth import authenticate, login # type: ignore
from rest_framework.decorators import api_view # type: ignore
from rest_framework.authentication import BasicAuthentication # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore

from django.contrib.auth.models import User # type: ignore
from rest_framework.authtoken.models import Token # type: ignore

## Permissions
from rest_framework.decorators import authentication_classes, permission_classes # type: ignore
from rest_framework.permissions import IsAuthenticated  # type: ignore
from rest_framework.authentication import TokenAuthentication, SessionAuthentication # type: ignore
from django.shortcuts import get_object_or_404 # type: ignore

class MeuUsuarioViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = MeuUsuarioSerializer


    @api_view(['POST'])
    def login(request):
        user = get_object_or_404(User, username=request.data['username'])
        if not user.check_password(request.data['password']):
            return Response({'message': 'Not Found!'}, status=status.HTTP_400_BAD_REQUEST)
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = MeuUsuarioSerializer(instance=user)
        return Response({'token': token.key, 'user':serializer.data})

    @api_view(['POST'])
    def signup(request):
        serializer = MeuUsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user':serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @api_view(['GET'])
    @authentication_classes([TokenAuthentication, SessionAuthentication])
    @permission_classes([IsAuthenticated])
    def test_token(request):
        return Response("passou para {}".format(request.user.email))

