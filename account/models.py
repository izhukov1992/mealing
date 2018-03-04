from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

from .constants import ACCOUNT_TYPES, MODERATOR, TRAINER, CLIENT, INVITE_STATUS_TYPES, OPEN


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


class InviteQuerySet(models.QuerySet):
    """Invite QuerySet
    """

    def get_by_user(self, user):
        return self.filter(Q(client__account__user=user) | Q(trainer__account__user=user))

    def get_open(self):
        return self.filter(status=OPEN)


class InviteBase(models.Model):
    """Base Invite model
    """

    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=INVITE_STATUS_TYPES, default=OPEN)
    objects = InviteQuerySet.as_manager()

    @property
    def is_open(self):
        return self.status == OPEN

    class Meta:
        abstract = True


class InviteTrainer(InviteBase):
    """Client initiated Invite model
    """

    pass


class InviteClient(InviteBase):
    """Trainer initiated Invite model
    """

    pass
