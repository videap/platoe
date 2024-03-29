# Generated by Django 3.1.1 on 2021-01-13 02:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0024_remove_user_stripe_account_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stripe_Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('context', models.CharField(max_length=21)),
                ('account_owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='stripe_account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Bank_Account',
        ),
    ]
