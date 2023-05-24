from rest_framework import permissions


class IsOwnerOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user if hasattr(obj, 'owner') \
            else obj.profile.owner == request.user