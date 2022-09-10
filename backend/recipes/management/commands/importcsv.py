import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import models

from recipes.models import Ingredient


def importcsv2db(model: models.Model, csv_file: str, field_list: list):
    """Импортирует из файла csv_file в базу модели model
    в field_list - список с именем полей.
    """

    with open(csv_file, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        row_number = 0
        for row in csvreader:
            try:
                print(dict(zip(field_list, row)))
                model.objects.create(**dict(zip(field_list, row)))
            except Exception as err1:
                print(f'Ошибка импорта строки {row_number}')
                print(err1)
            row_number += 1


class Command(BaseCommand):
    def handle(self, *args, **options):
        importcsv2db(
            Ingredient,
            settings.BASE_DIR / 'data/' / 'ingredients.csv',
            ['name', 'measurement_unit']
        )
