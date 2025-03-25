from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return obj == request.user

class OnlyAdminAccess(BasePermission):

    def has_permission(self, request, view):
        if not request.user or not request.user.is_staff:
            self.message = {"detail": "Only admins can see the user list."}
            return False
        return True