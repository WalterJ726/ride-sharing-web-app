# Generated by Django 4.1.5 on 2023-01-29 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_remove_ridesharer_owner_id_alter_ridesharer_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='ridesharer',
            name='owner_id',
            field=models.PositiveBigIntegerField(blank=True, default=0),
        ),
    ]
