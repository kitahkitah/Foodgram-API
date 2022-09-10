"""Views для эндпоинтов тегов, ингредиентов, рецептов."""

from io import BytesIO

from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .commons import change_object_status
from .filters import RecipeFilterSet
from .models import Ingredient, Recipe, RecipeIngredientAmount, Tag
from .permissions import IsAuthorOrGetObjectOnly
from .serializers import IngredientSerializer, RecipeSerializer, TagSerializer


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для эндпоинтов с тегами."""

    pagination_class = None
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для эндпоинтов с тегами."""

    filter_backends = (SearchFilter,)
    pagination_class = None
    search_fields = ('^name',)
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(ModelViewSet):
    """Вьюсет для эндпоинтов с рецептами."""

    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet
    http_method_names = ('get', 'post', 'patch', 'delete')
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrGetObjectOnly)
    serializer_class = RecipeSerializer
    queryset = Recipe.objects.prefetch_related('in_shopping_cart_of', 'favorited_by')

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

    @staticmethod
    def bulk_create(recipe, ingredients):
        """Создать ингредиенты с количеством для рецепта, используя bulk_create."""
        ingredients_for_recipe = [
            RecipeIngredientAmount(
                recipe=recipe,
                ingredient_id=ingredient['ingredient']['id'],
                amount=ingredient['amount']
            ) for ingredient in ingredients
        ]
        recipe.recipeingredientamount_set.bulk_create(ingredients_for_recipe)

    @action(['POST', 'DELETE'], detail=True, permission_classes=(IsAuthenticated,))
    def favorite(self, request, pk):
        """Изменить статус рецепта (избранный)."""
        instance = self.get_object()
        response = change_object_status(instance, request, 'favorited_by')
        return response

    @action(['POST', 'DELETE'], detail=True, permission_classes=(IsAuthenticated,))
    def shopping_cart(self, request, pk):
        """Изменить статус рецепта (в списке покупок)."""
        instance = self.get_object()
        response = change_object_status(instance, request, 'in_shopping_cart_of')
        return response

    @action(['GET'], detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        """Скачать список покупок."""
        output = {}
        ingredients = (
            RecipeIngredientAmount.objects
            .filter(recipe__in_shopping_cart_of__id=request.user.id)
            .values_list('ingredient__name', 'ingredient__measurement_unit', 'amount')
        )

        for ingredient in ingredients:
            name = f'{ingredient[0]} ({ingredient[1]})'
            if name in output:
                output[name] += ingredient[2]
            else:
                output[name] = ingredient[2]

        registerFont(TTFont('Calibri', 'Calibri.ttf', 'UTF-8'))
        buffer = BytesIO()
        page = Canvas(buffer)
        page.setFont('Calibri', 18)
        page.drawString(210, 800, 'Список ингредиентов')
        page.setFont('Calibri', 14)

        height = 750
        for number, (name, amount) in enumerate(output.items(), 1):
            page.drawString(75, height, f'{number}. {name} - {amount}')
            height -= 20

        page.showPage()
        page.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='shopping_cart.pdf')
