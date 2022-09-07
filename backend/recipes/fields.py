"""Кастомные поля Django."""

from base64 import b64decode
from re import compile as re_compile

from django.core.files.base import ContentFile
from django.core.validators import RegexValidator
from django.db import models
from rest_framework import serializers

HEX_COLOR_VALIDATOR = RegexValidator(
    re_compile('^#[A-Fa-f0-9]{6}$'),
    'Введите валидный цвет в формате HEX (#000000)',
    'invalid',
)


class HEXColor(models.CharField):
    """Поле модели для цвета в формате HEX с валидацией."""

    def __init__(self, *args, **kwargs):
        super(HEXColor, self).__init__(*args, **kwargs)

        self.max_length = 7
        self.validators.append(HEX_COLOR_VALIDATOR)


class Base64ImageField(serializers.ImageField):
    """Поле сериализатора для картинки в формате Base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            extension, imgstr = data.split(';base64,')
            ext = extension.split('/')[-1]
            data = ContentFile(b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)
