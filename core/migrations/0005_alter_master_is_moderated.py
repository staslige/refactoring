# Generated by Django 4.2.7 on 2023-12-01 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_master_is_moderated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='master',
            name='is_moderated',
            field=models.BooleanField(default=False, verbose_name='Модерация'),
        ),
    ]
