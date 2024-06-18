from rest_framework import serializers
from invitation.models import Invitation
from django.contrib.auth import get_user_model
from common.models import Profile

User=get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        user = User(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class InvitationSerializer(serializers.ModelSerializer):
    # This class use all fields in the model

    class Meta:
        model = Invitation
        fields = "__all__"

class InvitationNewSerializer(serializers.ModelSerializer):
    # This class use for creating a new invitation

    token = serializers.CharField()
    inviter_id = serializers.CharField(required=True)
    invitee_id = serializers.UUIDField(required=True)
    
    def validate_inviter_id(self, value):
        """
        Validates that the inviter ID exists in the database.
        """
        try:
            User.objects.get(pk=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid inviter ID. User does not exist.')

    def validate_invitee_id(self, value):
        """
        Validates that the invitee ID exists in the database.
        """
        try:
            User.objects.get(pk=value)
            return value
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid invitee ID. User does not exist.')

    
    class Meta:
        model = Invitation
        fields = (
            "inviter_id",
            "invitee_id",
            "token"
            )
    


class InvitationCreateSerializer(serializers.ModelSerializer):
    # This class use for creating a new invitation

    role = serializers.CharField()
    org = serializers.CharField()
    invitee_email = serializers.EmailField()
    
    class Meta:
        model = Invitation
        fields = ("inviter", "invitee_email", "role", "org")

class CreateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "role",
            "user",
            "org"
        )