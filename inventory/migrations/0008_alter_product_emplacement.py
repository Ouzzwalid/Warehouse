# Generated by Django 4.0.1 on 2022-02-23 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0007_alter_product_emplacement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='emplacement',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.emplacement'),
        ),
    ]
