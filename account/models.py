from django.db import models
from django.contrib.auth.models import User

from .constants import ACCOUNT_TYPES, CLIENT, TRAINER, MODERATOR


class AccountManager(models.Manager):
    """Account manager
    """

    def get_by_user(self, user):
        return self.filter(user=user)


class Account(models.Model):
    """Account model
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    limit = models.IntegerField(default=2500)
    role = models.CharField(max_length=255, choices=ACCOUNT_TYPES, default=CLIENT)
    objects = AccountManager()

    @property
    def is_staff(self):
        return self.role == MODERATOR or self.role == TRAINER
