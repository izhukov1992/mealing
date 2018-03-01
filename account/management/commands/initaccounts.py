from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from account.constants import MODERATOR, TRAINER, CLIENT
from account.models import Account, Moderator, Trainer, Client


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in User.objects.filter(account=None):
            account = Account.objects.create(user=user, role=(MODERATOR if user.is_staff else CLIENT))

        for account in Account.objects.filter(client=None, trainer=None, moderator=None):
            if account.role == MODERATOR:
                Moderator.objects.create(account=account)
            elif account.role == TRAINER:
                Trainer.objects.create(account=account)
            elif account.role == CLIENT:
                Client.objects.create(account=account)
