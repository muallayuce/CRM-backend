from django.db import models
from common.base import BaseModel  
from leads.models import Lead

class Negotiation(BaseModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="negotiations")
    negotiation_details = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    new_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "Negotiation"
        verbose_name_plural = "Negotiations"

    def __str__(self):
        return f"Negotiation for Lead {self.lead_id}"