from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            User.objects.create_superuser(username='admin', password='AdminAdmin123', email='admin@admin.com')
        except:
            pass
