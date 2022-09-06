"""Views для эндпоинтов тегов, ингредиентов, рецептов."""

from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet

from .models import Tag
from .serializers import TagSerializer


class TagViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    """Вьюсет для эндпоинтов с тегами."""

    serializer_class = TagSerializer
    queryset = Tag.objects.all()
