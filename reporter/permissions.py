from rest_framework import permissions


class UserPermissions(permissions.BasePermission):
    """
    Permissions checking owner of User objects
    """
    
    def has_permission(self, request, view):
        if request.user.is_anonymous():
            if request.method == "POST":
                return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj


class ReporterUserPermissions(permissions.BasePermission):
    """
    Permissions checking owner of Reporter objects
    """
    
    def has_permission(self, request, view):
        if request.user.is_anonymous():
            if request.method == "POST":
                return True
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
