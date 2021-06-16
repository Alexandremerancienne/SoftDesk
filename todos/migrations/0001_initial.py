# Generated by Django 3.2.4 on 2021-06-16 14:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('author', 'Author'), ('contributor', 'Contributor'), ('other', 'Other')], help_text='Role (author, contributor, other)', max_length=100)),
                ('permissions', models.CharField(choices=[('allowed', 'allowed'), ('none', 'None')], help_text='Permissions (allowed, none)', max_length=100)),
            ],
            options={
                'verbose_name_plural': 'contributors',
            },
        ),
        migrations.CreateModel(
            name='Projects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('type', models.CharField(blank=True, choices=[('back', 'Back-end'), ('front', 'Front-end'), ('android', 'Android'), ('ios', 'iOS')], help_text='Type (front, back, android, ios)', max_length=50)),
                ('author_user_id', models.ManyToManyField(through='todos.Contributors', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'projects',
            },
        ),
        migrations.CreateModel(
            name='Issues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=2000)),
                ('tag', models.CharField(blank=True, choices=[('bug', 'Bug'), ('improvement', 'Improvement'), ('task', 'Task')], help_text='Tag (bug, improvement, task)', max_length=50)),
                ('priority', models.CharField(blank=True, choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], help_text='Priority (low, medium, high)', max_length=50)),
                ('status', models.CharField(blank=True, choices=[('todo', 'To Do'), ('ongoing', 'Ongoing'), ('done', 'Done')], help_text='Status (todo, ongoing, done)', max_length=50)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('assignee_user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='todos.projects')),
            ],
            options={
                'verbose_name_plural': 'issues',
            },
        ),
        migrations.AddField(
            model_name='contributors',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todos.projects'),
        ),
        migrations.AddField(
            model_name='contributors',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=2000)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('author_user_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('issue_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='todos.issues')),
            ],
            options={
                'verbose_name_plural': 'comments',
            },
        ),
    ]
