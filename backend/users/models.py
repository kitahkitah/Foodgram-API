"""Переопределение модели пользователя."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    first_name = models.CharField('имя', max_length=150, blank=False)
    email = models.EmailField('email', max_length=254, unique=True, blank=False)
    last_name = models.CharField('фамилия', max_length=150, blank=False)
    password = models.CharField('пароль', max_length=150)

    class Meta:
        ordering = ('id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'


class Subscription(models.Model):
    """Модель подписки."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed_by',
        verbose_name='автор',
    )
    subscriber = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='subscribed_to',
        verbose_name='подписчик',
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('author', 'subscriber'),
                name='cant_follow_twice',
            ),
        )

    def __str__(self):
        return f'Подписка {self.subscriber} на {self.author}'
