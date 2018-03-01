from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from datetime import datetime

from account.permissions import ModeratorPermissions, ClientPermissions

from .models import Meal
from .serializers import MealClientSerializer, MealModeratorSerializer
from .permissions import MealOwnerPermissions


class MealBaseViewSet(viewsets.ModelViewSet):
    """Base calss of Meal API.
    Implements queryset filter method.
    """

    def filter_meals(self, meals):
        in_date = self.request.query_params.get('in_date')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')

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


class MealClientViewSet(MealBaseViewSet):
    """View set of Meal API.
    Used for creating, listing, viewing, updating and deleting Meals.
    Allowed only for owners.
    Choosing client is not allowed.
    """

    permission_classes = [IsAuthenticated, ClientPermissions, MealOwnerPermissions]
    queryset = Meal.objects.none()
    serializer_class = MealClientSerializer

    def get_queryset(self):
        meals = Meal.objects.get_by_user(self.request.user)
        return self.filter_meals(meals)

    def get_object(self):
        meal = get_object_or_404(Meal, pk=self.kwargs.get('pk'))
        self.check_object_permissions(self.request, meal)
        return meal

    def perform_create(self, serializer):
        serializer.save(client=self.request.user.account.client)


class MealModeratorViewSet(MealBaseViewSet):
    """View set of Meal API.
    Used for creating, listing, viewing, updating and deleting Meals.
    Allowed only for users with moderator type Account.
    Choosing clients is allowed.
    """

    permission_classes = [IsAuthenticated, ModeratorPermissions]
    queryset = Meal.objects.all()
    serializer_class = MealModeratorSerializer

    def get_queryset(self):
        meals = Meal.objects.all()

        user = self.request.query_params.get('user')

        if user:
            meals = Meal.objects.get_by_user(user)

        return self.filter_meals(meals)
