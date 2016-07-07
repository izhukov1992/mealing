from rest_framework import viewsets, permissions
from .models import Reporter, Meal
from .serializers import ReporterSerializer, MealSerializer


class ReporterViewSet(viewsets.ModelViewSet):
    """
    View set of Reporter API
    """

    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Reporter.objects.all()
    serializer_class = ReporterSerializer


class MealViewSet(viewsets.ModelViewSet):
    """
    View set of Meal API
    """

    permission_classes = [permissions.IsAuthenticated, ]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    def perform_create(self, serializer):
        serializer.save(reporter=Reporter.objects.get(user=self.request.user))
