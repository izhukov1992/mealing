from django.db import models
from django.contrib.auth.models import User


class MealQuerySet(models.QuerySet):
    """Meal QuerySet
    """

    def get_by_user(self, user):
        return self.filter(user=user)

    def get_by_date(self, date):
        return self.filter(date=date)

    def get_from_date(self, date):
        return self.filter(date__gte=date)

    def get_due_date(self, date):
        return self.filter(date__lte=date)

    def get_from_time(self, time):
        return self.filter(time__gte=start_time)

    def get_due_time(self, time):
        return self.filter(time__lte=end_time)

    def get_from_datetime(self, date, time):
        return self.filter(date__gte=date).exclude(date=date, time__lt=time)

    def get_due_datetime(self, date, time):
        return self.filter(date__lte=date).exclude(date=date, time__gt=time)


class Meal(models.Model):
    """Meal model
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    description = models.CharField(max_length=255)
    calories = models.IntegerField()
    objects = MealQuerySet.as_manager()
