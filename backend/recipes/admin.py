"""Настройки админки для моделей тега, ингредиента, рецепта."""

from django.contrib import admin

from .models import Tag

admin.site.register(Tag)
