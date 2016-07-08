from django.db import models
from django.contrib.auth.models import User


class Reporter(models.Model):
    """
    Reporter model
    """

    user = models.OneToOneField(User)
    limit = models.IntegerField()