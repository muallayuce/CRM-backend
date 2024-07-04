from rest_framework import serializers

from common.serializer import ProfileSerializer, UserSerializer
from contacts.serializer import ContactSerializer
from leads.serializer import LeadSerializer
from .models import Interaction

class InteractionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    interact_with = LeadSerializer(read_only=True)
    contact = ContactSerializer(read_only=True)

    class Meta:
        model = Interaction
        fields = ['id', 'user', 'created_at', 'updated_at', 'start_at', 'end_at', 'type', 'interact_with', 'contact', 'description']
