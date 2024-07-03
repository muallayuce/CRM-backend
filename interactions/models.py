from django.db import models
from django.contrib.auth import get_user_model
from contacts.models import Contact
from leads.models import Lead
import arrow


User = get_user_model()

class Interaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    interact_with = models.ForeignKey(Lead, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user} interacted with {self.interact_with} on {self.created_at}"
    
    class Meta:
        verbose_name = "Interactions"
        verbose_name_plural = "Interactions"
        db_table = "interaction"
        ordering = ("-created_at",)

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_at).humanize()
    
    @property
    def created_on(self):
        return self.created_at