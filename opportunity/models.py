import arrow
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.translation import pgettext_lazy

from accounts.models import Account, Tags
from common.models import Org, Profile
from common.base import BaseModel
from common.utils import CURRENCY_CODES, SOURCES, STAGES
from contacts.models import Contact
from leads.models import Lead
from teams.models import Teams


class Opportunity(BaseModel):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="opportunities", default=None)
    account = models.ForeignKey(
        Account,
        related_name="opportunities",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Opportunity"
        verbose_name_plural = "Opportunities"
        db_table = "opportunity"
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.lead}"

    @property
    def created_on_arrow(self):
        return arrow.get(self.created_at).humanize()
