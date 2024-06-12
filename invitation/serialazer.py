from rest_framework import serializers
from invitation.models import Invitation
from django.contrib.auth import get_user_model

User=get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']


class InvitationSerializer(serializers.ModelSerializer):
    # This class use all fields in the model

    class Meta:
        model = Invitation
        fields = "__all__"

class InvitationCreateSerializer(serializers.ModelSerializer):
    # This class use for creating a new invitation

    role = serializers.CharField()
    org = serializers.CharField()
    invitee_email = serializers.EmailField()
    
    class Meta:
        model = Invitation
        fields = ("inviter", "invitee_email", "role", "org")