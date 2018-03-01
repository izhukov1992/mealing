from rest_framework import permissions


class MealOwnerPermissions(permissions.BasePermission):
    """Object level permissions of Meal model.
    All actions are allowed.
    Only owners are allowed.
    """

    def has_object_permission(self, request, view, obj):
        # Otherwise, allow only own meals
        return request.user == obj.client.account.user
