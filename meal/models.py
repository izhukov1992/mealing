from django.db import models

from account.models import Account


class Meal(models.Model):
    """Meal model
    """

    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    description = models.CharField(max_length=255)
    calories = models.IntegerField()
