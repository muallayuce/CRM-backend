from django.db import models
from common.base import BaseModel  
from leads.models import Lead

class Qualified(BaseModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="qualified")
    description_of_services = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    offer_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "Qualified"
        verbose_name_plural = "Qualifieds"

    def __str__(self):
        return f"Qualified for Lead {self.lead_id}"