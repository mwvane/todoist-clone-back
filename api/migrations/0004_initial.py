# Generated by Django 4.0.5 on 2022-06-25 16:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0003_delete_usertoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('project', models.ForeignKey(db_column='project_id', on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='api.project')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('section', models.ForeignKey(db_column='section_id', on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api.section')),
                ('user', models.ForeignKey(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
