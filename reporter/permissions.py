from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    """
    Permissions checking owner of User objects
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class ReporterUserPermissions(permissions.BasePermission):
    """
    Permissions checking owner of Reporter objects
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
