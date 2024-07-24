from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth import get_user_model
from contacts.models import Contact
from leads.models import Lead
import arrow
import uuid

User = get_user_model()

class Interaction(models.Model):
    TYPE_CHOICES = [
        ('Call', 'Call'),
        ('Email', 'Email'),
        ('Meeting', 'Meeting'),
        ('Task', 'Task'),
    ]

    id = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False, db_index=True, primary_key=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='Call',
        verbose_name=_("Type")
    )
    interact_with = models.ForeignKey(Lead, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} interacted with {self.interact_with} on {self.created_at}"
    
    class Meta:
        verbose_name =_("Interactions")
        verbose_name_plural =_("Interactions")
        db_table = "interaction"
        ordering = ("-created_at",)

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_at).humanize()
    
    @property
    def created_on(self):
        return self.created_at
    
    @property
    def duration(self):
        if self.start_at and self.end_at:
            return self.end_at - self.start_at
        return None