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
        return Meal.objects.filter(reporter=Reporter.objects.get(user=self.request.user))

    def perform_create(self, serializer):
        serializer.save(reporter=Reporter.objects.get(user=self.request.user))
