from rest_framework import serializers
from .models import Qualified, Lead

class QualifiedSerializer(serializers.ModelSerializer):
    lead = serializers.PrimaryKeyRelatedField(queryset=Lead.objects.all())
    class Meta:
        model = Qualified
        fields = ['id', 'lead', 'created_at', 'description_of_services', 'notes', 'offer_value']