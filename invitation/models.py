from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Invitation(models.Model):
    # Model for creation and working with invitations table and objects

    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    invitee = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(null=True, blank=True)
    used = models.BooleanField(False)

    class Meta:
        # Adding table name

        verbose_name = "Invitation"
        verbose_name_plural = "Invitations"
        db_table = 'invitations'

    def __str__(self):
        return f"Invitation from {self.inviter} to {self.invitee}"

    def is_valid(self):
        return self.expires_at is None or self.expires_at > timezone.now() and not self.used