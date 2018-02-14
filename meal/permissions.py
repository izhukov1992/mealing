from rest_framework import permissions

from account.constants import TRAINER, MODERATOR
from account.models import Account


class MealUserPermissions(permissions.BasePermission):
    """Permissions checking owner of Meal objects
    """

    def has_object_permission(self, request, view, obj):
        account = Account.objects.get(user=request.user)
        if request.user.is_staff or account.role == MODERATOR or account.role == TRAINER:
            return True
        return request.user == obj.account.user
