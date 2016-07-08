from django.db import models
from reporter.models import Reporter


class Meal(models.Model):
    """
    Meal model
    """

    reporter = models.ForeignKey(Reporter)
    date = models.DateField()
    time = models.TimeField()
    description = models.CharField(max_length=255)
    calories = models.IntegerField()
