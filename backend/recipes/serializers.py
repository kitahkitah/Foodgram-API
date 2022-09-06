"""Сериализаторы для модели и эндпоинтов тегов, ингредиентов, рецептов."""

from rest_framework import serializers

from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели тега."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
