from rest_framework import viewsets, permissions
from rest_framework.response import Response

from datetime import datetime

from account.constants import TRAINER, MODERATOR
from account.models import Account

from .models import Meal
from .serializers import MealSerializer
from .permissions import MealUserPermissions


class MealViewSet(viewsets.ModelViewSet):
    """View set of Meal API
    """

    permission_classes = [permissions.IsAuthenticated, MealUserPermissions]
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    def get_queryset(self):
        queryset = Meal.objects.all()
        account = Account.objects.get(user=self.request.user)
        if self.request.user.is_staff or account.role == MODERATOR or account.role == TRAINER:
            account_param = self.request.query_params.get('account')
            if account_param:
                queryset = queryset.filter(account=account_param)
        else:
            queryset = queryset.filter(account=account)
        only_today = self.request.query_params.get('only_today')
        if only_today:
            return queryset.filter(date=datetime.today())
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
 
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            account = Account.objects.get(user=request.user)
            if request.user.is_staff or account.role == MODERATOR or account.role == TRAINER:
                account_param = serializer.validated_data.get('account')
                if account_param:
                    meal = serializer.save(account=account_param)
                else:
                    meal = serializer.save(account=account)
            else:
                meal = serializer.save(account=account)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
