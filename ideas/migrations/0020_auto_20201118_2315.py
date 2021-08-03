# Generated by Django 3.1.1 on 2020-11-19 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0019_auto_20201118_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shared_idea',
            name='idea_shared',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ideas.idea'),
        ),
        migrations.AlterField(
            model_name='shared_idea',
            name='request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request_shared_ideas', to='ideas.request'),
        ),
    ]