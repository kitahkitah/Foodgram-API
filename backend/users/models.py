"""Переопределение модели пользователя."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Переопределённая модель пользователя."""

    email = models.EmailField('email', unique=True, blank=False)
