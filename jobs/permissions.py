from rest_framework.permissions import BasePermission

class IsEmployer(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.employer == request.user
