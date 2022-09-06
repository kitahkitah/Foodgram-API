"""Определение моделей тега, ингредиента, рецепта."""

from django.db import models

from .fields import HEXColor


class Tag(models.Model):
    """Модель тега для рецепта."""

    color = HEXColor('цвет в HEX', blank=True)
    name = models.CharField('название', max_length=200, blank=False)
    slug = models.SlugField('уникальный slug', max_length=200,
                            unique=True, blank=False)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.slug})'

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        return super(Tag, self).save(*args, **kwargs)


class Ingredient(models.Model):
    """Модель тега для ингредиента."""

    measurement_unit = models.CharField('единица', max_length=200, blank=False)
    name = models.CharField('название', max_length=200, blank=False)

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['name'])
        ]

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'

    def save(self, *args, **kwargs):
        self.measurement_unit = self.measurement_unit.casefold()
        self.name = self.name.capitalize()
        return super(Ingredient, self).save(*args, **kwargs)
