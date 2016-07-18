from rest_framework import permissions
from .models import Reporter


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
        reporter = Reporter.objects.get(user=request.user)
        if request.user.is_staff or int(reporter.role) == 3:
            return True
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
        reporter = Reporter.objects.get(user=request.user)
        if request.user.is_staff or int(reporter.role) == 3:
            return True
        if int(reporter.role) == 2:
            if request.method == "GET":
                return True
            return False
        return request.user == obj.user
