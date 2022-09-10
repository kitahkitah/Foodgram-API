"""Кастомные поля Django."""

from base64 import b64decode
from re import compile as re_compile
from uuid import uuid4

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
        super().__init__(*args, **kwargs)
        self.validators.append(HEX_COLOR_VALIDATOR)


class Base64ImageField(serializers.ImageField):
    """Поле сериализатора для картинки в формате Base64."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            extension, imgstr = data.split(';base64,')
            ext = extension.split('/')[-1]
            data = ContentFile(b64decode(imgstr), name=str(uuid4()) + '.' + ext)

        return super().to_internal_value(data)


class ModelPKRelatedField(serializers.PrimaryKeyRelatedField):
    """Поле сериализатора PKRelated с репрезентацией модели."""

    def __init__(self, **kwargs):
        self.serializer = kwargs.pop('serializer')
        super().__init__(**kwargs)

    def to_representation(self, value):
        return self.serializer(value, context=self.context).data
