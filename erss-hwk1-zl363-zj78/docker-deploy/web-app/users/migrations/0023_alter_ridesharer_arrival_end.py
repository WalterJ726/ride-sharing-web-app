# Generated by Django 4.1.5 on 2023-02-03 00:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_alter_ridesharer_arrival_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ridesharer',
            name='arrival_end',
            field=models.DateTimeField(default=datetime.datetime(2023, 2, 2, 21, 3, 1, 764170)),
        ),
    ]