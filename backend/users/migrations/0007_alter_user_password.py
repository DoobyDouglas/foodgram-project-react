# Generated by Django 3.2.19 on 2023-06-02 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=150, verbose_name='Пароль'),
        ),
    ]