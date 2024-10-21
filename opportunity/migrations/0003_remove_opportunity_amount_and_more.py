# Generated by Django 5.0.7 on 2024-07-29 15:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leads', '0004_alter_lead_status'),
        ('opportunity', '0002_alter_opportunity_created_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opportunity',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='assigned_to',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='closed_by',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='closed_on',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='contacts',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='lead_source',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='name',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='org',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='probability',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='stage',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='opportunity',
            name='teams',
        ),
        migrations.AddField(
            model_name='opportunity',
            name='lead',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='opportunities', to='leads.lead'),
        ),
    ]