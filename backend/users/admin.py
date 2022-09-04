"""Настройки админки для модели пользователя."""

from django.contrib import admin

from .models import User

admin.site.register(User)
