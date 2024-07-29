from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Lead
from meeting.models import Meeting
from opportunity.models import Opportunity
from qualified.models import Qualified
from negotiation.models import Negotiation
from won.models import Won

@receiver(post_save, sender=Lead)
def handle_status_change(sender, instance, **kwargs):
    if instance.status == 'lead':
        Lead.objects.get_or_create(lead=instance)
    elif instance.status == 'meeting':
        Meeting.objects.get_or_create(lead=instance)
    elif instance.status == 'opportunity':
        Opportunity.objects.get_or_create(lead=instance)
    elif instance.status == 'qualified':
        Qualified.objects.get_or_create(lead=instance)
    elif instance.status == 'negotiation':
        Negotiation.objects.get_or_create(lead=instance)
    elif instance.status == 'won':
        Won.objects.get_or_create(lead=instance)