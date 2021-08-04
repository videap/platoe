# Generated by Django 3.1.1 on 2021-01-15 03:56

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0030_auto_20210113_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='idea_timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]