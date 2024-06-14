# Generated by Django 4.2.1 on 2023-11-02 11:42

from django.db import migrations, models
import uuid


def create_initial_google_auth(apps, schema_editor):
    GoogleAuth = apps.get_model('common', 'GoogleAuth')
    if not GoogleAuth.objects.exists():
        GoogleAuth.objects.create(is_google_auth=False)

class Migration(migrations.Migration):

    dependencies = [
        ('common', '0009_user_is_staff'),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleAuth',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Last Modified At')),
                ('is_google_auth', models.BooleanField(default=False)),
                ('created_by_id', models.UUIDField(null=True,default=uuid.uuid4, verbose_name='Created By')),
                ('updated_by_id', models.UUIDField(null=True,default=uuid.uuid4, verbose_name='Last Modified By')),
            ],
            options={
                'verbose_name': 'GoogleAuth',
                'verbose_name_plural': 'GoogleAuth',
                'db_table': 'google_auth',
            },
        ),
        migrations.RunPython(create_initial_google_auth),
    ]