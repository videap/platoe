# Generated by Django 3.1.1 on 2020-10-02 03:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0002_auto_20201002_0001'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Cards',
            new_name='Card',
        ),
    ]