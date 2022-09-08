"""Права для эндпоинтов рецептов."""

from rest_framework import permissions


class IsAuthorOrGetObjectOnly(permissions.BasePermission):
    """Разрешение на просмотр всем и на изменение автору."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
