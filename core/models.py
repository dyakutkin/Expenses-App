from __future__ import unicode_literals

from datetime import date
from django.utils import timezone

from django.db import models
from django.contrib.auth.models import User


def current_time(): timezone.now().time()


class Item(models.Model):
    text = models.CharField(null=True, blank=True, max_length=50)
    date = models.DateField(default=date.today)
    time = models.TimeField(null=True, blank=True, default=current_time)
    cost = models.FloatField(null=True, blank=True, default=0)
    user = models.ForeignKey(User)
