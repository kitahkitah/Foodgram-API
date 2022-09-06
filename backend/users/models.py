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
