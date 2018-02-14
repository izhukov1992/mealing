from rest_framework import permissions

from .constants import TRAINER, MODERATOR
from .models import Account


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
        account = Account.objects.get(user=request.user)
        if request.user.is_staff or account.role == MODERATOR:
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
        account = Account.objects.get(user=request.user)
        if request.user.is_staff or account.role == MODERATOR:
            return True
        if account.role == TRAINER:
            if request.method == "GET":
                return True
            return False
        return request.user == obj.user
