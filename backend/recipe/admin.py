from django.contrib import admin
from .models import Tag, Ingredient, Recipe, Amount


class RecipeAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'author',
        'favorites',
    )
    readonly_fields = (
        'favorites',
    )
    list_filter = (
        'name',
        'author',
        'tags',
    )
    search_fields = (
        'name',
        'author__username',
        'tags__name',
    )

    def favorites(self, obj):
        return obj.favorites.count()

    favorites.short_description = 'В избранном'


class IngredientAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )
    search_fields = (
        'name',
    )


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Amount)
