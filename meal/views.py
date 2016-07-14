from rest_framework import viewsets, permissions
from reporter.models import Reporter
from .models import Meal
from .serializers import MealSerializer
from .permissions import MealUserPermissions
from datetime import datetime


class MealViewSet(viewsets.ModelViewSet):
    """
    View set of Meal API
    """

    permission_classes = [permissions.IsAuthenticated, MealUserPermissions]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    def get_queryset(self):
        queryset = Meal.objects.all()
        only_today = self.request.query_params.get('only_today')
        if only_today:
            return queryset.filter(reporter=Reporter.objects.get(user=self.request.user),
                                   date=datetime.today())
        if self.request.user.is_staff:
            user = self.request.query_params.get('user')
            if user:
                queryset = queryset.filter(reporter=Reporter.objects.get(user=user))
        else:
            queryset = queryset.filter(reporter=Reporter.objects.get(user=self.request.user))
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        start_time = self.request.query_params.get('start_time')
        end_time = self.request.query_params.get('end_time')
        if start_time:
            if start_date:
                queryset = queryset.exclude(date=start_date,
                                            time__lt=start_time)
            queryset = queryset.filter(time__gte=start_time)
        if end_time:
            if end_date:
                queryset = queryset.exclude(date=end_date,
                                            time__gt=end_time)
            queryset = queryset.filter(time__lte=end_time)
        return queryset

    def perform_create(self, serializer):
        serializer.save(reporter=Reporter.objects.get(user=self.request.user))
