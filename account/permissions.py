from rest_framework import permissions

from .constants import CLIENT, TRAINER, MODERATOR


class UserOwnerPermissions(permissions.BasePermission):
    """Object level permissions of User model.
    All actions are allowed.
    Only owners are allowed.
    """

    def has_object_permission(self, request, view, obj):
        # Otherwise, allow only own account
        return request.user == obj
   
        
class StaffPermissions(permissions.BasePermission):
    """Permissions checked users with staff type Account.
    All actions are allowed.
    """

    def has_permission(self, request, view):
        # Allow rest methods for authenticated user only
        if request.user.account.is_staff:
            return True

        return False
   
        
class AnonymousPermissions(permissions.BasePermission):
    """Permissions checked anonymous users.
    All actions are allowed.
    """

    def has_permission(self, request, view):
        # Allow rest methods for authenticated user only
        if request.user.is_anonymous:
            return True

        return False
   
        




class TrainerPermissions(permissions.BasePermission):
    """Permissions checked users with staff type Account.
    All actions are allowed.
    """

    def has_permission(self, request, view):
        # Allow rest methods for authenticated user only
        if request.user.account.role == TRAINER:
            return True

        return False






class ClientPermissions(permissions.BasePermission):
    """Permissions checked users with staff type Account.
    All actions are allowed.
    """

    def has_permission(self, request, view):
        # Allow rest methods for authenticated user only
        if request.user.account.role == CLIENT:
            return True

        return False
