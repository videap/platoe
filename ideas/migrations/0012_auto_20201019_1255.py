# Generated by Django 3.1.1 on 2020-10-19 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0011_user_last_login_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='last_login_datetime',
            new_name='last_login_attempt',
        ),
    ]
