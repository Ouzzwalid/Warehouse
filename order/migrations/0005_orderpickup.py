# Generated by Django 4.0.1 on 2022-02-23 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0004_delete_orderpickup_orderitems_emplacement'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderPickUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255)),
                ('product_id', models.CharField(max_length=255)),
                ('emplacement', models.CharField(max_length=255)),
                ('pick_quantity', models.PositiveIntegerField()),
            ],
        ),
    ]
