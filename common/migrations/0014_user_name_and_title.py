# Generated by Django 5.0.6 on 2024-06-10 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_remove_user_has_marketing_access_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='First Name'),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Last Name'),
        ),
        migrations.AddField(
            model_name='user',
            name='job_title',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Job Title'),
        ),
    ]
