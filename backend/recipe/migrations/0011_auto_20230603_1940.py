# Generated by Django 3.2.19 on 2023-06-03 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0010_auto_20230603_1748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='image',
            field=models.ImageField(upload_to='recipes/images/', verbose_name='Изображение'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.ManyToManyField(related_name='recipes', through='recipe.Amount', to='recipe.Ingredient', verbose_name='Ингредиенты блюда'),
        ),
    ]
