from rest_framework import permissions
from rest_framework.exceptions import NotFound


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not obj:
            raise NotFound()

        return request.user == obj.author

    def has_permission(self, request, view):
        return super().has_permission(request, view)
