# Generated by Django 4.0.1 on 2022-02-23 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_alter_product_unstored_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='emplacement',
            field=models.ForeignKey(default='UNSTORED', null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.emplacement'),
        ),
    ]