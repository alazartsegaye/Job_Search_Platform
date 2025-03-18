from rest_framework.permissions import BasePermission
from rest_framework.views import View


class IsEmployer(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.employer == request.user
    