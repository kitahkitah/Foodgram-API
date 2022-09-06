"""Определение моделей тега, ингредиента, рецепта."""

from django.db import models

from .fields import HEXColor


class Tag(models.Model):
    """Модель тега для рецепта."""

    color = HEXColor('цвет в HEX', blank=True)
    name = models.CharField('название', max_length=200, blank=False)
    slug = models.SlugField('Уникальный slug', max_length=200,
                            unique=True, blank=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name}: {self.slug}'
