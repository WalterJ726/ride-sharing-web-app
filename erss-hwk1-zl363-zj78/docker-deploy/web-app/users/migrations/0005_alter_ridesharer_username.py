# Generated by Django 4.1.5 on 2023-01-29 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_remove_ridesharer_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ridesharer',
            name='username',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
    ]
