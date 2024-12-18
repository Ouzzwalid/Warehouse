# Generated by Django 4.0.1 on 2022-02-22 21:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=30, unique=True)),
                ('cost', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=60, verbose_name='full name')),
                ('address', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('status', models.TextField(choices=[('Created', 'Created'), ('Pending', 'Pending'), ('Reported', 'Reported'), ('Canceled', 'Canceled'), ('Delivered', 'Delivered'), ('No answer', 'No answer'), ('Returned', 'Returned'), ('Out for delivery', 'Out for delivery')], default='Created')),
                ('order_fees', models.DecimalField(decimal_places=2, default=0, max_digits=6, null=True)),
                ('order_amount', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True, verbose_name='Total')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='order.customer')),
            ],
        ),
        migrations.CreateModel(
            name='OrderPickUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255)),
                ('item_id', models.CharField(max_length=255)),
                ('emplacement_id', models.CharField(max_length=255)),
                ('pick_quantity', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_price', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='price')),
                ('quantity', models.PositiveIntegerField(null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='product',
            field=models.ManyToManyField(through='order.OrderItems', to='inventory.Product'),
        ),
    ]
