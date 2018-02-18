from rest_framework import viewsets, permissions
from rest_framework.response import Response

from datetime import datetime

from .models import Meal
from .serializers import MealSerializer
from .permissions import MealUserPermissions


class MealViewSet(viewsets.ModelViewSet):
    """View set of Meal API.
    Used for listing, viewing, updating and deleting Meals.
    """

    permission_classes = [permissions.IsAuthenticated,]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    def get_queryset(self):
        user = self.request.query_params.get('user')
        in_date = self.request.query_params.get('in_date')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')

        meals = Meal.objects.get_by_user(self.request.user)

        if self.request.user.account.is_staff:
            if user:
                meals = Meal.objects.get_by_user(user)
            else:
                meals = Meal.objects.all()

        if in_date:
            return meals.get_by_date(in_date)

        if start_date and start_time:
            meals = meals.get_from_datetime(start_date, start_time)
        else:
            if start_date:
                meals = meals.get_from_date(start_date)
            if start_time:
                meals = meals.get_from_time(start_time)

        if end_date and end_time:
            meals = meals.get_due_datetime(end_date, end_time)
        else:
            if end_date:
                meals = meals.get_due_date(end_date)
            if end_time:
                meals = meals.get_due_time(end_time)

        return meals

    def perform_create(self, serializer):
        user = serializer.validated_data.get('user')

        if self.request.user.account.is_staff and user:
            meal = serializer.save(user=user)
        else:
            meal = serializer.save(user=self.request.user)
