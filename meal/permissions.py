from rest_framework import permissions

from account.constants import TRAINER, MODERATOR


class MealUserPermissions(permissions.BasePermission):
    """Permissions checking allowed Meal instances.
    All actions are allowed.
    All instances are allowed for staff Accounts.
    Own instances are allowed for rest authenticated users.
    """

    def has_object_permission(self, request, view, obj):
        # If staff account, allow all meals
        if request.user.is_authenticated and request.user.account.is_staff:
            return True

        # Otherwise, allow only own meals
        return request.user == obj.user
