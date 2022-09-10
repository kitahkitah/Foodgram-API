"""Настройки админки для моделей тега, ингредиента, рецепта."""

from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredientAmount, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count_favorited_by')
    list_filter = ('author', 'name', 'tags')

    def count_favorited_by(self, obj):
        return obj.favorited_by.count()


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(RecipeIngredientAmount)
admin.site.register(Tag)
