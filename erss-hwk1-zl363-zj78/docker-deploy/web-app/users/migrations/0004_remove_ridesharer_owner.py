# Generated by Django 4.1.5 on 2023-01-29 02:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_ridedriver_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ridesharer',
            name='owner',
        ),
    ]