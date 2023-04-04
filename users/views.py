from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from random import choice, randint
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserLoginValidateSerializer,  UserRegValidateSerializer, UserConfirmValidateSerializer
from django.contrib.auth.models import User
from .models import ConfirmCode

@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserLoginValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(**serializer.validated_data)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(data={'errors': 'Username or password not correct'},
                    status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def registration_api_view(request):
    serializer = UserRegValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = User.objects.create_user(**serializer.validated_data, is_active=False)

    return Response(data={'user_id': user.id},
                    status=status.HTTP_201_CREATED)

@api_view(["POST"])
def confirmation_api_view(request):
    serializer = UserConfirmValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    if ConfirmCode.objects.filter(user_ptr_id=request.data['user_id'], code=request.data['code']):
        User.objects.update(is_active=True)
        return Response(status=status.HTTP_202_ACCEPTED,
                        data={'code': 'confirmed'})

    return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                    data={'error': 'wrong id or code!'})



