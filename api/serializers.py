from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError

from api.models import Project, Section, Item


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
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    sections = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'sections')
        model = Project

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        project = Project.objects.create(**validated_data)
        return project

    def get_sections(self, instance):
        sections = instance.sections.all()
        return SectionSerializer(many=True).to_representation(sections)


class SectionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    project_id = serializers.PrimaryKeyRelatedField(source='project',
                                                    required=True,
                                                    queryset=Project.objects.all())

    items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'project_id', 'items')
        model = Section

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(SectionSerializer, self).create(validated_data)

    def get_items(self, instance):
        items = instance.items.all()
        return ItemSerializer(many=True).to_representation(items)


class ItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    section_id = serializers.PrimaryKeyRelatedField(source='section',
                                                    required=True,
                                                    queryset=Section.objects.all())

    class Meta:
        fields = ('id', 'name', 'section_id')
        model = Item

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super(ItemSerializer, self).create(validated_data)
