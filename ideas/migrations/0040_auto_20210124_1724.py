# Generated by Django 3.1.1 on 2021-01-24 20:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0039_auto_20210119_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='banking_accept',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='banking_accept_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='payment_accept',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='payment_accept_time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]