# Generated by Django 4.0.1 on 2022-02-25 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Manager'), (2, 'Vendeur'), (3, 'Livreur'), (4, 'Receiver'), (5, 'Picker')], null=True),
        ),
    ]