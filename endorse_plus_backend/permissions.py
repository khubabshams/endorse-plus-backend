from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied


class IsOwnerOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user if hasattr(obj, 'owner') \
            else obj.profile.owner == request.user


class IsAdminOrReadOnly(permissions.IsAdminUser):

    def has_permission(self, request, view):
        is_admin = super(IsAdminOrReadOnly, self).has_permission(request, view)
        return request.method in permissions.SAFE_METHODS or is_admin


class IsOwnerOrReceiver(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or \
                request.user in [obj.profile.owner, obj.receiver.owner]:
            return True
        raise PermissionDenied({'detail':
                                'You don not have permission to access'})
