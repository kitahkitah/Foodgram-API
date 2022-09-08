"""Сериализаторы для моделей и эндпоинтов тегов, ингредиентов, рецептов."""

from rest_framework import serializers

from users.serializers import UserSerializer
from .fields import Base64ImageField, ModelPKRelatedField
from .models import Ingredient, Recipe, RecipeIngredientAmount, Tag


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


class RecipeIngredientAmountSerializer(serializers.ModelSerializer):
    """Сериализатор для связки рецепта, ингредиента и количества."""

    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )

    class Meta:
        model = RecipeIngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для модели рецепта."""

    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = RecipeIngredientAmountSerializer(
        source='recipeingredientamount_set',
        required=True,
        many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    tags = ModelPKRelatedField(
        queryset=Tag.objects.all(),
        serializer=TagSerializer,
        required=True,
        many=True,
    )

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time')

    def get_is_favorited(self, object):
        """Проверить наличие рецепта в избранных пользователя."""
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        return request.user.favorites.filter(id=object.id).exists()

    def get_is_in_shopping_cart(self, object):
        """Проверить наличие рецепта в списке покупок пользователя."""
        request = self.context.get("request")
        if request.user.is_anonymous:
            return False
        return request.user.shopping_cart.filter(id=object.id).exists()
