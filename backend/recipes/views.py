"""Views для эндпоинтов тегов, ингредиентов, рецептов."""

from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .models import Ingredient, Recipe, Tag
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
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.all()
