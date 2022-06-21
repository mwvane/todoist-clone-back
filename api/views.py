from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from api.serializers import UserRegistrationSerializer


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = User.objects.filter(username=username, password=password).first()
    if not user:
        raise ValidationError({'non_field_errors': {'username': 'no such user'}})
    token_model = user.auth_token
    return Response(token_model.key)


@api_view(['POST'])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(False)


@api_view(['GET'])
def test(request):
    from pprint import pprint
    print('')
    print('PPRINT')
    print('')
    print('')
    print('')
    pprint(request.user)
    print('')
    print('')
    print('')
    return Response()