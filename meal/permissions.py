from rest_framework import permissions

from account.constants import TRAINER, MODERATOR


class MealUserPermissions(permissions.BasePermission):
    """Permissions checking owner of Meal objects
    """

    def has_object_permission(self, request, view, obj):
        if request.user.account.is_staff:
            return True

        return request.user == obj.account.user
