# Generated by Django 4.0.1 on 2022-02-25 22:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_orderpickup'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderpickup',
            old_name='order_id',
            new_name='order',
        ),
        migrations.RenameField(
            model_name='orderpickup',
            old_name='product_id',
            new_name='product',
        ),
    ]