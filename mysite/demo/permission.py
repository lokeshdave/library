from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsLibrarian(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == "librarian"


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user