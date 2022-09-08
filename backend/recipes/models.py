"""Определение моделей тега, ингредиента, рецепта."""

from django.core.validators import MinValueValidator
from django.db import models

from users.models import User
from .fields import HEXColor


class Tag(models.Model):
    """Модель тега для рецепта."""

    color = HEXColor('цвет в HEX', blank=False, unique=True)
    name = models.CharField('название', max_length=200,
                            blank=False, unique=True)
    slug = models.SlugField('уникальный slug', max_length=200,
                            blank=False, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'тег'
        verbose_name_plural = 'теги'

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
        verbose_name = 'ингредиент'
        verbose_name_plural = 'ингредиенты'
        indexes = (models.Index(fields=['name']),)

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'

    def save(self, *args, **kwargs):
        self.measurement_unit = self.measurement_unit.casefold()
        self.name = self.name.capitalize()
        return super(Ingredient, self).save(*args, **kwargs)


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор',
    )
    cooking_time = models.PositiveSmallIntegerField(
        'время приготовления',
        validators=(MinValueValidator(1, 'Не меньше 1 минуты!'),),
    )
    favorited_by = models.ManyToManyField(
        User,
        related_name='favorites',
        verbose_name='избранное',
    )
    image = models.ImageField('картинка', upload_to='recipes/', blank=False)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredientAmount',
        verbose_name='ингредиенты',
    )
    name = models.CharField('название', max_length=200, blank=False)
    in_shopping_cart_of = models.ManyToManyField(
        User,
        related_name='shopping_cart',
        verbose_name='корзина',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='теги',
    )
    text = models.TextField('описание')

    class Meta:
        ordering = ('-id',)
        verbose_name = 'рецепт'
        verbose_name_plural = 'рецепты'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.capitalize()
        return super(Recipe, self).save(*args, **kwargs)


class RecipeIngredientAmount(models.Model):
    amount = models.PositiveSmallIntegerField(
        'количество',
        validators=(MinValueValidator(1, 'Минимальное количество - 1!'),),
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='ингредиент',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='рецепт',
    )

    class Meta:
        verbose_name = 'количество ингредиента к рецепту'
        verbose_name_plural = 'количество ингредиентов к рецепту'
        constraints = (
            models.UniqueConstraint(
                fields=('ingredient', 'recipe',),
                name='unique_ingredient_for_recipe',
            ),
        )

    def __str__(self):
        return f'Ингредиент "{self.ingredient}" для "{self.recipe}"/{self.amount}'
