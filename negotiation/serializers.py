from rest_framework import serializers
from .models import Negotiation, Lead

class NegotiationSerializer(serializers.ModelSerializer):
    lead = serializers.PrimaryKeyRelatedField(queryset=Lead.objects.all())
    class Meta:
        model = Negotiation
        fields = ['id', 'lead', 'created_at', 'negotiation_details', 'notes', 'new_value']