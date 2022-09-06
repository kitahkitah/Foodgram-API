"""Views для эндпоинтов тегов, ингредиентов, рецептов."""

from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Ingredient, Tag
from .serializers import IngredientSerializer, TagSerializer


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
