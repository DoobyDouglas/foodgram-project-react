from django.core.management.base import BaseCommand
from recipe.models import Ingredient
from django.conf import settings
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        data_path = f'{settings.BASE_DIR}/data/ingredients.json'
        with open(data_path, encoding='utf-8') as file:
            data = json.load(file)
        ingredients = []
        for item in data:
            ingredient = Ingredient(
                name=item['name'],
                measurement_unit=item['measurement_unit'],
            )
            ingredients.append(ingredient)
        Ingredient.objects.bulk_create(ingredients)
