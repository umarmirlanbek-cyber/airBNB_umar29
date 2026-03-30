from rest_framework.permissions import BasePermission

class ClientPermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'guest':
            return True
        return False

class OwnerPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'host'