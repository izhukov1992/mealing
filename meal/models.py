from django.db import models
from django.contrib.auth.models import User


class Meal(models.Model):
    """Meal model
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    description = models.CharField(max_length=255)
    calories = models.IntegerField()
