from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class IsEmployeeOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'employee' or request.user.is_superuser

class IsTaskOwnerOrEmployee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.user_type == 'employee' or request.user.is_superuser:
            return True
        return obj.client == request.user

class IsClient(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == 'client' or request.user.is_superuser 
