from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from datetime import datetime

from account.permissions import StaffPermissions

from .models import Meal
from .serializers import MealClientSerializer, MealStaffSerializer
from .permissions import MealStaffOrOwnerPermissions, MealOwnerPermissions


class MealClientViewSet(viewsets.ModelViewSet):
    """View set of Meal API.
    Used for creating, listing, viewing, updating and deleting Meals.
    Allowed only for owners.
    Changing users is not allowed.
    """

    permission_classes = [IsAuthenticated, MealOwnerPermissions]
    queryset = Meal.objects.none()
    serializer_class = MealClientSerializer

    def get_queryset(self):
        return Meal.objects.get_by_user(self.request.user)

    def get_object(self):
        meal = get_object_or_404(Meal, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, meal)
        return meal

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MealStaffViewSet(viewsets.ModelViewSet):
    """View set of Meal API.
    Used for creating, listing, viewing, updating and deleting Meals.
    Allowed only for users with staff type Account.
    Changing users is allowed.
    """

    permission_classes = [IsAuthenticated, StaffPermissions]
    queryset = Meal.objects.all()
    serializer_class = MealStaffSerializer

    def get_queryset(self):
        user = self.request.query_params.get('user')
        in_date = self.request.query_params.get('in_date')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')

        meals = Meal.objects.all()

        if user:
            meals = Meal.objects.get_by_user(user)

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
