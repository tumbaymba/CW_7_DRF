from rest_framework.permissions import BasePermission


class IsOwnerHabit(BasePermission):
    message = "Вы не являетесь владельцем"

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return request.method in ('GET', 'PUT', 'PATCH', 'DELETE')
        return False