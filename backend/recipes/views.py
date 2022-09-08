"""Views для эндпоинтов тегов, ингредиентов, рецептов."""

from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        ingredients = serializer.validated_data.pop('recipeingredientamount_set')
        tags = serializer.validated_data.pop('tags')
        created_recipe = serializer.save(author=request.user, tags=tags)

        ingredients_for_recipe = [
            RecipeIngredientAmount(
                recipe=created_recipe,
                ingredient_id=ingredient['ingredient']['id'],
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        created_recipe.recipeingredientamount_set.bulk_create(ingredients_for_recipe)

        headers = self.get_success_headers(serializer.data)
        tags = TagSerializer(data=tags, many=True)
        tags.is_valid(raise_exception=False)
        serializer._data['tags'] = tags.data
        return Response(serializer.data, status=HTTP_201_CREATED, headers=headers)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    #     ingredients = serializer.validated_data.get('recipeingredientamount_set',
    #                                                 False)
    #     if ingredients:
    #         ingredients = serializer.validated_data.pop('recipeingredientamount_set')
    #         print(ingredients)
    #         for ingredient in ingredients:

    #         ingredients_for_recipe = [
    #             RecipeIngredientAmount(
    #                 recipe=instance,
    #                 ingredient_id=ingredient['ingredient']['id'],
    #                 amount=ingredient['amount']
    #             ) for ingredient in ingredients
    #         ]
    #         instance.recipeingredientamount_set.bulk_create(ingredients_for_recipe)

    #     serializer = RecipeSerializer(
    #         serializer.instance,
    #         context={'request': self.request},
    #     )

    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         instance._prefetched_objects_cache = {}
    #     return Response(serializer.data)
