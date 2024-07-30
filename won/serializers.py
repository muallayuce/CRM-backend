from rest_framework import serializers
from .models import Won, Lead

class WonSerializer(serializers.ModelSerializer):
    lead = serializers.PrimaryKeyRelatedField(queryset=Lead.objects.all())
    class Meta:
        model = Won
        fields = ['id', 'lead', 'created_at', 'contract', 'review', 'delivery_plan', 'notes', 'deal_value']