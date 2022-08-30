from rest_framework.permissions import IsAuthenticated


class IsSchool(IsAuthenticated):
    def has_permission(self, request, view):
        base_permission = super().has_permission(request, view)

        if not base_permission or not request.user:
            return False

        if not request.user.is_staff:
            return False

        return True
