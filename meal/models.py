from django.db import models
from django.contrib.auth.models import User


class Reporter(models.Model):
    """
    Reporter model
    """

    user = models.OneToOneField(User)
    limit = models.IntegerField()


class Meal(models.Model):
    """
    Meal model
    """

    reporter = models.ForeignKey(Reporter)
    date = models.DateField()
    time = models.TimeField()
    description = models.CharField(max_length=255)
    calories = models.IntegerField()
