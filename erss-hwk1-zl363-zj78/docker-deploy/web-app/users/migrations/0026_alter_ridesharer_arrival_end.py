# Generated by Django 4.1.5 on 2023-02-03 00:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_alter_ridesharer_arrival_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ridesharer',
            name='arrival_end',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 2, 21, 28, 6, 341107)),
        ),
    ]
