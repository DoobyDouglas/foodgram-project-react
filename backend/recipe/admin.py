from django.contrib import admin
from .models import Tag, ingredient, Recipe, Amount


admin.site.register(Tag)
admin.site.register(ingredient)
admin.site.register(Recipe)
admin.site.register(Amount)
