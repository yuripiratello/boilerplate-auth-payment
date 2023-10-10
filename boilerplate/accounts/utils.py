from rest_framework import permissions


class HasPlanPermission(permissions.BasePermission):
    message = "User doesn't have a plan"

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.profile.has_plan()
