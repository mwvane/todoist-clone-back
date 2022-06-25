from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from api.models import Project, Section, Task


class UserRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=True, max_length=150)
    last_name = serializers.CharField(required=True, max_length=150)
    username = serializers.CharField(required=True, max_length=150)
    email = serializers.EmailField(required=True, max_length=150)
    password = serializers.CharField(required=True, max_length=150)

    class Meta:
        model = User

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        existing_user = User.objects.filter(Q(username=username) | Q(email=email)).first()
        if existing_user is not None:
            error = {}
            if existing_user.username == username:
                raise ValidationError({'non_field_errors': {'username': 'Such username already exists'}})
            else:
                raise ValidationError({'non_field_errors': {'email': 'Such email already exists'}})
        # hash password
        user = User(**validated_data)
        user.save()
        token = Token.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        pass


class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)

    class Meta:
        fields = ('name',)
        model = Project

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        project = Project.objects.create(**validated_data)
        return project


class SectionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    project = ProjectSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(source='project',
                                                    required=True,
                                                    queryset=Project.objects.all())

    class Meta:
        fields = ('name', 'project_id', 'project')
        model = Section

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(SectionSerializer, self).create(validated_data)


class TaskSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    section = SectionSerializer(read_only=True)
    section_id = serializers.PrimaryKeyRelatedField(source='section',
                                                    required=True,
                                                    queryset=Section.objects.all())

    class Meta:
        fields = ('name', 'section_id', 'section')
        model = Task

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(TaskSerializer, self).create(validated_data)
