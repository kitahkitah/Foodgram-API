"""Сериализаторы для модели и эндпоинтов тегов, ингредиентов, рецептов."""

from rest_framework import serializers

from .models import Ingredient, Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для модели тега."""

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для модели ингредиента."""

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
