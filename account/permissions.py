from rest_framework import permissions

from .constants import TRAINER, MODERATOR


class UserPermissions(permissions.BasePermission):
    """Permissions checking owner of User objects
    """
    
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            if request.method == "POST":
                return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.account.is_staff:
            return True

        return request.user == obj


class AccountUserPermissions(permissions.BasePermission):
    """Permissions checking owner of Account objects
    """
    
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            if request.method == "POST":
                return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.account.role == MODERATOR:
            return True
        if request.user.account.role == TRAINER:
            if request.method == "GET":
                return True
            return False
        return request.user == obj.user
