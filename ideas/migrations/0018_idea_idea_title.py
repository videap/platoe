# Generated by Django 3.1.1 on 2020-11-18 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0017_remove_idea_is_requested'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='idea_title',
            field=models.CharField(blank=True, max_length=72),
        ),
    ]
