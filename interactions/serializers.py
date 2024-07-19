from rest_framework import serializers

from common.serializer import ProfileSerializer, UserSerializer
from contacts.serializer import ContactSerializer
from leads.serializer import LeadSerializer
from .models import Interaction

class InteractionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)
    interact_with = LeadSerializer(read_only=True)
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Interaction
        fields = ['id', 'user', 'created_at', 'updated_at', 'start_at', 'end_at', 'duration', 'type', 'interact_with', 'contact', 'description']

class InteractionCreateSerializer(serializers.ModelSerializer):
    start_at = serializers.DateTimeField(required=False, allow_null=True)
    end_at = serializers.DateTimeField(required=False, allow_null=True)
    
    class Meta:
        model = Interaction
        fields = ['user', 'start_at', 'end_at', 'type', 'interact_with', 'contact', 'description']