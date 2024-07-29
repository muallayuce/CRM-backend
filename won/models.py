from django.db import models
from common.base import BaseModel
from leads.models import Lead

class Won(BaseModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="wons")
    contract = models.TextField(blank=True, null=True)
    review = models.TextField(blank=True, null=True)
    delivery_plan = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    deal_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "Won"
        verbose_name_plural = "Wons"

    def __str__(self):
        return f"Won deal for Lead {self.lead_id}"
