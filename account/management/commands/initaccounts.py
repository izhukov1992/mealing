from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from account.constants import CLIENT, MODERATOR
from account.models import Account


class Command(BaseCommand):

    def handle(self, *args, **options):
        for user in User.objects.filter(account=None):
            Account.objects.create(user=user, role=(MODERATOR if user.is_staff else CLIENT))
