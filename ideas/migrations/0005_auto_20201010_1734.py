# Generated by Django 3.1.1 on 2020-10-10 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0004_auto_20201010_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=24),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=24),
        ),
    ]
