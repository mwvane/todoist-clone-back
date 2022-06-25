from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets

from api.models import Project, Section, Task
from api.serializers import UserRegistrationSerializer, ProjectSerializer, SectionSerializer, TaskSerializer


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


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
