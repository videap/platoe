# Generated by Django 3.1.1 on 2021-01-15 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0033_idea_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='idea',
            name='status',
            field=models.CharField(default='offered', max_length=12),
        ),
    ]
