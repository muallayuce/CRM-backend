from rest_framework import serializers
from invitation.models import Invitation


class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = (
            "inviter",
            "invitee_email"
        )