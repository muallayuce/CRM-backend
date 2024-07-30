from rest_framework import serializers
from .models import Meeting, Lead

class MeetingSerializer(serializers.ModelSerializer):
    lead = serializers.PrimaryKeyRelatedField(queryset=Lead.objects.all())
    class Meta:
        model = Meeting
        fields = ['id', 'lead', 'date_time', 'location', 'participants', 'notes', 'estimated_value']