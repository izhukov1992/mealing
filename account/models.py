from django.db import models
from django.contrib.auth.models import User

from .constants import ACCOUNT_TYPES, MODERATOR, TRAINER, CLIENT


class AccountManager(models.Manager):
    """Account manager
    """

    def get_by_user(self, user):
        return self.filter(user=user)


class Account(models.Model):
    """Account model
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=255, choices=ACCOUNT_TYPES, default=CLIENT)
    available = models.BooleanField(default=True)
    objects = AccountManager()

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_trainer(self):
        return self.role == TRAINER

    @property
    def is_client(self):
        return self.role == CLIENT


class Moderator(models.Model):
    """Moderator model
    """

    account = models.OneToOneField(Account, on_delete=models.CASCADE)


class Trainer(models.Model):
    """Trainer model
    """

    account = models.OneToOneField(Account, on_delete=models.CASCADE)


class Client(models.Model):
    """Client model
    """

    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    limit = models.IntegerField(default=2500)
    trainers = models.ManyToManyField(Trainer, related_name='clients')
