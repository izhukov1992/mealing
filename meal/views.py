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
        queryset = Meal.objects.filter(reporter=Reporter.objects.get(user=self.request.user))
        only_today = self.request.query_params.get('only_today')
        if only_today:
            return queryset.filter(date=datetime.today())
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
            start_time = self.request.query_params.get('start_time')
            if start_time:
                queryset = queryset.exclude(time__lt=start_time)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
            end_time = self.request.query_params.get('end_time')
            if end_time:
                queryset = queryset.exclude(time__gt=end_time)
        return queryset

    def perform_create(self, serializer):
        serializer.save(reporter=Reporter.objects.get(user=self.request.user))
