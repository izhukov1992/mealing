from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    """Permissions checking allowed methods and User instance.
    Creating is allowed for anonymous users only.
    Rest actions are allowed for authenticated users only.
    Own instances allowed only.
    """

    def has_permission(self, request, view):
        # Allow POST for anonymous user only
        if request.method == "POST":
            if request.user.is_anonymous:
                return True
            return False

        # Allow rest methods for authenticated user only
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        # Allow own user only
        return request.user == obj


class AccountPermissions(permissions.BasePermission):
    """Permissions checking allowed Acount instances.
    All actions are allowed.
    All instances are allowed for staff Accounts.
    Own instances are allowed for rest authenticated users.
    """

    def has_object_permission(self, request, view, obj):
        # If staff account, allow all accounts
        if request.user.account.is_staff:
            return True

        # Otherwise, allow only own account
        return request.user == obj.user
