from rest_framework import permissions


class UserOwnerPermissions(permissions.BasePermission):
    """Object level permissions of User model.
    All actions are allowed.
    Only owners are allowed.
    """

    def has_object_permission(self, request, view, obj):
        # Otherwise, allow only own account
        return request.user == obj
   
        
class AnonymousPermissions(permissions.BasePermission):
    """Permissions checked anonymous users.
    All actions are allowed.
    """

    def has_permission(self, request, view):
        # Allow rest methods for authenticated user only
        if request.user.is_anonymous:
            return True

        return False


class ModeratorPermissions(permissions.BasePermission):
    """Permissions checked users with Moderator type Account.
    All actions are allowed.
    """

    def has_permission(self, request, view):
        # Allow rest methods for authenticated user only
        if request.user.account.is_moderator:
            return True

        return False


class TrainerPermissions(permissions.BasePermission):
    """Permissions checked users with Trainer type Account.
    All actions are allowed.
    """

    def has_permission(self, request, view):
        # Allow rest methods for authenticated user only
        if request.user.account.is_trainer:
            return True

        return False


class ClientPermissions(permissions.BasePermission):
    """Permissions checked users with Client type Account.
    All actions are allowed.
    """

    def has_permission(self, request, view):
        # Allow rest methods for authenticated user only
        if request.user.account.is_client:
            return True

        return False


class InviteOwnPermissions(permissions.BasePermission):
    """
    """

    def has_object_permission(self, request, view, obj):
        # Otherwise, allow only own account
        is_client_owner = request.user.account.is_client and request.user.account.client == obj.client
        is_trainer_owner = request.user.account.is_trainer and request.user.account.trainer == obj.trainer
        return is_client_owner or is_trainer_owner


class InviteOpenPermissions(permissions.BasePermission):
    """
    """

    def has_object_permission(self, request, view, obj):
        # Otherwise, allow only own account
        return obj.is_open
