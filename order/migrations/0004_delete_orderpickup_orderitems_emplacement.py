# Generated by Django 4.0.1 on 2022-02-23 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_alter_order_status'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OrderPickUp',
        ),
        migrations.AddField(
            model_name='orderitems',
            name='emplacement',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
