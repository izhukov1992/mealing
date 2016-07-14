from rest_framework import permissions


class MealUserPermissions(permissions.BasePermission):
    """
    Permissions checking owner of Meal objects
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return request.user == obj.reporter.user
