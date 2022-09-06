"""Кастомные поля Django."""

from re import compile as re_compile

from django.core.validators import RegexValidator
from django.db import models

HEX_COLOR_VALIDATOR = RegexValidator(
    re_compile('^#[A-Fa-f0-9]{6}$'),
    'Введите валидный цвет в формате HEX (#000000)',
    'invalid'
)


class HEXColor(models.CharField):
    """Поле для цвета в формате HEX с валидацией."""

    def __init__(self, *args, **kwargs):
        super(HEXColor, self).__init__(*args, **kwargs)

        self.max_length = 7
        self.validators.append(HEX_COLOR_VALIDATOR)
