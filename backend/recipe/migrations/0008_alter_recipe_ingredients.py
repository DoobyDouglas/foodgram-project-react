# Generated by Django 3.2.19 on 2023-06-02 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0007_alter_recipe_ingredients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipe.Amount', to='recipe.Ingredient', verbose_name='Ингредиенты блюда'),
        ),
    ]
