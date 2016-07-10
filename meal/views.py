from rest_framework import viewsets, permissions
from reporter.models import Reporter
from .models import Meal
from .serializers import MealSerializer
from .permissions import MealUserPermissions


class MealViewSet(viewsets.ModelViewSet):
    """
    View set of Meal API
    """

    permission_classes = [permissions.IsAuthenticated, MealUserPermissions]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    def get_queryset(self):
        queryset = Meal.objects.filter(reporter=Reporter.objects.get(user=self.request.user))
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        return queryset

    def perform_create(self, serializer):
        serializer.save(reporter=Reporter.objects.get(user=self.request.user))
