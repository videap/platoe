# Generated by Django 3.1.1 on 2021-01-13 00:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0023_auto_20210112_2105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='stripe_account_id',
        ),
    ]