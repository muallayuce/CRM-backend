from django.apps import AppConfig


class QualifiedConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'qualified'
