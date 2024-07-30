from django.db import models
from common.base import BaseModel
from leads.models import Lead
from accounts.models import Profile


class Meeting(BaseModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="meetings")
    date_time = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=255)
    participants = models.ManyToManyField(Profile, related_name="meeting_participants")
    notes = models.TextField(blank=True, null=True)
    estimated_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)


    class Meta:
        verbose_name = "Meeting"
        verbose_name_plural = "Meetings"


    def __str__(self):
        return f"Meeting on {self.date_time} for {self.lead}"