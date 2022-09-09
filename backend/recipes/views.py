"""Views для эндпоинтов тегов, ингредиентов, рецептов."""

from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Ingredient, Recipe, RecipeIngredientAmount, Tag
from .permissions import IsAuthorOrGetObjectOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class TagViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Вьюсет для эндпоинтов с тегами."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Вьюсет для эндпоинтов с тегами."""

    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(ModelViewSet):
    """Вьюсет для эндпоинтов с рецептами."""

    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrGetObjectOnly)
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()

    def perform_create(self, serializer):
        ingredients = serializer.validated_data.pop('recipeingredientamount_set')
        created_recipe = serializer.save(author=self.request.user)
        self.bulk_create(created_recipe, ingredients)

    def perform_update(self, serializer):
        if serializer.validated_data.get('recipeingredientamount_set', False):
            ingredients = serializer.validated_data.pop('recipeingredientamount_set')
            updated_recipe = serializer.save()
            updated_recipe.ingredients.clear()
            self.bulk_create(updated_recipe, ingredients)
        else:
            serializer.save()

    def bulk_create(self, recipe, ingredients):
        ingredients_for_recipe = [
            RecipeIngredientAmount(
                recipe=recipe,
                ingredient_id=ingredient['ingredient']['id'],
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        recipe.recipeingredientamount_set.bulk_create(ingredients_for_recipe)
