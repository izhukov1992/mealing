from django.db import models
from django.contrib.auth.models import User

from .constants import ACCOUNT_TYPES, CLIENT


class Account(models.Model):
    """Account model
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    limit = models.IntegerField(default=2500)
    role = models.CharField(max_length=255, choices=ACCOUNT_TYPES, default=CLIENT)
