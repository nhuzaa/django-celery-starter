from rest_framework import permissions
from devices.models import Device

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users to access the view.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff

class DeviceAccessPermission(permissions.BasePermission):
    """
    Custom permission to only allow managers to access all devices
    and engineers to access only their assigned devices.
    """
    def has_permission(self, request, view):
        # Allow all authenticated users to list devices
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        # Allow managers full access
        if request.user.is_manager():
            return True
        
        # Allow engineers to access only their assigned devices
        if request.user.is_engineer():
            return obj.assigned_to == request.user
        
        return False 