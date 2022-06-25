from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=150)
    user = models.ForeignKey(User, related_name='projects', db_column='user_id', on_delete=models.CASCADE)


class Section(models.Model):
    name = models.CharField(max_length=150)
    project = models.ForeignKey(Project, related_name='sections', db_column='project_id', on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)


class Task(models.Model):
    name = models.CharField(max_length=512)
    section = models.ForeignKey(Section, related_name='items', db_column='section_id', on_delete=models.CASCADE)
    user = models.ForeignKey(User, db_column='user_id', on_delete=models.CASCADE)