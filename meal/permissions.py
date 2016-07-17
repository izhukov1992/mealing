from rest_framework import permissions
from reporter.models import Reporter


class MealUserPermissions(permissions.BasePermission):
    """
    Permissions checking owner of Meal objects
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        reporter = Reporter.objects.get(user=request.user)
        if int(reporter.role) == 3 or int(reporter.role) == 2:
            return True
        return request.user == obj.reporter.user
