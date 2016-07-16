from django.db import models
from django.contrib.auth.models import User


class Reporter(models.Model):
    """
    Reporter model
    """

    user = models.OneToOneField(User, blank=True, null=True)
    limit = models.IntegerField(default=2500)
    role = models.CharField(
        max_length=255,
        choices=(
            (1, 'User'),
            (2, 'Manager'),
            (3, 'Admin')
        ),
        default=1,
    )