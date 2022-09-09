"""Фильтсеты для эндпоинтов рецептов."""

from django_filters import BooleanFilter, CharFilter, FilterSet

from .models import Recipe


class AuthorTagsFilterSet(FilterSet):
    """Фильтерсет для изменения имени поля тегов."""

    tags = CharFilter(field_name='tags__slug')
    is_favorited = BooleanFilter(field_name='favorited_by', method='favorites')
    is_in_shopping_cart = BooleanFilter(field_name='in_shopping_cart_of',
                                        method='favorites')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def favorites(self, queryset, name, value):
        """Отфильтровать по избранному пользователя."""
        if not self.request.user.is_anonymous and value:
            return queryset.filter(**{name: self.request.user})
        return queryset